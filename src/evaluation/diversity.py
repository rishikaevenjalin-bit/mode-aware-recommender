import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

FEATURES = ["danceability", "energy", "speechiness", "acousticness",
            "instrumentalness", "valence", "tempo"]

def intra_list_diversity(ranked_df, k=10):
    """Average pairwise Euclidean distance among top-k tracks in audio-feature space."""
    top = ranked_df.head(k)
    if len(top) < 2:
        return 0.0
    X = top[FEATURES].values
    # normalize each feature column 0-1 so tempo doesn't dominate
    mins = X.min(axis=0)
    ranges = X.max(axis=0) - mins
    ranges[ranges < 1e-9] = 1.0
    Xn = (X - mins) / ranges
    dists = euclidean_distances(Xn)
    n = len(top)
    total = dists.sum() / 2.0
    pairs = n * (n - 1) / 2.0
    return total / pairs

if __name__ == "__main__":
    from src.recommender import generate_candidates
    from src.ranking.focus import rank_focus
    from src.ranking.energy import rank_energy
    from src.ranking.inspiration import rank_inspiration

    users = [0, 5, 10, 15, 20]
    print("Intra-List Diversity@10 across", len(users), "users:")
    print(f"{'user':>5} {'baseline':>9} {'focus':>7} {'energy':>7} {'inspir':>7}")
    for u in users:
        c = generate_candidates(u)
        if c.empty:
            continue
        base = intra_list_diversity(c.sort_values("hybrid_score", ascending=False))
        f = intra_list_diversity(rank_focus(c))
        e = intra_list_diversity(rank_energy(c))
        i = intra_list_diversity(rank_inspiration(c))
        print(f"{u:>5} {base:>9.3f} {f:>7.3f} {e:>7.3f} {i:>7.3f}")
