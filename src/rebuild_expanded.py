import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle

FEATURES = ["danceability", "energy", "speechiness", "acousticness",
            "instrumentalness", "valence", "tempo"]

print("Loading expanded data...")
m = pd.read_csv("data/processed/music_expanded.csv", low_memory=False)
print("Before filtering:", len(m))

# Remove non-music categories that produce odd recommendations
non_music = ["comedy", "study", "sleep", "ambient", "children", "disney", "kids"]
m = m[~m["genre"].astype(str).str.lower().isin(non_music)]
m = m.dropna(subset=["name", "artist"] + FEATURES).drop_duplicates(subset="track_id")
m = m.reset_index(drop=True)
print("After filtering:", len(m))

# Save the cleaned expanded music file
m.to_csv("data/processed/music_expanded_clean.csv", index=False)

# Rebuild content model on expanded data
scaler = MinMaxScaler()
feature_matrix = scaler.fit_transform(m[FEATURES])
with open("data/processed/content_model_expanded.pkl", "wb") as f:
    pickle.dump({"feature_matrix": feature_matrix, "scaler": scaler,
                 "features": FEATURES, "track_ids": m["track_id"].tolist()}, f)
print("Saved expanded content model.")
print("Final track count:", len(m), "| Artists:", m["artist"].nunique())
