import pandas as pd
import glob

REMOVE_WORDS = {
    "india",
    "indian",
    "research",
    "report",
    "annual report",
    "activity",
    "activities",
    "programme",
    "program",
    "project",
    "projects",
    "development",
    "developed",
    "institute",
    "national",
    "average",
    "year",
    "years",
    "paper",
    "papers",
    "study",
    "studies",
    "icar",
    "nrri",
    "cuttack",
    "odisha"
}

REPLACE_DICT = {

    "rice variety":"rice varieties",
    "rice varieties":"rice varieties",

    "rice cultivar":"rice varieties",
    "rice cultivars":"rice varieties",

    "rice genotype":"rice genotypes",
    "rice genotypes":"rice genotypes",
    "genotype":"rice genotypes",
    "genotypes":"rice genotypes",

    "blast disease":"rice blast",
    "rice blast disease":"rice blast",

    "brown spot disease":"brown spot",

    "false smut disease":"false smut",

    "bacterial blight disease":"bacterial blight",

    "climate resilient rice":"climate resilience",

    "climate smart rice":"climate resilience",

    "hybrid rice":"rice hybrids",
    "rice hybrid":"rice hybrids"
}

files = glob.glob("*_keywords.csv")

all_data = []

for file in files:

    print(f"Reading : {file}")

    df = pd.read_csv(file)

    if "keyword" not in df.columns:
        print(f"Skipping {file} (keyword column missing)")
        continue

    # Count column check
    if "count" not in df.columns:
        df["count"] = 1

    # Lowercase
    df["keyword"] = (
        df["keyword"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df = df[df["keyword"] != ""]

    df = df[df["keyword"].str.len() >= 3]

    df = df[~df["keyword"].isin(REMOVE_WORDS)]

    df["keyword"] = df["keyword"].replace(REPLACE_DICT)

    all_data.append(df)

master = pd.concat(all_data, ignore_index=True)

master = (
    master
    .groupby("keyword", as_index=False)["count"]
    .sum()
)

master = master.sort_values(
    by="count",
    ascending=False
)

master.to_csv(
    "Master_Keywords.csv",
    index=False
)

print("\nDone ✅")
print("Total Unique Keywords :", len(master))
print("Saved as Master_Keywords.csv")