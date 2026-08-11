import numpy as np

# Focus rewards concentration-friendly audio: instrumental, acoustic, calm, low speech.
# Weights are a starting point (domain knowledge); tune via ablation later.
FOCUS_WEIGHTS = {
    "instrumentalness": 0.35,
    "acousticness": 0.25,
    "energy": -0.25,
    "speechiness": -0.15,
}

def focus_score(df):
    """Compute a 0-based Focus score from audio features (df already scaled 0-1 in features)."""
    score = np.zeros(len(df))
    for feat, w in FOCUS_WEIGHTS.items():
        score += w * df[feat].values
    return score

def rank_focus(df, mode_weight=0.6):
    """Re-rank candidate pool for Focus mode.
    mode_weight balances Focus signal vs personal hybrid score."""
    d = df.copy()
    fs = focus_score(d)
    # normalize focus score to 0-1 for fair blending
    if fs.max() - fs.min() > 1e-9:
        fs = (fs - fs.min()) / (fs.max() - fs.min())
    else:
        fs = np.zeros_like(fs)
    d["focus_score"] = fs
    d["final_score"] = mode_weight * d["focus_score"] + (1 - mode_weight) * d["hybrid_score"]
    return d.sort_values("final_score", ascending=False).reset_index(drop=True)

if __name__ == "__main__":
    from src.recommender import generate_candidates
    cands = generate_candidates(0)
    ranked = rank_focus(cands)
    print("Top 10 FOCUS recommendations for user 0:")
    cols = ["name", "artist", "instrumentalness", "energy", "final_score"]
    print(ranked[cols].head(10).to_string())
