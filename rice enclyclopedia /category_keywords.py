import pandas as pd
import os

CATEGORY_RULES = {
    "Crop & Plant": [
        "rice", "paddy", "crop", "plant"
    ],

    "Varieties & Cultivars": [ 
        "variety", "varieties", "cultivar", "hybrid"
    ],

    "Germplasm & Genetic Resources": [
        "germplasm", "landrace", "accession"
    ],

    "Genetics & Genomics": [
        "gene", "genome", "genotype", "genotypes",
        "dna", "rna", "allele"
    ],

    "Plant Breeding": [
        "breeding", "breeder", "cross"
    ],

    "Yield & Productivity": [
        "yield", "productivity"
    ],

    "Grain Quality & Nutrition": [
        "protein", "amylose", "starch",
        "nutrition", "quality", "glycemic"
    ],

    "Physiology": [
        "photosynthesis", "chlorophyll",
        "catalase", "peroxidase",
        "transpiration"
    ],

    "Morphological Traits": [
        "plant height",
        "panicle",
        "root",
        "leaf",
        "tiller",
        "grain length",
        "grain width"
    ],

    "Growth & Development": [
        "germination",
        "flowering",
        "maturity",
        "seedling"
    ],

    "Abiotic Stress": [
        "drought",
        "salinity",
        "heat",
        "cold",
        "flood",
        "submergence",
        "stress"
    ],

    "Biotic Stress": [
        "biotic"
    ],

    "Diseases": [
        "blast",
        "blight",
        "smut",
        "bakanae",
        "brown spot",
        "disease",
        "sheath blight"
    ],

    "Insect Pests": [
        "stem borer",
        "leaf folder",
        "planthopper",
        "gall midge",
        "pest"
    ],

    "Biocontrol": [
        "trichoderma",
        "parasitoid",
        "amf"
    ],

    "Crop Protection": [
        "fungicide",
        "herbicide",
        "pesticide",
        "imidacloprid"
    ],

    "Weed Management": [
        "weed",
        "weeding"
    ],

    "Nutrient Management": [
        "nitrogen",
        "fertilizer",
        "phosphorus",
        "potassium"
    ],

    "Agronomy": [
        "cultivation",
        "farming",
        "agronomy",
        "cropping"
    ],

    "Water Management": [
        "water",
        "irrigation"
    ],

    "Climate & Environment": [
        "climate",
        "environment",
        "ecosystem",
        "sustainability"
    ],

    "Food & Processing": [
        "bran",
        "parboiling",
        "cooking",
        "food"
    ],

    "Economics & Policy": [
        "economics",
        "profit",
        "market",
        "policy",
        "msp"
    ],

    "Institutions": [
        "nrri",
        "crri",
        "icar",
        "kvk",
        "aicrip"
    ],

    "Research & Education": [
        "research",
        "training",
        "student"
    ],

    "Geography": [
        "india",
        "assam",
        "odisha",
        "bihar"
    ],

    "Seed Science": [
        "seed"
    ],

    "Ecology & Biodiversity": [
        "biodiversity",
        "ecology"
    ]
}

def assign_category(keyword):

    keyword = str(keyword).lower()

    for category, words in CATEGORY_RULES.items():

        for word in words:

            if word in keyword:
                return category

    return "Miscellaneous"

df = pd.read_csv("Master_Keywords.csv")

df = df.dropna(subset=["keyword"])

df = df.drop_duplicates(subset=["keyword"])

df["Category"] = df["keyword"].apply(assign_category)

os.makedirs("output", exist_ok=True)

output_file = "output/Encyclopedia_Categorized.csv"

df.to_csv(output_file, index=False)

print("=" * 50)
print("Finished Successfully")
print(f"Total Keywords : {len(df)}")
print(f"Saved File : {output_file}")
print("=" * 50)
