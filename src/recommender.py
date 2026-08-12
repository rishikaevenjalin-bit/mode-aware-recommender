import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load everything once at import
import os
_cf = None
if os.path.exists("data/processed/als_model.pkl"):
    with open("data/processed/als_model.pkl", "rb") as f:
        _cf = pickle.load(f)
with open("data/processed/content_model.pkl", "rb") as f:
    _cb = pickle.load(f)
_music = pd.read_csv("data/processed/music_clean.csv").reset_index(drop=True)

_model = _cf["model"]
_matrix = _cf["matrix"]
_track_map = _cf["track_map"]
_feat = _cb["feature_matrix"]
_cid_to_row = {tid: i for i, tid in enumerate(_cb["track_ids"])}
_features = _cb["features"]

def _normalize(x):
    x = np.asarray(x, dtype=float)
    if x.max() - x.min() < 1e-9:
        return np.zeros_like(x)
    return (x - x.min()) / (x.max() - x.min())

def generate_candidates(user_idx, alpha=0.5, n_candidates=150):
    """Return a DataFrame of candidate tracks with hybrid score and audio features."""
    cf_ids, cf_scores = _model.recommend(
        user_idx, _matrix[user_idx], N=n_candidates * 3,
        filter_already_liked_items=False)

    played = _matrix[user_idx].indices
    played_tids = [_track_map[i] for i in played]
    played_rows = [_cid_to_row[t] for t in played_tids if t in _cid_to_row]
    if not played_rows:
        return pd.DataFrame()
    user_profile = _feat[played_rows].mean(axis=0)

    cand_tids = [_track_map[i] for i in cf_ids]
    rows, cf_keep, content = [], [], []
    for tid, cfs in zip(cand_tids, cf_scores):
        r = _cid_to_row.get(tid)
        if r is None:
            continue
        rows.append(tid)
        cf_keep.append(cfs)
        content.append(cosine_similarity([user_profile], [_feat[r]])[0][0])

    cf_n = _normalize(cf_keep)
    ct_n = _normalize(content)
    hybrid = alpha * cf_n + (1 - alpha) * ct_n

    df = pd.DataFrame({"track_id": rows, "hybrid_score": hybrid})
    df = df.drop_duplicates(subset="track_id")
    df = df.merge(_music, on="track_id", how="left")
    df = df.dropna(subset=_features)
    df = df.sort_values("hybrid_score", ascending=False).head(n_candidates)
    return df.reset_index(drop=True)
    print(cands[["name", "artist", "hybrid_score"]].head(10).to_string())


def generate_candidates_from_artists(seed_artists, n_candidates=150):
    """Cold-start: build a taste profile from chosen artists, return candidate pool.
    Used for new app visitors who have no listening history."""
    # Find all tracks by the seed artists
    seed_rows = _music[_music["artist"].isin(seed_artists)]
    if seed_rows.empty:
        return pd.DataFrame()

    # Build taste profile: average audio features of seed artists' tracks
    seed_track_ids = seed_rows["track_id"].tolist()
    seed_feat_rows = [_cid_to_row[t] for t in seed_track_ids if t in _cid_to_row]
    if not seed_feat_rows:
        return pd.DataFrame()
    user_profile = _feat[seed_feat_rows].mean(axis=0)

    # Score every track by similarity to the taste profile
    sims = cosine_similarity([user_profile], _feat)[0]

    df = _music.copy().reset_index(drop=True)
    # align sims to music rows via track_id order in content model
    sim_by_tid = {tid: sims[i] for i, tid in enumerate(_cb["track_ids"])}
    df["hybrid_score"] = df["track_id"].map(sim_by_tid).fillna(0.0)

    # Drop the seed artists' own tracks so we recommend NEW music, not their picks
    df = df[~df["artist"].isin(seed_artists)]
    df = df.dropna(subset=_features)
    df = df.sort_values("hybrid_score", ascending=False).head(n_candidates)
    return df.reset_index(drop=True)


if __name__ == "__main__":
    print("\nCold-start test - seed artists: Radiohead, Coldplay")
    c = generate_candidates_from_artists(["Radiohead", "Coldplay"])
    print("Generated", len(c), "candidates")
    print(c[["name", "artist", "hybrid_score"]].head(10).to_string())
