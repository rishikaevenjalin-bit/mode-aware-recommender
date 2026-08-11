import pandas as pd
import numpy as np

# Locked weights (proposal): Grammy 30%, Metacritic 40%, Rolling Stone 30%
W_GRAMMY = 0.30
W_METACRITIC = 0.40
W_ROLLINGSTONE = 0.30

def _norm(s):
    s = s.astype(float)
    if s.max() - s.min() < 1e-9:
        return s * 0.0
    return (s - s.min()) / (s.max() - s.min())

def build_acclaim_scores(path="data/raw/acclaim_data.csv", out="data/processed/acclaim_scores.csv"):
    df = pd.read_csv(path)
    df["grammy_signal"] = df["grammy_wins"] * 2 + df["grammy_noms"]
    g = _norm(df["grammy_signal"])
    m = _norm(df["metacritic"])
    r = _norm(df["rolling_stone"])
    df["acclaim_score"] = W_GRAMMY * g + W_METACRITIC * m + W_ROLLINGSTONE * r
    df.to_csv(out, index=False)
    return df

if __name__ == "__main__":
    df = build_acclaim_scores()
    print("Acclaim scores built for", len(df), "artists.")
    print("\nTop 15 by acclaim score:")
    top = df.sort_values("acclaim_score", ascending=False).head(15)
    print(top[["artist", "grammy_wins", "metacritic", "rolling_stone", "acclaim_score"]].to_string(index=False))
