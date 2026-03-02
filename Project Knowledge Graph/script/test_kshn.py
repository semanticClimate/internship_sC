import pytest
import os
import networkx as nx
from bs4 import BeautifulSoup
from unittest.mock import MagicMock, patch
from kshn import (
    Entity, Triple, normalize_key, deduplicate_entries, 
    extract_entries, compute_cooccurrence, generate_vis_data
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. UNIT TESTS: DATA MODELS
# ─────────────────────────────────────────────────────────────────────────────

def test_entity_creation():
    e = Entity(id="1", term="Test", qid="Q123", wiki_url="url", description="desc")
    assert e.id == "1"
    assert e.term == "Test"
    assert e.to_dict()["qid"] == "Q123"

def test_triple_to_dict():
    t = Triple(subject="S", subjectLabel="SL", predicate="P", predicateId="P1", object="O", objectLabel="OL")
    d = t.to_dict()
    assert d["subject"] == "S"
    assert d["predicateId"] == "P1"

# ─────────────────────────────────────────────────────────────────────────────
# 2. UNIT TESTS: EXTRACTION & LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def test_normalize_key():
    assert normalize_key("  Hello  World  ") == "hello world"
    assert normalize_key("Python-3.0!") == "python-3.0!"
    assert normalize_key("") == ""

def test_extract_entries():
    html = """
    <div role="ami_entry" term="Term 1" wikidataid="Q1" wikipedia_url="url1">
        <p>This is a description for Term 1. It is longer than 5 characters.</p>
        <p><a href="url2" title="Rel">Link Text</a></p>
    </div>
    <div role="ami_entry" wikidataid="Q2"><b>Term 2</b></div>
    """
    soup = BeautifulSoup(html, "html.parser")
    entries = extract_entries(soup)
    
    assert len(entries) == 2
    assert entries[0].term == "Term 1"
    assert entries[0].qid == "Q1"
    assert "description for Term 1" in entries[0].description
    assert entries[1].term == "Term 2" # Extracted from <b>
    assert entries[1].qid == "Q2"

def test_deduplicate_entries():
    e1 = Entity(id="Q1", term="Apple", qid="Q1", wiki_url="url1", description="desc1")
    e2 = Entity(id="apple-id", term="apple", qid="Q1", wiki_url="url1", description="desc2_longer") # Duplicate QID
    e3 = Entity(id="Q3", term="Banana", qid="Q3", wiki_url="url3", description="desc3")
    
    deduped_list, term_to_id = deduplicate_entries([e1, e2, e3])
    
    assert len(deduped_list) == 2
    # Ensure the entry with longer description is kept (e2)
    ids = [e.id for e in deduped_list]
    assert "apple-id" in ids
    assert "Q3" in ids
    
    # Check term mapping
    assert term_to_id["Apple"] == "apple-id"
    assert term_to_id["apple"] == "apple-id"
    assert term_to_id["Q1"] == "apple-id"

# ─────────────────────────────────────────────────────────────────────────────
# 3. UNIT TESTS: GRAPH LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def test_compute_cooccurrence():
    # Setup entities with cross-references in paragraphs
    e1 = Entity(id="id1", term="A", qid="Q1", wiki_url="u1", description="d1", para_groups=[["B", "B"]]) 
    e2 = Entity(id="id2", term="B", qid="Q2", wiki_url="u2", description="d2", para_groups=[["A", "A"]])
    
    G = nx.DiGraph()
    G.add_node("id1", label="A")
    G.add_node("id2", label="B")
    
    term_to_id = {"A": "id1", "B": "id2"}
    
    # Note: compute_cooccurrence adds edge only if count >= 2
    # Here, e1's para has 2 'B's, so pair (id1, id2) count will be 2
    _, added = compute_cooccurrence([e1, e2], term_to_id, G)
    
    assert G.has_edge("id1", "id2") or G.has_edge("id2", "id1")
    assert added >= 1

def test_generate_vis_data():
    G = nx.DiGraph()
    G.add_node("n1", label="Node 1", node_type="Type A", qid="Q1", wiki_url="u1", description="d1")
    G.add_node("n2", label="Node 2", node_type="Type B", qid="Q2", wiki_url="u2", description="d2")
    G.add_edge("n1", "n2", label="relates to", source="wikidata")
    
    nodes, edges, type_counts, edge_labels = generate_vis_data(G)
    
    assert len(nodes) == 2
    assert len(edges) == 1
    assert nodes[0]["id"] == "n1"
    assert type_counts["Type A"] == 1
    assert edge_labels["relates to"] == 1

# ─────────────────────────────────────────────────────────────────────────────
# 4. INTEGRATION TEST: END-TO-END (Minimal)
# ─────────────────────────────────────────────────────────────────────────────

def test_full_pipeline_minimal():
    html = """
    <div role="ami_entry" term="Sun" wikidataid="Q10"><b>Sun</b><p>A star.</p></div>
    <div role="ami_entry" term="Earth" wikidataid="Q11"><b>Earth</b><p>A planet near the Sun.</p></div>
    """
    soup = BeautifulSoup(html, "html.parser")
    entries = extract_entries(soup)
    deduped_list, term_to_id = deduplicate_entries(entries)
    
    G = nx.DiGraph()
    for e in deduped_list:
        G.add_node(e.id, label=e.term, qid=e.qid, wiki_url=e.wiki_url, description=e.description, node_type="Concept")
    
    # Force a co-occurrence by manually adding para_groups that match
    # Script adds edge if count >= 2. Each entry's para_groups are checked.
    # We add the same pair into two different paragraphs for id1 ("Sun").
    deduped_list[0].para_groups = [["Earth"], ["Earth"]] 
    
    compute_cooccurrence(deduped_list, term_to_id, G)
    
    nodes, edges, _, _ = generate_vis_data(G)
    
    assert len(nodes) == 2
    assert len(edges) == 1
    assert "co-occurs" in edges[0]["title"].lower()
