import numpy as np
import pandas as pd

acclaim_full = pd.read_csv("data/processed/acclaim_scores.csv")[["artist", "acclaim_score"]]

def avg_acclaim_of_top(ranked_df, k=10):
    """Mean acclaim score of the top-k recommended tracks' artists."""
    top = ranked_df.head(k).merge(acclaim_full, on="artist", how="left")
    return top["acclaim_score_y"].fillna(0).mean() if "acclaim_score_y" in top else top["acclaim_score"].fillna(0).mean()

if __name__ == "__main__":
    from src.recommender import generate_candidates
    from src.ranking.inspiration import rank_inspiration

    users = [0, 5, 10, 15, 20]

    print("=" * 60)
    print("ABLATION 1: Does acclaim improve Inspiration? (RQ3)")
    print("Metric: avg acclaim of top-10 recommended artists")
    print("=" * 60)
    print(f"{'user':>5} {'no acclaim (hybrid only)':>26} {'with acclaim':>14}")
    no_acc, with_acc = [], []
    for u in users:
        c = generate_candidates(u)
        if c.empty:
            continue
        # no acclaim = pure hybrid ranking (mode_weight 0)
        base = rank_inspiration(c, mode_weight=0.0)
        insp = rank_inspiration(c, mode_weight=0.5)
        b = base.head(10)["acclaim_score"].fillna(0).mean()
        i = insp.head(10)["acclaim_score"].fillna(0).mean()
        no_acc.append(b); with_acc.append(i)
        print(f"{u:>5} {b:>26.3f} {i:>14.3f}")
    print(f"{'AVG':>5} {np.mean(no_acc):>26.3f} {np.mean(with_acc):>14.3f}")
    lift = np.mean(with_acc) - np.mean(no_acc)
    print(f"\nAcclaim lift: +{lift:.3f} ({100*lift/max(np.mean(no_acc),0.001):.0f}% more acclaimed)")

    print("\n" + "=" * 60)
    print("ABLATION 2: Weight sensitivity")
    print("avg acclaim of top-10 under different mode_weights")
    print("=" * 60)
    print(f"{'user':>5} {'w=0.0':>7} {'w=0.3':>7} {'w=0.5':>7} {'w=0.7':>7}")
    for u in users:
        c = generate_candidates(u)
        if c.empty:
            continue
        vals = []
        for w in [0.0, 0.3, 0.5, 0.7]:
            r = rank_inspiration(c, mode_weight=w)
            vals.append(r.head(10)["acclaim_score"].fillna(0).mean())
        print(f"{u:>5} {vals[0]:>7.3f} {vals[1]:>7.3f} {vals[2]:>7.3f} {vals[3]:>7.3f}")
