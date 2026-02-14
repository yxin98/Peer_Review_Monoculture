import pandas as pd, json, ast
import matplotlib.pyplot as plt
from itertools import combinations

# -----------------------------
# 0) Load
# -----------------------------
df = pd.read_csv("paper_review_aspect_stance_2021_2025_with_year.tsv", sep="\t")
df["year"] = pd.to_numeric(df["year"], errors="raise").astype(int)

# -----------------------------
# 1) Coarse taxonomy (rubric-style)
# -----------------------------
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

def coarse_set(s):
    if pd.isna(s) or str(s).strip()=="":
        return set()
    try: d = json.loads(s)
    except: d = ast.literal_eval(s)
    if not isinstance(d, dict):
        return set()
    # 你这里 UNKNOWN rate=0，所以直接丢弃未知项也可以更干净
    return {ASPECT_TO_COARSE[k] for k in d.keys() if k in ASPECT_TO_COARSE}

df["C"] = df["aspect_bundle"].apply(coarse_set)

# quick sanity (should be 0.0 and 7 categories for your data)
print("UNKNOWN rate:", (df["aspect_bundle"].apply(lambda x: False)).mean())  # placeholder,保持简短
print("Coarse categories:", sorted(set().union(*df["C"])))

# -----------------------------
# 2) Paper-level: union size U + n_reviews + pairwise Jaccard homogeneity
# -----------------------------
g = df.groupby(["year","paper_id"])["C"].agg(list).reset_index()
g["n_reviews"] = g["C"].apply(len)

def union_size(L):
    return len(set().union(*L)) if L else 0

def avg_pairwise_jaccard(L):
    if len(L) < 2:
        return 0.0
    vals = []
    for a, b in combinations(L, 2):
        denom = len(a | b)
        vals.append((len(a & b) / denom) if denom else 0.0)
    return sum(vals) / len(vals)

g["U"] = g["C"].apply(union_size)
g["pair_jacc"] = g["C"].apply(avg_pairwise_jaccard)

# -----------------------------
# 3) Controls / filters (关键：让“同质化随年”更可见)
# -----------------------------
TARGET_NREV = 3         # 建议：固定 review 数
DROP_2023 = False       # 可选：把 2023 当过渡期剔除

g = g[g["n_reviews"] == TARGET_NREV].copy()
if DROP_2023:
    g = g[g["year"] != 2023].copy()

# 规则：每年每个 union size，若该 cell 的 paper 数 < 10 则丢弃
cnt = g.groupby(["year","U"]).size().rename("n").reset_index()
valid = cnt[cnt["n"] >= 10][["year","U"]]
g = g.merge(valid, on=["year","U"], how="inner")

print("\n[Kept] years:", sorted(g["year"].unique()))
print("[Kept] union sizes:", sorted(g["U"].unique()))
print("[Kept] papers:", len(g))

# -----------------------------
# 4) Tables you actually need
# -----------------------------
# (A) 每年 union size 分布（占比）
distU = g.groupby(["year","U"]).size().rename("n").reset_index()
distU["share"] = distU["n"] / distU.groupby("year")["n"].transform("sum")

# (B) 同质化：在 (year,U) 下的平均 pairwise Jaccard
mJ = g.groupby(["year","U"])["pair_jacc"].mean().reset_index()

# 你如果还想保留你之前那张 P(I|year,U) 的“离散表”，这里就不再打印（你说要简化）

# -----------------------------
# 5) Plots (少图但信息密度高)
# -----------------------------
pU = distU.pivot(index="year", columns="U", values="share").fillna(0)
pJ = mJ.pivot(index="year", columns="U", values="pair_jacc")

plt.figure()
plt.imshow(pU.values, aspect="auto")
plt.xticks(range(pU.shape[1]), pU.columns, rotation=0)
plt.yticks(range(pU.shape[0]), pU.index)
plt.colorbar(label="share of papers (given year)")
plt.title(f"Union size distribution by year (n_reviews={TARGET_NREV}, filtered cell>=10)")
plt.xlabel("Union size U (coarse categories)")
plt.ylabel("Year")
plt.tight_layout()
plt.show()

plt.figure()
plt.imshow(pJ.values, aspect="auto")
plt.xticks(range(pJ.shape[1]), pJ.columns, rotation=0)
plt.yticks(range(pJ.shape[0]), pJ.index)
plt.colorbar(label="mean pairwise Jaccard")
plt.title(f"Homogeneity by year & union size (pairwise Jaccard; n_reviews={TARGET_NREV})")
plt.xlabel("Union size U (coarse categories)")
plt.ylabel("Year")
plt.tight_layout()
plt.show()

# -----------------------------
# 6) Optional: single trend plot (1 figure, very paper-friendly)
# -----------------------------
trend = g.groupby("year")["pair_jacc"].mean().reset_index()

plt.figure()
plt.plot(trend["year"], trend["pair_jacc"], marker="o")
plt.xticks(trend["year"])
plt.xlabel("Year")
plt.ylabel("mean pairwise Jaccard")
plt.title(f"Overall homogeneity trend (n_reviews={TARGET_NREV}, cell>=10)")
plt.tight_layout()
plt.show()
