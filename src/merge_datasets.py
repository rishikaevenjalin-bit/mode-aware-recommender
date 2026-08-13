import pandas as pd

FEATURES = ["danceability", "energy", "speechiness", "acousticness",
            "instrumentalness", "valence", "tempo"]

print("Loading existing data...")
existing = pd.read_csv("data/processed/music_clean.csv")
print("Existing tracks:", len(existing))

print("Loading new 114k dataset...")
new = pd.read_csv("data/raw/spotify_114k.csv")
print("New dataset tracks:", len(new))

# Rename new dataset columns to match existing schema
new = new.rename(columns={
    "track_name": "name",
    "artists": "artist",
    "track_genre": "genre",
})

# Keep only columns we need (that exist in both)
keep = ["track_id", "name", "artist", "genre", "year", "popularity"] + FEATURES
# 'year' may not exist in new data; keep what's available
new_cols = [c for c in keep if c in new.columns]
new = new[new_cols].copy()

# Drop rows missing critical fields
new = new.dropna(subset=["name", "artist"] + FEATURES)
new = new.drop_duplicates(subset=["name", "artist"])
print("New after cleaning:", len(new))

# Dedupe against existing: build a normalized key (lowercase artist+name)
def key(df):
    return (df["artist"].str.lower().str.strip() + " ::: " +
            df["name"].str.lower().str.strip())

existing_keys = set(key(existing))
new["_key"] = key(new)
new_unique = new[~new["_key"].isin(existing_keys)].drop(columns="_key")
print("New unique tracks (not already in existing):", len(new_unique))

# Merge: existing + new unique. Align columns.
combined = pd.concat([existing, new_unique], ignore_index=True, sort=False)
combined = combined.drop_duplicates(subset="track_id", keep="first")
print("Combined total tracks:", len(combined))

# Save expanded dataset (original stays untouched)
combined.to_csv("data/processed/music_expanded.csv", index=False)
print("Saved data/processed/music_expanded.csv")
print("\nGenre breakdown (top 10):")
print(combined["genre"].value_counts().head(10).to_string())
