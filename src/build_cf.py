import pandas as pd
import numpy as np
import scipy.sparse as sparse
from implicit.als import AlternatingLeastSquares
import pickle

print("Loading interactions...")
hist = pd.read_csv("data/processed/interactions_clean.csv")
print("Rows:", hist.shape[0])

# Map user_id and track_id to integer indices for the matrix
hist["user_idx"] = hist["user_id"].astype("category").cat.codes
hist["track_idx"] = hist["track_id"].astype("category").cat.codes

# Save the mappings (idx -> real id) for later use
user_map = dict(enumerate(hist["user_id"].astype("category").cat.categories))
track_map = dict(enumerate(hist["track_id"].astype("category").cat.categories))

# Build sparse matrix: rows = users, cols = tracks, values = playcount
n_users = hist["user_idx"].nunique()
n_tracks = hist["track_idx"].nunique()
matrix = sparse.csr_matrix(
    (hist["playcount"].astype(float), (hist["user_idx"], hist["track_idx"])),
    shape=(n_users, n_tracks),
)
print("Matrix shape:", matrix.shape)

# Train ALS
print("Training ALS model...")
model = AlternatingLeastSquares(factors=50, regularization=0.01, iterations=15)
model.fit(matrix)
print("Training done.")

# Save model, matrix, and maps
with open("data/processed/als_model.pkl", "wb") as f:
    pickle.dump({"model": model, "matrix": matrix, "user_map": user_map, "track_map": track_map}, f)
print("Saved model to data/processed/als_model.pkl")

# Sanity check: recommend 5 tracks for user index 0
music = pd.read_csv("data/processed/music_clean.csv")
ids, scores = model.recommend(0, matrix[0], N=5)
print("\nSample recommendations for user 0:")
for i in ids:
    tid = track_map[i]
    row = music[music["track_id"] == tid]
    if not row.empty:
        print(" -", row.iloc[0]["name"], "by", row.iloc[0]["artist"])
