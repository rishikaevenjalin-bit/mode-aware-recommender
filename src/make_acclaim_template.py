import pandas as pd

music = pd.read_csv("data/processed/music_clean.csv")

# Top 150 artists by track count (the ones users will actually encounter)
top_artists = music["artist"].value_counts().head(150).index.tolist()

template = pd.DataFrame({
    "artist": top_artists,
    "grammy_wins": 0,
    "grammy_noms": 0,
    "metacritic": 0,
    "rolling_stone": 0,
})

template.to_csv("data/raw/acclaim_template.csv", index=False)
print("Created acclaim_template.csv with", len(template), "artists")
print("\nColumns:")
print("  grammy_wins   - number of Grammy wins (integer)")
print("  grammy_noms   - number of Grammy nominations (integer)")
print("  metacritic    - average Metacritic critic score 0-100 (0 if unknown)")
print("  rolling_stone - number of appearances on RS greatest lists (integer)")
print("\nFirst 20 artists to fill:")
print(template["artist"].head(20).to_string())
