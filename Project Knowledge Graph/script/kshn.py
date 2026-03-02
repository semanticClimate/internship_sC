"""
kshn — Wikidata-First Approach

"""

import sys, os, json, re, argparse, html as html_mod, time
from pathlib import Path
from collections import Counter
from itertools import combinations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Optional, Tuple, Any
from bs4 import BeautifulSoup
import networkx as nx
try:
    import requests
except ImportError:
    requests = None


@dataclass
class Entity:
    id: str
    term: str
    qid: str
    wiki_url: str
    description: str
    links: List[Dict[str, str]] = field(default_factory=list)
    para_groups: List[List[str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Triple:
    subject: str
    subjectLabel: str
    predicate: str
    predicateId: str
    object: str
    objectLabel: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

# ─────────────────────────────────────────────────────────────────────────────
# 1. PARSE HTML — extract QIDs and metadata
# ─────────────────────────────────────────────────────────────────────────────

def load_html(file_path: str) -> BeautifulSoup:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return BeautifulSoup(f, 'html.parser')
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found."); sys.exit(1)
    except Exception as e:
        print(f"Error: {e}"); sys.exit(1)


def extract_entries(soup: BeautifulSoup) -> List[Entity]:
    """
    Extract (term, QID, wiki_url, description, links) from <div role="ami_entry">.
    Uses div attributes directly — no guessing.
    """
    entries: List[Entity] = []
    for div in soup.find_all('div', attrs={"role": "ami_entry"}):
        term = div.get('term', '').strip() or div.get('name', '').strip()
        qid = div.get('wikidataid', '').strip()
        wiki_url = div.get('wikipedia_url', '').strip()

        if not term:
            tag = div.find(class_='term') or div.find(['b', 'h1', 'h2', 'strong'])
            term = tag.get_text(strip=True) if tag else "Unknown"

        if not wiki_url:
            a_tag = div.find('a', href=lambda x: x and 'wikipedia.org' in x)
            wiki_url = a_tag['href'] if a_tag else ""

        first_p = div.find('p', class_='wpage_first_para') or div.find('p')
        desc = first_p.get_text(strip=True) if first_p else ""
        if len(desc) > 500:
            desc = desc[:500] + '...'

        # Per-paragraph link groups (for co-occurrence counting)
        links = []
        para_groups = []  # list of lists: which entities co-occur per paragraph
        for p in div.find_all('p'):
            para_links = []
            for a in p.find_all('a'):
                href = a.get('href', '')
                title = a.get('title', '')
                link_text = a.get_text(strip=True)
                if href.startswith('#') or not link_text or len(link_text) < 2:
                    continue
                links.append({'text': link_text, 'title': title, 'href': href})
                para_links.append(link_text)
            if para_links:
                para_groups.append(para_links)

        node_id = qid if qid else term
        entries.append(Entity(
            id=node_id, term=term, qid=qid,
            wiki_url=wiki_url, description=desc,
            links=links, para_groups=para_groups,
        ))

    return entries


# ─────────────────────────────────────────────────────────────────────────────
# 2. DEDUPLICATION
# ─────────────────────────────────────────────────────────────────────────────

def normalize_key(term: str) -> str:
    t = term.strip().lower()
    t = re.sub(r'\s+', ' ', t)
    if t.endswith('ies') and len(t) > 5:  t = t[:-3] + 'y'
    elif t.endswith('ses') and len(t) > 5: t = t[:-2]
    elif t.endswith('es') and len(t) > 4 and not t.endswith('ies'): t = t[:-2]
    elif t.endswith('s') and len(t) > 3 and not t.endswith('ss'): t = t[:-1]
    return t


def deduplicate_entries(entries: List[Entity]) -> Tuple[List[Entity], Dict[str, str]]:
    key_to_group: Dict[str, List[Entity]] = {}
    for e in entries:
        key = normalize_key(e.term)
        key_to_group.setdefault(key, []).append(e)

    deduped: List[Entity] = []
    term_to_id: Dict[str, str] = {}
    for key, group in key_to_group.items():
        best = max(group, key=lambda e: (len(e.description), bool(e.qid), -len(e.term)))
        deduped.append(best)
        for e in group:
            term_to_id[e.term] = best.id
            if e.qid:
                term_to_id[e.qid] = best.id

    return deduped, term_to_id


# ─────────────────────────────────────────────────────────────────────────────
# 3. WIKIDATA SPARQL — the core
# ─────────────────────────────────────────────────────────────────────────────

# Common property labels so we don't need SERVICE wikibase:label in every query
PROPERTY_LABELS = {
    'P17': 'country', 'P27': 'country of citizenship',
    'P30': 'continent', 'P31': 'instance of', 'P36': 'capital',
    'P47': 'shares border with', 'P131': 'located in',
    'P137': 'operator', 'P138': 'named after',
    'P150': 'contains', 'P155': 'follows', 'P156': 'followed by',
    'P159': 'headquarters', 'P176': 'manufacturer',
    'P186': 'made from', 'P279': 'subclass of',
    'P361': 'part of', 'P366': 'has use',
    'P460': 'same as', 'P461': 'opposite of',
    'P495': 'country of origin', 'P527': 'has part',
    'P737': 'influenced by', 'P828': 'has cause',
    'P910': 'main category', 'P921': 'main subject',
    'P1056': 'product', 'P1127': 'owned by',
    'P1269': 'facet of', 'P1376': 'capital of',
    'P1382': 'overlaps with', 'P1535': 'used by',
    'P1542': 'has effect', 'P1552': 'has quality',
    'P2283': 'uses', 'P2579': 'studied by',
    'P3095': 'practiced by', 'P2670': 'has parts of class',
    'P530': 'diplomatic relation', 'P463': 'member of',
    'P706': 'geographically located in',
    'P2388': 'office held by',
    'P37': 'official language', 'P38': 'currency',
    'P194': 'legislative body', 'P35': 'head of state',
    'P1151': 'topic of', 'P2348': 'time period',
    'P1365': 'replaces',
    'P1366': 'replaced by',
    'P2789': 'connects with',
}

# Vibrant Premium Palette
TYPE_COLORS = {
    'Country': '#4CAF50', 'City': '#81C784', 'Continent': '#2E7D32',
    'Region': '#43A047', 'Person': '#F06292', 'Organization': '#FFB74D',
    'Technology': '#2196F3', 'Chemical': '#BA68C8', 'Publication': '#8D6E63',
    'Software': '#00BCD4', 'Tool': '#90A4AE', 'Unit': '#DCE775',
    'WikiPage': '#78909C', 'Concept': '#64B5F6', 'unknown': '#888888',
    'Category': '#FFD54F', 'Taxon': '#FF6B6B', 'field of study': '#F7DC6F',
    'biological process': '#BB8FCE', 'sex': '#FFEAA7', 'medical attribute': '#A3E4D7',
    'structural class of chemical entities': '#F1948A', 'type of chemical entity': '#F7DC6F',
}


def get_type_color(t: str) -> str:
    """Get color for a type, with a deterministic fallback for unknown types."""
    if t in TYPE_COLORS:
        return TYPE_COLORS[t]
    # Simple hash-based color fallback
    import hashlib
    h = hashlib.md5(t.encode()).hexdigest()
    # Use the first 6 chars of md5 for a hex color, but keep it somewhat bright
    # by ensuring higher values
    r = int(h[0:2], 16) % 155 + 100
    g = int(h[2:4], 16) % 155 + 100
    b = int(h[4:6], 16) % 155 + 100
    return f"#{r:02x}{g:02x}{b:02x}"


def fetch_wikidata_graph(qids: Set[str], cache_path: Optional[str] = None) -> List[Triple]:
    """
    Query Wikidata SPARQL for direct relationships between our QIDs.
    Strategy: query 50 subjects at a time for ALL their direct claims,
    then filter locally to keep only triples where object is in our set.
    ~11 queries instead of 169 (40x40 cross-product).
    """
    try:
        from SPARQLWrapper import SPARQLWrapper, JSON as SPARQL_JSON
    except ImportError:
        print("  SPARQLWrapper not installed. Run: pip install SPARQLWrapper")
        return []

    # Check cache
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            try:
                cached = json.load(f)
                if cached:
                    print(f"  Loaded {len(cached)} cached triples")
                    # Reconstruct Triple objects from cached dicts
                    return [Triple(**t) if isinstance(t, dict) else t for t in cached]
            except json.JSONDecodeError:
                print(f"  Cache file {cache_path} is invalid. Fetching fresh data...")

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.addCustomHttpHeader("User-Agent", "kshn/3.0 (educational project)")

    all_triples = []
    qid_list = list(qids)
    qid_set = set(qids)
    BATCH = 50
    total_batches = (len(qid_list) + BATCH - 1) // BATCH

    print(f"  {len(qid_list)} QIDs -> {total_batches} SPARQL batches...")

    for i in range(0, len(qid_list), BATCH):
        batch = qid_list[i:i+BATCH]
        batch_num = i // BATCH + 1
        values = ' '.join(f'wd:{q}' for q in batch)

        query = f"""
        SELECT ?s ?p ?o ?sLabel ?oLabel WHERE {{
            VALUES ?s {{ {values} }}
            ?s ?prop ?o .
            BIND(REPLACE(STR(?prop), ".*/", "") AS ?p)
            FILTER(STRSTARTS(STR(?prop), "http://www.wikidata.org/prop/direct/"))
            FILTER(STRSTARTS(STR(?o), "http://www.wikidata.org/entity/Q"))
            FILTER(?s != ?o)
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 5000
        """
        # Retry with backoff
        for attempt in range(3):
            try:
                sparql.setQuery(query)
                sparql.setReturnFormat(SPARQL_JSON)
                results = sparql.query().convert()

                for r in results['results']['bindings']:
                    subj = r['s']['value'].split('/')[-1]
                    obj = r['o']['value'].split('/')[-1]
                    prop_id = r.get('p', {}).get('value', '')
                    # Only keep if object is in our entity set
                    if obj not in qid_set:
                        continue
                    subj_label = r.get('sLabel', {}).get('value', subj)
                    obj_label = r.get('oLabel', {}).get('value', obj)
                    prop_label = PROPERTY_LABELS.get(prop_id, prop_id)
                    all_triples.append(Triple(
                        subject=subj, subjectLabel=subj_label,
                        predicate=prop_label, predicateId=prop_id,
                        object=obj, objectLabel=obj_label,
                    ))
                break
            except Exception as ex:
                if attempt < 2:
                    wait = 3 * (attempt + 1)
                    print(f"    Batch {batch_num} retry {attempt+1} in {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"    Batch {batch_num}/{total_batches} failed: {ex}")

        print(f"    Batch {batch_num}/{total_batches}: {len(all_triples)} triples")
        time.sleep(1)

    # Deduplicate
    seen = set()
    unique: List[Triple] = []
    for t in all_triples:
        key = (t.subject, t.predicateId, t.object)
        if key not in seen:
            seen.add(key)
            unique.append(t)

    print(f"  {len(unique)} unique triples")

    if cache_path:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in unique], f, indent=2, ensure_ascii=False)
        print(f"  Cached to {cache_path}")

    return unique


def fetch_entity_types(qids: List[str], cache_path: Optional[str] = None) -> Dict[str, str]:
    """Fetch P31 (instance of) types for each QID."""
    try:
        from SPARQLWrapper import SPARQLWrapper, JSON as SPARQL_JSON
    except ImportError:
        return {}

    cache = {}
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache = json.load(f)

    todo = [q for q in qids if q not in cache]
    if not todo:
        return cache

    print(f"  Fetching types for {len(todo)} entities...")
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.addCustomHttpHeader("User-Agent", "kshn/3.0 (educational project)")

    # Step 1: Fetch type QIDs (fast, no label service)
    qid_to_type_qid: Dict[str, str] = {}
    for i in range(0, len(todo), 50):
        batch = todo[i:i+50]
        values = ' '.join(f'wd:{q}' for q in batch)
        query = f"""
        SELECT ?item ?type WHERE {{
          VALUES ?item {{ {values} }}
          ?item wdt:P31 ?type .
        }}
        """
        try:
            sparql.setQuery(query)
            sparql.setReturnFormat(SPARQL_JSON)
            results = sparql.query().convert()
            for r in results['results']['bindings']:
                qid = r['item']['value'].split('/')[-1]
                type_qid = r['type']['value'].split('/')[-1]
                if qid not in qid_to_type_qid:
                    qid_to_type_qid[qid] = type_qid
        except Exception as e:
            print(f"  Error fetching type QIDs: {e}")
        if i + 50 < len(todo):
            time.sleep(1)

    # Step 2: Resolve type QID labels in one query
    unique_type_qids = list(set(qid_to_type_qid.values()))
    type_qid_to_label: Dict[str, str] = {}
    if unique_type_qids:
        for i in range(0, len(unique_type_qids), 100):
            batch = unique_type_qids[i:i+100]
            values = ' '.join(f'wd:{q}' for q in batch)
            query = f"""
            SELECT ?type ?typeLabel WHERE {{
              VALUES ?type {{ {values} }}
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            """
            try:
                sparql.setQuery(query)
                sparql.setReturnFormat(SPARQL_JSON)
                results = sparql.query().convert()
                for r in results['results']['bindings']:
                    tqid = r['type']['value'].split('/')[-1]
                    label = r['typeLabel']['value']
                    # If label is still a QID, skip it
                    if not label.startswith('Q'):
                        type_qid_to_label[tqid] = label
            except Exception as e:
                print(f"  Error fetching type labels: {e}")
            if i + 100 < len(unique_type_qids):
                time.sleep(1)

    # Step 3: Combine - map entity QIDs to human-readable type labels
    for qid, type_qid in qid_to_type_qid.items():
        label = type_qid_to_label.get(type_qid, type_qid)
        cache[qid] = label

    if cache_path:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)

    return cache


# ─────────────────────────────────────────────────────────────────────────────
# 4. BUILD GRAPH
# ─────────────────────────────────────────────────────────────────────────────

def build_wikidata_graph(entries: List[Entity], triples: List[Triple], type_cache: Dict[str, str]) -> nx.DiGraph:
    """Build graph primarily from Wikidata triples."""
    G = nx.DiGraph()

    # Add our encyclopedia entries as nodes
    for e in entries:
        qid = e.qid
        node_type = type_cache.get(qid, 'Concept')

        G.add_node(e.id,
            label=e.term, qid=qid,
            wiki_url=e.wiki_url,
            description=e.description,
            node_type=node_type,
        )

    # Add edges from Wikidata triples
    for t in triples:
        src = t.subject
        tgt = t.object
        label = t.predicate

        if src in G and tgt in G and src != tgt:
            G.add_edge(src, tgt, label=label, predicate_id=t.predicateId, source='wikidata')

    return G


def add_text_edges(G: nx.DiGraph, entries: List[Entity], term_to_id: Dict[str, str]) -> int:
    """Add text-based edges as supplement (lower priority than Wikidata edges)."""
    added = 0
    for e in entries:
        src = e.id
        if src not in G:
            continue
        for link in e.links:
            target_text = link['text']
            tgt = term_to_id.get(target_text)
            if not tgt:
                tgt = term_to_id.get(normalize_key(target_text))
            if not tgt or tgt == src or tgt not in G:
                continue
            if not G.has_edge(src, tgt):
                G.add_edge(src, tgt, label='mentions', source='text')
                added += 1
    return added


# ─────────────────────────────────────────────────────────────────────────────
# 4b. CO-OCCURRENCE NETWORKS
# ─────────────────────────────────────────────────────────────────────────────

def compute_cooccurrence(entries: List[Entity], term_to_id: Dict[str, str], G: nx.DiGraph) -> Tuple[int, int]:
    """
    Count co-occurrence: how often two entities appear in the same paragraph.
    Applies co-occurrence count as edge weight.
    """
    pair_counts = Counter()

    for e in entries:
        src_id = e.id
        if src_id not in G:
            continue

        for para_links in e.para_groups:
            # Resolve each link text to a canonical node id
            resolved = set()
            for text in para_links:
                nid = term_to_id.get(text) or term_to_id.get(normalize_key(text))
                if nid and nid in G:
                    resolved.add(nid)
            # Also include the source entry itself
            resolved.add(src_id)

            # Count all pairs
            for a, b in combinations(sorted(resolved), 2):
                if a != b:
                    pair_counts[(a, b)] += 1

    # Apply weights to existing edges or add new co-occurrence edges
    added = 0
    for (a, b), count in pair_counts.items():
        if G.has_edge(a, b):
            G.edges[a, b]['weight'] = count
        elif G.has_edge(b, a):
            G.edges[b, a]['weight'] = count
        elif count >= 2:  # Only add co-occurrence edges if they appear 2+ times
            G.add_edge(a, b, label='co-occurs', source='cooccurrence', weight=count)
            added += 1

    return len(pair_counts), added


# ─────────────────────────────────────────────────────────────────────────────
# 4c. CATEGORY HIERARCHY (Wikipedia MediaWiki API)
# ─────────────────────────────────────────────────────────────────────────────

def fetch_categories(entries: List[Entity], G: nx.DiGraph, cache_path: Optional[str] = None) -> Tuple[int, int]:
    """
    Fetch Wikipedia categories for each entity via MediaWiki API.
    Adds shared parent categories as nodes + 'in_category' edges.
    """
    if requests is None:
        print("  'requests' not installed. Run: pip install requests")
        return 0, 0

    # Load cache
    cat_cache = {}
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            cat_cache = json.load(f)
        print(f"  Loaded {len(cat_cache)} cached category sets")

    # Collect Wikipedia page titles from URLs
    title_to_id: Dict[str, str] = {}
    for e in entries:
        url = e.wiki_url
        if 'wikipedia.org/wiki/' in url:
            title = url.split('/wiki/')[-1]
            title_to_id[title] = e.id

    # Fetch categories for titles not already cached
    api_url = "https://en.wikipedia.org/w/api.php"
    todo = [t for t in title_to_id if t not in cat_cache]

    if todo:
        print(f"  Fetching categories for {len(todo)} pages...")
        # MediaWiki API supports up to 50 titles per request
        for i in range(0, len(todo), 50):
            batch = todo[i:i+50]
            params = {
                'action': 'query', 'titles': '|'.join(batch),
                'prop': 'categories', 'cllimit': '20',
                'clshow': '!hidden', 'format': 'json',
            }
            try:
                resp = requests.get(api_url, params=params,
                                    headers={'User-Agent': 'kshn/3.0'},
                                    timeout=15)
                data = resp.json()
                pages = data.get('query', {}).get('pages', {})
                for page_id, page_data in pages.items():
                    title = page_data.get('title', '').replace(' ', '_')
                    cats = [c['title'].replace('Category:', '')
                            for c in page_data.get('categories', [])
                            if not any(x in c['title'].lower() for x in
                                       ['stub', 'article', 'pages', 'dmy dates',
                                        'cs1', 'wikidata', 'short description',
                                        'use mdy', 'commons category', 'webarchive',
                                        'good articles', 'featured'])]
                    cat_cache[title] = cats
            except Exception as ex:
                print(f"    MediaWiki API error: {ex}")

            if i + 50 < len(todo):
                time.sleep(0.5)

    # Save cache
    if cache_path:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cat_cache, f, indent=2, ensure_ascii=False)

    # Find shared categories (categories that 2+ entities share)
    cat_members = Counter()  # category -> count of entities
    entity_cats = {}  # node_id -> set of categories
    for title, node_id in title_to_id.items():
        if title in cat_cache and node_id in G:
            cats = set(cat_cache[title])
            entity_cats[node_id] = cats
            for c in cats:
                cat_members[c] += 1

    # Add only categories shared by 3+ entities (to avoid noise)
    shared_cats = {c for c, count in cat_members.items() if count >= 3}
    cat_nodes_added = 0
    cat_edges_added = 0

    for cat in shared_cats:
        cat_node_id = f"cat:{cat}"
        if cat_node_id not in G:
            G.add_node(cat_node_id,
                label=cat, qid='', wiki_url='',
                description=f'Wikipedia category ({cat_members[cat]} entities)',
                node_type='Category',
            )
            cat_nodes_added += 1

        for node_id, cats in entity_cats.items():
            if cat in cats and not G.has_edge(node_id, cat_node_id):
                G.add_edge(node_id, cat_node_id,
                           label='in_category', source='wikipedia')
                cat_edges_added += 1

    return cat_nodes_added, cat_edges_added


# ─────────────────────────────────────────────────────────────────────────────
# 5. COMMUNITY DETECTION
# ─────────────────────────────────────────────────────────────────────────────

COMMUNITY_COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
    '#82E0AA', '#F8C471', '#D7BDE2', '#AED6F1', '#A3E4D7',
    '#FAD7A0', '#D5F5E3', '#FADBD8', '#D6EAF8', '#E8DAEF',
]


def detect_communities(G):
    try:
        UG = G.to_undirected()
        communities = nx.community.louvain_communities(UG, seed=42)
        for i, community in enumerate(communities):
            for node in community:
                G.nodes[node]['community'] = i
        return len(communities)
    except Exception:
        for n in G.nodes():
            G.nodes[n]['community'] = 0
        return 1


# ─────────────────────────────────────────────────────────────────────────────
# 6. EXPORT: GraphML
# ─────────────────────────────────────────────────────────────────────────────

def export_graphml(G, output_path):
    nx.write_graphml(G, output_path)
    print(f"  GraphML: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. EXPORT: Interactive HTML
# ─────────────────────────────────────────────────────────────────────────────

def generate_vis_data(G, color_by='type'):
    degrees = dict(G.degree())
    max_deg = max(degrees.values()) if degrees else 1
    min_size, max_size = 8, 30

    type_counts = Counter()
    edge_labels = Counter()
    vis_nodes = []

    for nid in G.nodes():
        data = G.nodes[nid]
        deg = degrees.get(nid, 0)
        label = data.get('label', nid)
        node_type = data.get('node_type', 'Concept')
        community = data.get('community', 0)

        if color_by == 'type':
            color = get_type_color(node_type)
        else:
            color = COMMUNITY_COLORS[community % len(COMMUNITY_COLORS)]

        type_counts[node_type] += 1
        size = min_size + (deg / max_deg) * (max_size - min_size) if max_deg > 0 else min_size

        esc_label = html_mod.escape(label)
        esc_desc = html_mod.escape(data.get('description', '')[:300])
        esc_url = html_mod.escape(data.get('wiki_url', ''))
        qid = data.get('qid', '')
        tooltip = (
            f"<div style='max-width:420px;color:#fff;font-family:system-ui,sans-serif;'>"
            f"<h3 style='margin:0 0 6px;color:{color};font-size:15px'>{esc_label}</h3>"
            f"<div style='font-size:11px;color:#aaa;margin-bottom:4px;'>"
            f"Type: <b>{node_type}</b> | Connections: <b>{deg}</b>"
            f"{f' | QID: <a href=\"https://www.wikidata.org/wiki/{qid}\" target=\"_blank\" style=\"color:#66b2ff\">{qid}</a>' if qid else ''}</div>"
            f"<div style='font-size:12px;color:#ddd;line-height:1.4;'>{esc_desc}</div>"
            f"{'<div style=\"margin-top:4px;\"><a href=\"' + esc_url + '\" target=\"_blank\" style=\"color:#66b2ff;font-size:11px;\">Wikipedia</a></div>' if esc_url else ''}"
            f"</div>"
        )

        vis_nodes.append({
            "id": nid, "label": label, "shape": "dot",
            "size": round(size, 1),
            "color": {
                "background": color,
                "border": color,
                "highlight": {"background": color, "border": color},
                "hover": {"background": color, "border": color}
            },
            "font": {"color": "#FFFFFF", "size": max(10, min(14, 8 + deg))},
            "title": tooltip, "group": node_type,
        })

    vis_edges = []
    for idx, (src, tgt, data) in enumerate(G.edges(data=True)):
        edge_label = data.get('label', 'relates_to')
        edge_labels[edge_label] += 1
        source = data.get('source', 'text')
        edge_color = '#4488ff' if source == 'wikidata' else '#555555'
        vis_edges.append({
            "id": str(idx), "from": src, "to": tgt,
            "title": f"<b>{edge_label}</b><br><span style='color:#888'>source: {source}</span>",
            "label": edge_label if len(edge_label) < 20 else "",
            "arrows": {"to": {"enabled": True, "scaleFactor": 0.4}},
            "color": {"color": edge_color, "highlight": "#66b2ff"},
            "font": {"color": "#888", "size": 9, "strokeWidth": 0, "align": "middle"},
        })

    return vis_nodes, vis_edges, dict(type_counts), dict(edge_labels)


def save_html(vis_nodes, vis_edges, type_counts, edge_labels, stats, output_path):
    nodes_json = json.dumps(vis_nodes, ensure_ascii=False)
    edges_json = json.dumps(vis_edges, ensure_ascii=False)

    # Legend
    legend_types = ""
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        c = get_type_color(t)
        legend_types += (
            f'<div class="legend-item" data-type="{t}">'
            f'<span class="legend-dot" style="background:{c}"></span>'
            f'{t} <span style="color:#666">({count})</span></div>\n'
        )

    # Top edge labels
    top_edges = sorted(edge_labels.items(), key=lambda x: -x[1])[:15]
    legend_edges = ""
    for label, count in top_edges:
        legend_edges += f'<div style="color:#aaa;font-size:11px;padding:1px 0">{label}: {count}</div>\n'

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{stats.get('title','')}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" crossorigin="anonymous"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Inter',system-ui,sans-serif; overflow:hidden; background:#080808; }}
        #mynetwork {{ width:100%; height:100vh; background:#080808; }}

        #loadingBar {{
            position:fixed; top:0; left:0; width:100%; height:100vh;
            background:rgba(8,8,8,0.97); z-index:10000;
            display:flex; align-items:center; justify-content:center; flex-direction:column;
            transition:opacity 0.5s;
        }}
        .loader-track {{ width:400px; height:6px; background:#1a1a1a; border-radius:3px; overflow:hidden; }}
        .loader-bar {{ height:100%; width:0%; background:linear-gradient(90deg,#2196F3,#4ECDC4); border-radius:3px; transition:width 0.2s; }}
        .loader-text {{ color:#666; font-size:13px; margin-top:12px; }}

        #searchBox {{
            position:fixed; top:14px; left:14px; z-index:9999;
            background:rgba(12,12,12,0.9); backdrop-filter:blur(12px);
            padding:8px 12px; border-radius:8px; border:1px solid #222;
            display:flex; gap:6px; align-items:center;
        }}
        #searchInput {{
            width:200px; padding:6px 10px; border:1px solid #333; outline:none;
            background:#111; color:#eee; border-radius:5px; font-size:12px;
        }}
        #searchInput:focus {{ border-color:#2196F3; }}
        #searchBtn {{
            padding:6px 12px; background:#2196F3; color:#fff; font-weight:600;
            border:none; border-radius:5px; cursor:pointer; font-size:12px;
        }}

        #panel {{
            position:fixed; top:14px; right:14px; z-index:9999;
            background:rgba(12,12,12,0.9); backdrop-filter:blur(12px);
            border:1px solid #222; border-radius:8px;
            padding:12px; max-width:210px; max-height:85vh;
            overflow-y:auto; color:#ddd; font-size:11px;
        }}
        #panel::-webkit-scrollbar {{ width:4px; }}
        #panel::-webkit-scrollbar-thumb {{ background:#333; border-radius:2px; }}
        .panel-section {{ margin-bottom:10px; }}
        .panel-title {{ font-size:12px; font-weight:600; color:#2196F3; margin-bottom:6px; }}
        .legend-item {{
            display:flex; align-items:center; margin-bottom:3px; cursor:pointer;
            padding:2px 4px; border-radius:3px; transition:background 0.15s;
        }}
        .legend-item:hover {{ background:rgba(255,255,255,0.06); }}
        .legend-item.dimmed {{ opacity:0.25; }}
        .legend-dot {{ width:10px; height:10px; border-radius:50%; margin-right:6px; flex-shrink:0; }}

        #statsBar {{
            position:fixed; bottom:12px; left:14px; z-index:9999;
            background:rgba(12,12,12,0.9); backdrop-filter:blur(12px);
            border:1px solid #222; border-radius:8px;
            padding:8px 14px; color:#666; font-size:11px;
            display:flex; gap:14px;
        }}
        .sv {{ color:#eee; font-weight:600; }}
    </style>
</head>
<body>

<div id="mynetwork"></div>

<div id="loadingBar">
    <div style="color:#2196F3;font-size:16px;font-weight:600;margin-bottom:14px;">Opening Knowledge Graph</div>
    <div class="loader-track"><div class="loader-bar" id="loaderBar"></div></div>
    <div class="loader-text" id="loaderText">Initializing...</div>
</div>

<div id="searchBox">
    <input id="searchInput" type="text" placeholder="Search entities...">
    <button id="searchBtn">Go</button>
</div>

<div id="panel">
    <div class="panel-section">
        <div class="panel-title">Entity Types (click to filter)</div>
        {legend_types}
    </div>
    <div class="panel-section">
        <div class="panel-title">Top Relationships</div>
        {legend_edges}
    </div>
    <div class="panel-section">
        <div style="color:#666;font-size:10px;margin-top:4px;">
            <span style="color:#4488ff;">&#9679;</span> Wikidata edge
            <span style="color:#555;margin-left:6px;">&#9679;</span> Text edge
        </div>
    </div>
</div>

<div id="statsBar">
    <div>Nodes <span class="sv">{stats['nodes']}</span></div>
    <div>Edges <span class="sv">{stats['edges']}</span></div>
    <div>Wikidata <span class="sv">{stats.get('wd_triples',0)}</span></div>
    <div>Communities <span class="sv">{stats['communities']}</span></div>
</div>

<script>
var allNodes={nodes_json};
var allEdges={edges_json};
var nodeDS=new vis.DataSet(allNodes);
var edgeDS=new vis.DataSet(allEdges);
var network;
var hiddenTypes=new Set();

function drawGraph(){{
    var container=document.getElementById('mynetwork');
    var options={{
        nodes:{{ shape:"dot",borderWidth:1.5,shadow:{{enabled:true,size:3}},
            font:{{color:"#fff",face:"Inter,system-ui,sans-serif"}} }},
        edges:{{ smooth:{{type:"continuous"}},width:0.5,
            font:{{size:0,color:"#666"}} }},
        interaction:{{ hover:true,tooltipDelay:100,hideEdgesOnDrag:true,
            hideEdgesOnZoom:true }},
        physics:{{ solver:"forceAtlas2Based",
            forceAtlas2Based:{{ gravitationalConstant:-35,centralGravity:0.005,
                springLength:130,springConstant:0.05,damping:0.4 }},
            stabilization:{{ enabled:true,iterations:300,updateInterval:20 }} }}
    }};
    network=new vis.Network(container,{{nodes:nodeDS,edges:edgeDS}},options);

    // 🔎 Focus mode — show only neighborhood
    var focusMode = false;

    network.on("click", function(params) {{
        if (params.nodes.length === 0) {{
            // Reset view if clicking background
            if (focusMode) {{
                nodeDS.update(allNodes.map(n => ({{id:n.id, hidden:false}})));
                edgeDS.update(allEdges.map(e => ({{id:e.id, hidden:false}})));
                focusMode = false;
            }}
            return;
        }}

        var nodeId = params.nodes[0];
        var connected = network.getConnectedNodes(nodeId);
        connected.push(nodeId);

        var updates = [];
        allNodes.forEach(function(n){{
            updates.push({{
                id: n.id,
                hidden: connected.indexOf(n.id) === -1
            }});
        }});
        nodeDS.update(updates);

        var edgeUpdates = [];
        allEdges.forEach(function(e){{
            edgeUpdates.push({{
                id: e.id,
                hidden: connected.indexOf(e.from) === -1 ||
                        connected.indexOf(e.to) === -1
            }});
        }});
        edgeDS.update(edgeUpdates);

        focusMode = true;
    }});

    network.on("stabilizationProgress",function(p){{
        var pct=Math.round(p.iterations/p.total*100);
        document.getElementById('loaderBar').style.width=pct+'%';
        document.getElementById('loaderText').innerText='Stabilizing... '+pct+'%';
    }});
    network.once("stabilizationIterationsDone",function(){{
        document.getElementById('loaderBar').style.width='100%';
        document.getElementById('loaderText').innerText='Done!';
        setTimeout(function(){{
            document.getElementById('loadingBar').style.opacity=0;
            setTimeout(function(){{document.getElementById('loadingBar').style.display='none';}},500);
        }},200);
    }});

    // Show edge labels on hover
    network.on("hoverEdge",function(p){{
        edgeDS.update({{id:p.edge,font:{{size:11}}}});
    }});
    network.on("blurEdge",function(p){{
        edgeDS.update({{id:p.edge,font:{{size:0}}}});
    }});
}}
drawGraph();

// Search
document.getElementById('searchBtn').onclick=function(){{
    var q=document.getElementById('searchInput').value.trim().toLowerCase();
    if(!q)return;
    var found=allNodes.find(function(n){{return n.label.toLowerCase()===q;}});
    if(!found) found=allNodes.find(function(n){{return n.label.toLowerCase().indexOf(q)!==-1;}});
    if(found){{ network.focus(found.id,{{scale:1.8,animation:true}}); network.selectNodes([found.id]); }}
    else{{ document.getElementById('searchInput').style.borderColor='#ff5555';
        setTimeout(function(){{document.getElementById('searchInput').style.borderColor='#333';}},800); }}
}};
document.getElementById('searchInput').addEventListener('keydown',function(e){{
    if(e.key==='Enter')document.getElementById('searchBtn').click();
}});

// Type filter
document.querySelectorAll('.legend-item').forEach(function(el){{
    el.addEventListener('click',function(){{
        var type=this.dataset.type;
        if(hiddenTypes.has(type)){{hiddenTypes.delete(type);this.classList.remove('dimmed');}}
        else{{hiddenTypes.add(type);this.classList.add('dimmed');}}
        var visibleIds=new Set();
        var updates=[];
        allNodes.forEach(function(n){{
            var hidden=hiddenTypes.has(n.group);
            updates.push({{id:n.id,hidden:hidden}});
            if(!hidden)visibleIds.add(n.id);
        }});
        nodeDS.update(updates);
        var eu=[];
        allEdges.forEach(function(e){{
            eu.push({{id:e.id,hidden:!visibleIds.has(e.from)||!visibleIds.has(e.to)}});
        }});
        edgeDS.update(eu);
    }});
}});
</script>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  HTML: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="kshn - Wikidata-First",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python kshn.py -i input.html                    # Wikidata relationships only
  python kshn.py -i input.html --text-edges        # + text-based mention edges
  python kshn.py -i input.html --all               # everything
  python kshn.py -i input.html -o my_graph.html    # custom output name
""")
    parser.add_argument('-i', '--input', required=True, help='Input HTML encyclopedia file')
    parser.add_argument('-o', '--output', help='Output HTML file (default: <input>_KG.html)')
    parser.add_argument('--text-edges', action='store_true', help='Add text-based mention edges')
    parser.add_argument('--cooccur', action='store_true', help='Add co-occurrence edge weights')
    parser.add_argument('--categories', action='store_true', help='Fetch Wikipedia category hierarchy')
    parser.add_argument('--all', action='store_true', help='Enable all features')
    parser.add_argument('--graphml', action='store_true', help='Export GraphML for Gephi/Cytoscape')
    parser.add_argument('--color-by', choices=['type', 'community'], default='type', help='Node coloring scheme')
    args = parser.parse_args()

    if args.all:
        args.text_edges = args.cooccur = args.categories = True

    input_file = Path(args.input)
    base = input_file.stem
    output_path = args.output if args.output else str(input_file.with_name(f"{base}_KG.html"))

    # 1. Parse
    print(f"[1/8] Parsing {args.input}...")
    soup = load_html(args.input)
    entries = extract_entries(soup)
    print(f"  {len(entries)} entries")

    # 2. Deduplicate
    print(f"[2/8] Deduplicating...")
    entries, term_to_id = deduplicate_entries(entries)
    qids = [e.qid for e in entries if e.qid]
    print(f"  {len(entries)} unique ({len(qids)} QIDs)")

    # 3. Wikidata relationships
    print(f"[3/8] Wikidata relationships...")
    rels_cache = str(Path(args.input).with_name(f"{base}.wikidata_rels.json"))
    triples = fetch_wikidata_graph(set(qids), cache_path=rels_cache)

    # 4. Entity types
    print(f"[4/8] Entity types...")
    types_cache = str(Path(args.input).with_name(f"{base}.wikidata_types.json"))
    type_cache = fetch_entity_types(qids, cache_path=types_cache)
    typed = sum(1 for q in qids if q in type_cache)
    print(f"  {typed}/{len(qids)} typed")

    # 5. Build graph
    print(f"[5/8] Building graph...")
    G = build_wikidata_graph(entries, triples, type_cache)
    print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges (Wikidata)")

    if args.text_edges:
        text_added = add_text_edges(G, entries, term_to_id)
        print(f"  +{text_added} text edges -> {G.number_of_edges()} total")

    # 6. Co-occurrence
    if args.cooccur:
        print(f"[6/8] Co-occurrence analysis...")
        pairs, cooc_added = compute_cooccurrence(entries, term_to_id, G)
        print(f"  {pairs} co-occurring pairs, {cooc_added} new edges")
    else:
        print(f"[6/8] Skipping co-occurrence (use --cooccur)")

    # 7. Category hierarchy
    if args.categories:
        print(f"[7/8] Category hierarchy...")
        cat_cache_path = str(Path(args.input).with_name(f"{base}.wiki_categories.json"))
        cat_nodes, cat_edges = fetch_categories(entries, G, cache_path=cat_cache_path)
        print(f"  +{cat_nodes} category nodes, +{cat_edges} taxonomy edges")
    else:
        print(f"[7/8] Skipping categories (use --categories)")

    # 8. Communities + export
    print(f"[8/8] Communities + export...")
    num_communities = detect_communities(G)
    print(f"  {num_communities} communities")

    stats = {
        'title': base, 'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges(), 'communities': num_communities,
        'wd_triples': len(triples),
    }
    # Determine adaptive coloring: if < 10% of nodes have QIDs, fallback to community coloring
    color_by = args.color_by
    if color_by == 'type' and len(entries) > 0:
        qid_coverage = len(qids) / len(entries)
        if qid_coverage < 0.1:
            print(f"  ⚠️ Low QID coverage ({qid_coverage:.1%}). Falling back to community coloring.")
            color_by = 'community'

    vis_nodes, vis_edges, type_counts, edge_labels = generate_vis_data(G, color_by=color_by)
    save_html(vis_nodes, vis_edges, type_counts, edge_labels, stats, output_path)

    if args.graphml:
        export_graphml(G, str(Path(output_path).with_suffix('.graphml')))

    print(f"\nDone! Open {output_path} in your browser.")
    print(f"  Wikidata triples: {len(triples)}")
    print(f"  Top edges: {', '.join(f'{k}({v})' for k,v in sorted(edge_labels.items(), key=lambda x:-x[1])[:8])}")


if __name__ == "__main__":
    main()
