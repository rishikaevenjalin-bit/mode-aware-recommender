import numpy as np

# Energy rewards high-arousal, upbeat, positive tracks.
ENERGY_WEIGHTS = {
    "energy": 0.40,
    "tempo": 0.25,
    "valence": 0.25,
    "danceability": 0.10,
}

def energy_score(df):
    score = np.zeros(len(df))
    for feat, w in ENERGY_WEIGHTS.items():
        score += w * df[feat].values
    return score

def rank_energy(df, mode_weight=0.6):
    d = df.copy()
    es = energy_score(d)
    if es.max() - es.min() > 1e-9:
        es = (es - es.min()) / (es.max() - es.min())
    else:
        es = np.zeros_like(es)
    d["energy_mode_score"] = es
    d["final_score"] = mode_weight * d["energy_mode_score"] + (1 - mode_weight) * d["hybrid_score"]
    return d.sort_values("final_score", ascending=False).reset_index(drop=True)

if __name__ == "__main__":
    from src.recommender import generate_candidates
    cands = generate_candidates(0)
    ranked = rank_energy(cands)
    print("Top 10 ENERGY recommendations for user 0:")
    cols = ["name", "artist", "energy", "tempo", "valence", "final_score"]
    print(ranked[cols].head(10).to_string())
