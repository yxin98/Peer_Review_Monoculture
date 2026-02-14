import pandas as pd, json, ast
import matplotlib.pyplot as plt

PATH = "paper_review_aspect_stance_2021_2025_with_year.tsv"

ASPECT_TO_COARSE = {
    "Motivation / Problem Framing": "Contribution & Positioning",
    "Originality / Novelty": "Contribution & Positioning",
    "Fit to Venue / Scope": "Contribution & Positioning",
    "Problem Setup Validity": "Contribution & Positioning",
    "Technical Correctness": "Technical Quality",
    "Technical Novelty": "Technical Quality",
    "Experimental Setup & Protocol": "Empirical Evidence",
    "Baselines & Fair Comparison": "Empirical Evidence",
    "Data / Dataset Appropriateness": "Empirical Evidence",
    "Metrics & Evaluation Criteria": "Empirical Evidence",
    "Statistical Evidence": "Empirical Evidence",
    "Ablation & Attribution": "Empirical Evidence",
    "Hyperparameter / Seed Sensitivity": "Empirical Evidence",
    "Distribution Shift & Generalization (OOD)": "Empirical Evidence",
    "Interpretation of Results": "Result Analysis",
    "Reproducibility & Implementation": "Reproducibility & Practicality",
    "Efficiency & Scalability": "Reproducibility & Practicality",
    "Writing Clarity & Organization": "Presentation",
    "Figures / Tables & Visual Presentation": "Presentation",
    "Related Work Positioning & Citations": "Presentation",
    "Ethics / Safety / Misuse": "Responsibility",
    "Societal / Broader Impacts": "Responsibility",
}

df = pd.read_csv(PATH, sep="\t")
df["year"] = pd.to_numeric(df["year"], errors="raise").astype(int)

def parse_keys(s):
    if pd.isna(s) or str(s).strip()=="":
        return set()
    try: d = json.loads(s)
    except: d = ast.literal_eval(s)
    return set(d.keys()) if isinstance(d, dict) else set()

df["fine_set"] = df["aspect_bundle"].apply(parse_keys)
df["coarse_set"] = df["fine_set"].apply(lambda S: {ASPECT_TO_COARSE[a] for a in S if a in ASPECT_TO_COARSE})

paper = df.groupby(["year","paper_id"]).agg(
    fine_union=("fine_set", lambda L: set().union(*L)),
    coarse_union=("coarse_set", lambda L: set().union(*L)),
).reset_index()

paper["Uf"] = paper["fine_union"].apply(len)
paper["Uc"] = paper["coarse_union"].apply(len)

def plot_union_share(paper, ucol, title):
    dist = paper.groupby(["year", ucol]).size().rename("n").reset_index()
    dist["share"] = dist["n"] / dist.groupby("year")["n"].transform("sum")
    pivot = dist.pivot(index="year", columns=ucol, values="share").fillna(0).sort_index()
    xs = pivot.index.to_list()
    cols = pivot.columns.to_list()
    ys = [pivot[c].values for c in cols]

    plt.figure()
    plt.stackplot(xs, ys, labels=cols)
    plt.xticks(xs)
    plt.ylim(0, 1)
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Share of papers")
    plt.legend(title="Union size", ncol=4, fontsize=8)
    plt.tight_layout()
    plt.show()

plot_union_share(paper, "Uc", "Coarse: share by union size over years")
plot_union_share(paper, "Uf", "Fine: share by union size over years")
