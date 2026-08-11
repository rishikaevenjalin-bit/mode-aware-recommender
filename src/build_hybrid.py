import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

print("Loading models...")
with open("data/processed/als_model.pkl", "rb") as f:
    cf = pickle.load(f)
with open("data/processed/content_model.pkl", "rb") as f:
    cb = pickle.load(f)
music = pd.read_csv("data/processed/music_clean.csv").reset_index(drop=True)

model = cf["model"]
matrix = cf["matrix"]
track_map = cf["track_map"]
feat = cb["feature_matrix"]
content_track_ids = cb["track_ids"]

# track_id -> row index in content feature matrix
cid_to_row = {tid: i for i, tid in enumerate(content_track_ids)}

def normalize(x):
    x = np.asarray(x, dtype=float)
    if x.max() - x.min() < 1e-9:
        return np.zeros_like(x)
    return (x - x.min()) / (x.max() - x.min())

def hybrid_recommend(user_idx, alpha=0.5, n=10):
    # CF scores for all tracks for this user
    cf_ids, cf_scores = model.recommend(user_idx, matrix[user_idx], N=500, filter_already_liked_items=False)
    # Build user taste profile: average audio features of tracks they played
    played = matrix[user_idx].indices
    played_tids = [track_map[i] for i in played]
    played_rows = [cid_to_row[t] for t in played_tids if t in cid_to_row]
    if not played_rows:
        print("No audio features for this user\047s tracks.")
        return
    user_profile = feat[played_rows].mean(axis=0)
    # Content score for each CF candidate
    cand_tids = [track_map[i] for i in cf_ids]
    cand_rows = [cid_to_row.get(t, None) for t in cand_tids]
    content_scores = []
    for r in cand_rows:
        if r is None:
            content_scores.append(0.0)
        else:
            content_scores.append(cosine_similarity([user_profile], [feat[r]])[0][0])
    cf_n = normalize(cf_scores)
    ct_n = normalize(content_scores)
    hybrid = alpha * cf_n + (1 - alpha) * ct_n
    order = np.argsort(hybrid)[::-1][:n]
    print("Top hybrid recommendations (alpha=" + str(alpha) + "):")
    for o in order:
        tid = cand_tids[o]
        row = music[music["track_id"] == tid]
        if not row.empty:
            print(" -", row.iloc[0]["name"], "by", row.iloc[0]["artist"])

hybrid_recommend(0, alpha=0.5, n=10)
