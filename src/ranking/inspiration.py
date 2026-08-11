import pandas as pd

_acclaim = pd.read_csv("data/processed/acclaim_scores.csv")[["artist", "acclaim_score"]]

def rank_inspiration(df, mode_weight=0.5):
    d = df.copy()
    # Attach acclaim score by artist; artists not in acclaim data get 0
    d = d.merge(_acclaim, on="artist", how="left")
    d["acclaim_score"] = d["acclaim_score"].fillna(0.0)
    d["final_score"] = mode_weight * d["acclaim_score"] + (1 - mode_weight) * d["hybrid_score"]
    return d.sort_values("final_score", ascending=False).reset_index(drop=True)

if __name__ == "__main__":
    from src.recommender import generate_candidates
    cands = generate_candidates(0)
    ranked = rank_inspiration(cands)
    print("Top 10 INSPIRATION recommendations for user 0:")
    cols = ["name", "artist", "acclaim_score", "hybrid_score", "final_score"]
    print(ranked[cols].head(10).to_string())
