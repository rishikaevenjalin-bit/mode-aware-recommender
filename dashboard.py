"""
MusicIntent — Feedback Dashboard
Run with:  streamlit run dashboard.py
Reads the same music_rec.db the main app writes to, so you can see every
session rating and every per-track like/dislike in one place.
"""

import json
import pandas as pd
import streamlit as st

from src.db.database import (
    init_db,
    init_track_feedback,
    get_all_sessions,
    get_all_track_feedback,
)

st.set_page_config(page_title="MusicIntent · Feedback", page_icon="♫", layout="wide")

# Make sure both tables exist even on a fresh database.
init_db()
init_track_feedback()

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='margin-bottom:0'>♫ MusicIntent — Feedback Dashboard</h1>"
    "<p style='color:#6b6790;margin-top:4px'>Everything collected from the app: "
    "session ratings, written comments, and per-track likes & dislikes.</p>",
    unsafe_allow_html=True,
)

sessions = get_all_sessions()
tracks = get_all_track_feedback()

sdf = pd.DataFrame(sessions)
tdf = pd.DataFrame(tracks)

if sdf.empty and tdf.empty:
    st.info("No feedback has been collected yet. Run the main app, complete a "
            "session, and give some 👍 / 👎 — then refresh this page.")
    st.stop()

# ── Top-line numbers ────────────────────────────────────────────────────────
likes = int((tdf["feedback"].str.lower() == "like").sum()) if not tdf.empty else 0
dislikes = int((tdf["feedback"].str.lower() == "dislike").sum()) if not tdf.empty else 0
total_tf = len(tdf)
like_rate = f"{(likes / total_tf * 100):.0f}%" if total_tf else "—"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sessions completed", len(sdf))
c2.metric("Track ratings", total_tf)
c3.metric("👍 Likes", likes)
c4.metric("Like rate", like_rate, help="Share of track ratings that were likes")

# ── Average session ratings ─────────────────────────────────────────────────
if not sdf.empty:
    st.subheader("Average session ratings (1–5)")
    rating_cols = ["rating_relevance", "rating_mode_fit", "rating_explanation"]
    labels = {"rating_relevance": "Relevance",
              "rating_mode_fit": "Mode fit",
              "rating_explanation": "Explanation quality"}
    have = [c for c in rating_cols if c in sdf.columns]
    r1 = st.columns(len(have))
    for col, box in zip(have, r1):
        vals = pd.to_numeric(sdf[col], errors="coerce").dropna()
        box.metric(labels[col], f"{vals.mean():.2f}" if len(vals) else "—")

    # per-mode averages
    if "mode" in sdf.columns:
        st.caption("By mode")
        by_mode = (sdf.assign(**{c: pd.to_numeric(sdf[c], errors="coerce") for c in have})
                      .groupby("mode")[have]
                      .mean()
                      .rename(columns=labels)
                      .round(2))
        st.dataframe(by_mode, use_container_width=True)

# ── Likes / dislikes by mode ────────────────────────────────────────────────
if not tdf.empty and "mode" in tdf.columns:
    st.subheader("Likes & dislikes by mode")
    pivot = (tdf.assign(feedback=tdf["feedback"].str.lower())
                .pivot_table(index="mode", columns="feedback",
                             values="track_name", aggfunc="count", fill_value=0))
    for col in ["like", "dislike"]:
        if col not in pivot.columns:
            pivot[col] = 0
    pivot = pivot.rename(columns={"like": "👍 Likes", "dislike": "👎 Dislikes"})
    st.bar_chart(pivot[["👍 Likes", "👎 Dislikes"]])

# ── Most-liked / most-disliked tracks ───────────────────────────────────────
if not tdf.empty:
    tdf["label"] = tdf["track_name"].fillna("?") + " — " + tdf["artist"].fillna("?")
    fb = tdf.assign(feedback=tdf["feedback"].str.lower())
    left, right = st.columns(2)
    with left:
        st.subheader("Most liked")
        ml = fb[fb["feedback"] == "like"]["label"].value_counts().head(10)
        ml_df = pd.DataFrame({"Track": ml.index, "👍": ml.values})
        st.dataframe(ml_df, use_container_width=True, hide_index=True)
    with right:
        st.subheader("Most disliked")
        md = fb[fb["feedback"] == "dislike"]["label"].value_counts().head(10)
        md_df = pd.DataFrame({"Track": md.index, "👎": md.values})
        st.dataframe(md_df, use_container_width=True, hide_index=True)

# ── Written comments ────────────────────────────────────────────────────────
if not sdf.empty and "comment" in sdf.columns:
    comments = sdf[sdf["comment"].fillna("").str.strip() != ""]
    st.subheader(f"Written comments ({len(comments)})")
    if comments.empty:
        st.caption("No written comments yet.")
    else:
        for _, row in comments.sort_values("timestamp", ascending=False).iterrows():
            ts = str(row.get("timestamp", ""))[:16].replace("T", " ")
            st.markdown(
                f"> {row['comment']}  \n"
                f"<span style='color:#8a86a8;font-size:0.85em'>"
                f"{row.get('mode','')} · {ts}</span>",
                unsafe_allow_html=True,
            )

# ── Raw tables (expanders) ──────────────────────────────────────────────────
with st.expander("All sessions (raw)"):
    if not sdf.empty:
        show = sdf.copy()
        for c in ["seed_artists", "recommendations"]:
            if c in show.columns:
                show[c] = show[c].apply(
                    lambda v: ", ".join(json.loads(v)) if isinstance(v, str)
                    and v.startswith("[") else v)
        st.dataframe(show.sort_values("timestamp", ascending=False)
                     if "timestamp" in show.columns else show,
                     use_container_width=True, hide_index=True)

with st.expander("All track feedback (raw)"):
    if not tdf.empty:
        cols = [c for c in ["timestamp", "mode", "track_name", "artist", "feedback",
                            "session_id"] if c in tdf.columns]
        st.dataframe(tdf[cols].sort_values("timestamp", ascending=False)
                     if "timestamp" in tdf.columns else tdf[cols],
                     use_container_width=True, hide_index=True)

# ── Download everything ─────────────────────────────────────────────────────
st.subheader("Export")
d1, d2 = st.columns(2)
if not sdf.empty:
    d1.download_button("Download sessions CSV", sdf.to_csv(index=False),
                       "sessions.csv", "text/csv")
if not tdf.empty:
    d2.download_button("Download track feedback CSV", tdf.to_csv(index=False),
                       "track_feedback.csv", "text/csv")
