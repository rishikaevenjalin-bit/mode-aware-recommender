import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

FEATURES = ["danceability", "energy", "speechiness", "acousticness",
            "instrumentalness", "valence", "tempo"]

# Target profiles per mode (0-1 scaled feature space).
# Order: danceability, energy, speechiness, acousticness, instrumentalness, valence, tempo
TARGETS = {
    "focus":  np.array([0.3, 0.15, 0.1, 0.8, 0.8, 0.3, 0.4]),
    "energy": np.array([0.8, 0.9,  0.3, 0.1, 0.1, 0.8, 0.8]),
    "inspiration": None,  # acclaim-based, not a pure audio target
}

def _scale(df):
    X = df[FEATURES].values.astype(float)
    # scale using fixed known feature ranges (0-1 features already; tempo needs /250)
    X = X.copy()
    X[:, 6] = X[:, 6] / 250.0  # tempo to ~0-1
    return X

def mood_match(ranked_df, target_name, k=10):
    """Cosine similarity between the top-k recommendation centroid and a mode target."""
    if TARGETS.get(target_name) is None:
        return None
    top = ranked_df.head(k)
    X = _scale(top)
    centroid = X.mean(axis=0).reshape(1, -1)
    target = TARGETS[target_name].reshape(1, -1)
    return float(cosine_similarity(centroid, target)[0][0])

if __name__ == "__main__":
    from src.recommender import generate_candidates
    from src.ranking.focus import rank_focus
    from src.ranking.energy import rank_energy

    users = [0, 5, 10, 15, 20]
    print("Mood-Match: each mode scored against each target (avg over users)")
    print("Proof = each mode should win on its OWN target.\n")

    focus_on_focus, focus_on_energy = [], []
    energy_on_focus, energy_on_energy = [], []
    base_on_focus, base_on_energy = [], []

    for u in users:
        c = generate_candidates(u)
        if c.empty:
            continue
        base = c.sort_values("hybrid_score", ascending=False)
        f = rank_focus(c)
        e = rank_energy(c)
        focus_on_focus.append(mood_match(f, "focus"))
        focus_on_energy.append(mood_match(f, "energy"))
        energy_on_focus.append(mood_match(e, "focus"))
        energy_on_energy.append(mood_match(e, "energy"))
        base_on_focus.append(mood_match(base, "focus"))
        base_on_energy.append(mood_match(base, "energy"))

    def avg(x): return sum(x) / len(x)
    print(f"{'ranking':>10} {'vs FOCUS target':>16} {'vs ENERGY target':>17}")
    print(f"{'baseline':>10} {avg(base_on_focus):>16.3f} {avg(base_on_energy):>17.3f}")
    print(f"{'focus':>10} {avg(focus_on_focus):>16.3f} {avg(focus_on_energy):>17.3f}")
    print(f"{'energy':>10} {avg(energy_on_focus):>16.3f} {avg(energy_on_energy):>17.3f}")
