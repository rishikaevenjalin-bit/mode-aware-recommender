import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import pickle

print("Loading music...")
music = pd.read_csv("data/processed/music_clean.csv").reset_index(drop=True)
print("Tracks:", music.shape[0])

features = ["danceability", "energy", "speechiness", "acousticness",
            "instrumentalness", "valence", "tempo"]

scaler = MinMaxScaler()
feature_matrix = scaler.fit_transform(music[features])
print("Feature matrix shape:", feature_matrix.shape)

with open("data/processed/content_model.pkl", "wb") as f:
    pickle.dump({"feature_matrix": feature_matrix, "scaler": scaler,
                 "features": features, "track_ids": music["track_id"].tolist()}, f)
print("Saved content model.")

seed = 0
sims = cosine_similarity([feature_matrix[seed]], feature_matrix)[0]
top = np.argsort(sims)[::-1][1:6]
print("Seed track:", music.iloc[seed]["name"], "by", music.iloc[seed]["artist"])
print("Most similar by audio features:")
for i in top:
    sim_val = round(float(sims[i]), 3)
    print(" -", music.iloc[i]["name"], "by", music.iloc[i]["artist"], "sim", sim_val)
