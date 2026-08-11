import numpy as np
import pandas as pd
import pickle

with open("data/processed/als_model.pkl", "rb") as f:
    _cf = pickle.load(f)
_matrix = _cf["matrix"]
_track_map = _cf["track_map"]

def precision_at_k(ranked_df, user_idx, k=10):
    """Fraction of top-k recommended tracks that are in the user's actual played set."""
    played_cols = set(_matrix[user_idx].indices)
    played_tids = set(_track_map[i] for i in played_cols)
    top_k = ranked_df.head(k)["track_id"].tolist()
    if not top_k:
        return 0.0
    hits = sum(1 for t in top_k if t in played_tids)
    return hits / len(top_k)

if __name__ == "__main__":
    from src.recommender import generate_candidates
    from src.ranking.focus import rank_focus
    from src.ranking.energy import rank_energy
    from src.ranking.inspiration import rank_inspiration

    users = [0, 5, 10, 15, 20]
    print("Precision@10 across", len(users), "users:")
    print(f"{'user':>5} {'baseline':>9} {'focus':>7} {'energy':>7} {'inspir':>7}")
    for u in users:
        c = generate_candidates(u)
        if c.empty:
            continue
        base = precision_at_k(c.sort_values("hybrid_score", ascending=False), u)
        f = precision_at_k(rank_focus(c), u)
        e = precision_at_k(rank_energy(c), u)
        i = precision_at_k(rank_inspiration(c), u)
        print(f"{u:>5} {base:>9.3f} {f:>7.3f} {e:>7.3f} {i:>7.3f}")
