import pandas as pd

print("Loading data...")
music = pd.read_csv("data/raw/Music Info.csv")
hist = pd.read_csv("data/raw/User Listening History.csv")
print("Loaded:", music.shape, hist.shape)

music = music.dropna(subset=["track_id", "name", "artist"])
music = music.drop_duplicates(subset="track_id")
print("Music after clean:", music.shape)

hist = hist[hist["track_id"].isin(music["track_id"])]
print("History after matching:", hist.shape)

user_counts = hist["user_id"].value_counts()
active_users = user_counts[user_counts >= 20].index
hist = hist[hist["user_id"].isin(active_users)]

track_counts = hist["track_id"].value_counts()
popular_tracks = track_counts[track_counts >= 50].index
hist = hist[hist["track_id"].isin(popular_tracks)]
print("History after filtering:", hist.shape)
print("Users:", hist["user_id"].nunique(), "Tracks:", hist["track_id"].nunique())

music = music[music["track_id"].isin(hist["track_id"])]
print("Final music:", music.shape)

music.to_csv("data/processed/music_clean.csv", index=False)
hist.to_csv("data/processed/interactions_clean.csv", index=False)
print("Saved.")
