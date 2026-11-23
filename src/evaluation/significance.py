import numpy as np
from scipy.stats import wilcoxon

from src.recommender import generate_candidates
from src.ranking.focus import rank_focus
from src.ranking.energy import rank_energy
from src.evaluation.mood_match import mood_match

N_USERS = 60
f_mode, f_base, e_mode, e_base = [], [], [], []

for u in range(N_USERS):
    c = generate_candidates(u)
    if c.empty:
        continue
    base = c.sort_values("hybrid_score", ascending=False)
    f_mode.append(mood_match(rank_focus(c), "focus"))
    f_base.append(mood_match(base, "focus"))
    e_mode.append(mood_match(rank_energy(c), "energy"))
    e_base.append(mood_match(base, "energy"))

f_mode, f_base = np.array(f_mode), np.array(f_base)
e_mode, e_base = np.array(e_mode), np.array(e_base)
print(f"Users evaluated: {len(f_mode)}")

wf, pf = wilcoxon(f_mode, f_base)
print("\nFOCUS mode-aware vs baseline (focus target):")
print(f"  mean: mode-aware={f_mode.mean():.3f}  baseline={f_base.mean():.3f}  diff=+{f_mode.mean()-f_base.mean():.3f}")
print(f"  Wilcoxon W={wf:.1f}, p={pf:.2e}")

we, pe = wilcoxon(e_mode, e_base)
print("\nENERGY mode-aware vs baseline (energy target):")
print(f"  mean: mode-aware={e_mode.mean():.3f}  baseline={e_base.mean():.3f}  diff=+{e_mode.mean()-e_base.mean():.3f}")
print(f"  Wilcoxon W={we:.1f}, p={pe:.2e}")
