import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

print("Loading data...")
music = pd.read_csv("data/processed/music_clean.csv")
hist = pd.read_csv("data/processed/interactions_clean.csv")

print("Tracks:", music.shape[0])
print("Interactions:", hist.shape[0])
print("Users:", hist["user_id"].nunique())
print("Artists:", music["artist"].nunique())

features = ["danceability", "energy", "speechiness", "acousticness",
            "instrumentalness", "valence", "tempo"]

# 1. Audio feature distributions
fig, axes = plt.subplots(2, 4, figsize=(18, 8))
for ax, feat in zip(axes.flatten(), features):
    sns.histplot(music[feat], bins=40, ax=ax, color="steelblue")
    ax.set_title(feat)
axes.flatten()[-1].axis("off")
plt.tight_layout()
plt.savefig("results/audio_feature_distributions.png", dpi=120)
plt.close()
print("Saved: audio_feature_distributions.png")

# 2. Top 15 artists by track count
top_artists = music["artist"].value_counts().head(15)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_artists.values, y=top_artists.index, color="coral")
plt.title("Top 15 Artists by Track Count")
plt.xlabel("Number of tracks")
plt.tight_layout()
plt.savefig("results/top_artists.png", dpi=120)
plt.close()
print("Saved: top_artists.png")

# 3. Track popularity (how many users played each track)
track_pop = hist["track_id"].value_counts()
plt.figure(figsize=(10, 6))
sns.histplot(track_pop.values, bins=50, color="seagreen")
plt.title("Track Popularity Distribution (listeners per track)")
plt.xlabel("Number of listeners")
plt.ylabel("Number of tracks")
plt.tight_layout()
plt.savefig("results/track_popularity.png", dpi=120)
plt.close()
print("Saved: track_popularity.png")

# 4. User activity (how many tracks each user played)
user_act = hist["user_id"].value_counts()
plt.figure(figsize=(10, 6))
sns.histplot(user_act.values, bins=50, color="mediumpurple")
plt.title("User Activity Distribution (tracks per user)")
plt.xlabel("Number of tracks played")
plt.ylabel("Number of users")
plt.tight_layout()
plt.savefig("results/user_activity.png", dpi=120)
plt.close()
print("Saved: user_activity.png")

# 5. Feature correlation heatmap
plt.figure(figsize=(9, 7))
corr = music[features].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Audio Feature Correlations")
plt.tight_layout()
plt.savefig("results/feature_correlations.png", dpi=120)
plt.close()
print("Saved: feature_correlations.png")

# 6. Tracks per year
if "year" in music.columns:
    year_counts = music["year"].value_counts().sort_index()
    year_counts = year_counts[year_counts.index > 1950]
    plt.figure(figsize=(12, 5))
    sns.lineplot(x=year_counts.index, y=year_counts.values, color="darkorange")
    plt.title("Tracks per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of tracks")
    plt.tight_layout()
    plt.savefig("results/tracks_per_year.png", dpi=120)
    plt.close()
    print("Saved: tracks_per_year.png")

print("EDA complete. Charts in results/")
