import streamlit as st
import pandas as pd

from src.recommender import generate_candidates_from_artists
from src.ranking.focus import rank_focus
from src.ranking.energy import rank_energy
from src.ranking.inspiration import rank_inspiration
from src.explanation.explain import explain
from src.db.database import init_db, new_session_id, save_session

st.set_page_config(page_title="MusicIntent", page_icon="music", layout="centered")
init_db()

@st.cache_data
def load_artists():
    music = pd.read_csv("data/processed/music_clean.csv")
    return music["artist"].value_counts().index.tolist()

artists = load_artists()
RANKERS = {"Focus": rank_focus, "Energy": rank_energy, "Inspiration": rank_inspiration}

if "step" not in st.session_state:
    st.session_state.step = "setup"
    st.session_state.seed_artists = []
    st.session_state.mode = None
    st.session_state.recs = None
    st.session_state.session_id = new_session_id()

# --- SCREEN 1: Setup ---
if st.session_state.step == "setup":
    st.title("MusicIntent")
    st.write("Music recommendations that adapt to how you want to listen.")

    st.subheader("1. Pick a few artists you like")
    chosen = st.multiselect(
        "Choose 3-5 artists to build your taste profile:",
        options=artists, default=st.session_state.seed_artists, max_selections=5,
    )
    st.subheader("2. How do you want to listen?")
    mode = st.radio(
        "Select a mode:",
        options=["Focus", "Energy", "Inspiration"],
        captions=["Deep work, low distraction", "High tempo, motivation", "Acclaimed music, discovery"],
        index=None,
    )
    if st.button("Get recommendations", type="primary"):
        if len(chosen) < 1:
            st.error("Please pick at least one artist.")
        elif mode is None:
            st.error("Please select a mode.")
        else:
            st.session_state.seed_artists = chosen
            st.session_state.mode = mode
            with st.spinner("Building your recommendations..."):
                cands = generate_candidates_from_artists(chosen)
                ranked = RANKERS[mode](cands)
                st.session_state.recs = ranked.head(8).to_dict("records")
            st.session_state.step = "results"
            st.rerun()

# --- SCREEN 2: Results ---
elif st.session_state.step == "results":
    st.title(f"Your {st.session_state.mode} recommendations")
    st.caption("Based on: " + ", ".join(st.session_state.seed_artists))

    for i, track in enumerate(st.session_state.recs, 1):
        with st.container(border=True):
            st.markdown(f"**{i}. {track['name']}** - {track['artist']}")
            cols = st.columns(3)
            cols[0].metric("Energy", f"{track['energy']:.2f}")
            cols[1].metric("Tempo", f"{track['tempo']:.0f}")
            cols[2].metric("Valence", f"{track['valence']:.2f}")
            st.info(explain(track, st.session_state.mode))

    if st.button("Rate this session", type="primary"):
        st.session_state.step = "feedback"
        st.rerun()

# --- SCREEN 3: Feedback ---
elif st.session_state.step == "feedback":
    st.title("Rate your session")
    st.caption(f"Mode: {st.session_state.mode}")

    relevance = st.slider("How relevant were the recommendations?", 1, 5, 3)
    mode_fit = st.slider("Did they suit your chosen mode?", 1, 5, 3)
    expl = st.slider("Were the explanations useful?", 1, 5, 3)
    comment = st.text_area("Any comments? (optional)")

    if st.button("Submit feedback", type="primary"):
        save_session(
            st.session_state.session_id, st.session_state.mode,
            st.session_state.seed_artists, st.session_state.recs,
            relevance, mode_fit, expl, comment,
        )
        st.session_state.step = "done"
        st.rerun()

# --- SCREEN 4: Done ---
elif st.session_state.step == "done":
    st.title("Thank you!")
    st.success("Your feedback has been saved.")
    st.balloons()
    if st.button("Start a new session"):
        for k in ["step", "seed_artists", "mode", "recs", "session_id"]:
            st.session_state.pop(k, None)
        st.rerun()
