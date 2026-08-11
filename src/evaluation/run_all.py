import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.recommender import generate_candidates
from src.ranking.focus import rank_focus
from src.ranking.energy import rank_energy
from src.ranking.inspiration import rank_inspiration
from src.evaluation.precision import precision_at_k
from src.evaluation.diversity import intra_list_diversity
from src.evaluation.mood_match import mood_match

N_USERS = 60
users = list(range(N_USERS))

rows = []
for u in users:
    c = generate_candidates(u)
    if c.empty:
        continue
    base = c.sort_values("hybrid_score", ascending=False)
    f = rank_focus(c)
    e = rank_energy(c)
    i = rank_inspiration(c)
    rows.append({
        "prec_base": precision_at_k(base, u), "prec_focus": precision_at_k(f, u),
        "prec_energy": precision_at_k(e, u), "prec_insp": precision_at_k(i, u),
        "ild_base": intra_list_diversity(base), "ild_focus": intra_list_diversity(f),
        "ild_energy": intra_list_diversity(e), "ild_insp": intra_list_diversity(i),
        "mm_focus_on_focus": mood_match(f, "focus"), "mm_base_on_focus": mood_match(base, "focus"),
        "mm_energy_on_energy": mood_match(e, "energy"), "mm_base_on_energy": mood_match(base, "energy"),
    })

df = pd.DataFrame(rows)
print("Evaluated", len(df), "users")
means = df.mean()
means.to_csv("results/evaluation_results.csv")
print("\nMean results:")
print(means.round(3).to_string())

# Chart 1: Precision@10 by mode
plt.figure(figsize=(8,5))
vals = [means["prec_base"], means["prec_focus"], means["prec_energy"], means["prec_insp"]]
plt.bar(["Baseline","Focus","Energy","Inspiration"], vals, color=["gray","steelblue","coral","seagreen"])
plt.ylabel("Precision@10"); plt.title("Precision@10 by Mode (avg over %d users)" % len(df))
plt.tight_layout(); plt.savefig("results/eval_precision.png", dpi=120); plt.close()

# Chart 2: Intra-List Diversity by mode
plt.figure(figsize=(8,5))
vals = [means["ild_base"], means["ild_focus"], means["ild_energy"], means["ild_insp"]]
plt.bar(["Baseline","Focus","Energy","Inspiration"], vals, color=["gray","steelblue","coral","seagreen"])
plt.ylabel("Intra-List Diversity"); plt.title("Diversity by Mode (avg over %d users)" % len(df))
plt.tight_layout(); plt.savefig("results/eval_diversity.png", dpi=120); plt.close()

# Chart 3: Mood-Match - each mode vs baseline on its own target
plt.figure(figsize=(8,5))
labels = ["Focus target","Energy target"]
base_vals = [means["mm_base_on_focus"], means["mm_base_on_energy"]]
mode_vals = [means["mm_focus_on_focus"], means["mm_energy_on_energy"]]
x = np.arange(len(labels)); w = 0.35
plt.bar(x - w/2, base_vals, w, label="Baseline", color="gray")
plt.bar(x + w/2, mode_vals, w, label="Mode-aware", color="mediumpurple")
plt.xticks(x, labels); plt.ylabel("Mood-Match (cosine)")
plt.title("Mode-Appropriateness: Mode-aware vs Baseline (avg over %d users)" % len(df))
plt.legend(); plt.tight_layout(); plt.savefig("results/eval_mood_match.png", dpi=120); plt.close()

print("\nSaved: eval_precision.png, eval_diversity.png, eval_mood_match.png + evaluation_results.csv")
