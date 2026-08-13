import streamlit as st
import pandas as pd

from src.recommender import generate_candidates_from_artists
from src.ranking.focus import rank_focus
from src.ranking.energy import rank_energy
from src.ranking.inspiration import rank_inspiration
from src.explanation.explain import explain
from src.db.database import init_db, new_session_id, save_session, init_track_feedback, save_track_feedback
import html

def song_card(rank, track, artist, energy, tempo, valence, explanation, spotify_id=None):
    import urllib.parse as _up
    _q = _up.quote(f"{track} {artist}")
    _yurl = f"https://www.youtube.com/results?search_query={_q}"
    _surl = f"https://open.spotify.com/search/{_q}"
    _sl = (f'<div style="margin-top:10px;">'
           f'<a href="{_surl}" target="_blank" style="display:inline-block;padding:6px 14px;border-radius:999px;background:#1DB954;color:#fff;text-decoration:none;font-size:0.8rem;font-weight:700;margin-right:8px;">Listen on Spotify</a>'
           f'<a href="{_yurl}" target="_blank" style="display:inline-block;padding:6px 14px;border-radius:999px;background:#FF0000;color:#fff;text-decoration:none;font-size:0.8rem;font-weight:700;">Listen on YouTube</a>'
           f'</div>')
    st.markdown(f"""<div class="mi-song">
  <div class="mi-song-top">
    <div class="mi-rank">{rank}</div>
    <div class="mi-song-main">
      <div class="mi-track">{html.escape(str(track))}</div>
      <div class="mi-artist">{html.escape(str(artist))}</div>
      <div class="mi-metrics">
        <div class="mi-metric"><div class="mi-metric-label">Energy</div><div class="mi-metric-value">{energy:.2f}</div></div>
        <div class="mi-metric"><div class="mi-metric-label">Tempo</div><div class="mi-metric-value">{tempo:.0f} BPM</div></div>
        <div class="mi-metric"><div class="mi-metric-label">Valence</div><div class="mi-metric-value">{valence:.2f}</div></div>
      </div>
    </div>
  </div>
  <div class="mi-why"><b>Why this track:</b> {html.escape(str(explanation))}</div>
  {_sl}
</div>""", unsafe_allow_html=True)


st.set_page_config(page_title="MusicIntent", page_icon="music", layout="centered")
init_db()
init_track_feedback()

MODE_THEME = {
    "Focus":       {"accent": "#A8C9BB", "tint": "#F0F8F4", "icon": "\u25CE"},
    "Energy":      {"accent": "#F0B89A", "tint": "#FFF3EC", "icon": "\u26A1"},
    "Inspiration": {"accent": "#E8BCC8", "tint": "#FFF1F6", "icon": "\u2727"},
}

from styling import inject_css as _new_css

def inject_css(mode=None):
    _new_css()
@st.cache_data
def load_artists():
    music = pd.read_csv("data/processed/music_expanded_clean.csv", low_memory=False)
    return music["artist"].value_counts().index.tolist()

artists = load_artists()
RANKERS = {"Focus": rank_focus, "Energy": rank_energy, "Inspiration": rank_inspiration}

if "step" not in st.session_state:
    st.session_state.step = "setup"
    st.session_state.seed_artists = []
    st.session_state.mode = None
    st.session_state.recs = None
    st.session_state.session_id = new_session_id()

if st.session_state.step == "setup":
    inject_css()
    st.markdown("<h1 style='text-align:center;'>MusicIntent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#536071;'>Personalised music for what you're looking for right now.</p>", unsafe_allow_html=True)
    st.subheader("Choose your artists")
    chosen = st.multiselect("Select 3-5 artists you enjoy:", options=artists,
                            default=st.session_state.seed_artists, max_selections=5)
    st.subheader("What are you listening for?")
    mode = st.radio("Select a mode:", options=["Focus", "Energy", "Inspiration"],
        captions=["Concentration, deep work", "Workouts, motivation", "Discovery, acclaimed music"], index=None)
    if st.button("Get recommendations"):
        if len(chosen) < 1:
            st.error("Please pick at least one artist.")
        elif mode is None:
            st.error("Please select a mode.")
        else:
            st.session_state.seed_artists = chosen
            st.session_state.mode = mode
            with st.spinner("Finding the perfect music..."):
                cands = generate_candidates_from_artists(chosen)
                _ranked = RANKERS[mode](cands)
                # Pin one seed-artist track near the top so users see an artist they picked
                _seed_mask = _ranked["artist"].isin(chosen)
                if _seed_mask.any():
                    _seed_track = _ranked[_seed_mask].head(1)
                    _rest = _ranked[~_ranked.index.isin(_seed_track.index)]
                    _ranked = pd.concat([_seed_track, _rest], ignore_index=True)
                st.session_state.recs = _ranked.head(8).to_dict("records")
            st.session_state.step = "results"
            st.rerun()

elif st.session_state.step == "results":
    mode = st.session_state.mode
    inject_css(mode)
    mode_key = mode.lower()
    icons = {"focus": "\u25CE", "energy": "\u26A1", "inspiration": "\u2728"}
    st.markdown(
        f'<div style="text-align:center; margin-bottom:6px;"><span class="mi-badge {mode_key}">{icons[mode_key]} {mode.upper()}</span></div>',
        unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#5A6478;'>Based on: {', '.join(st.session_state.seed_artists)}</p>", unsafe_allow_html=True)
    for i, t in enumerate(st.session_state.recs, 1):
        expl = explain(t, mode)
        song_card(i, t["name"], t["artist"], t["energy"], t["tempo"], t["valence"], expl, t.get("spotify_id"))
        _c1, _c2, _ = st.columns([1, 1, 4])
        if _c1.button("Like", key=f"like_{i}"):
            save_track_feedback(st.session_state.session_id, mode, t["name"], t["artist"], "like")
            st.toast("Liked " + t["name"])
        if _c2.button("Dislike", key=f"dislike_{i}"):
            save_track_feedback(st.session_state.session_id, mode, t["name"], t["artist"], "dislike")
            st.toast("Noted")
    if st.button("Rate this session"):
        st.session_state.step = "feedback"
        st.rerun()

elif st.session_state.step == "feedback":
    inject_css(st.session_state.mode)
    st.title("How was this session?")
    st.caption(f"Mode: {st.session_state.mode}")
    relevance = st.slider("How relevant were the recommendations?", 1, 5, 3)
    mode_fit = st.slider("Did they suit your chosen mode?", 1, 5, 3)
    expl_r = st.slider("Were the explanations useful?", 1, 5, 3)
    comment = st.text_area("Additional comments (optional)")
    if st.button("Submit feedback"):
        save_session(st.session_state.session_id, st.session_state.mode,
                     st.session_state.seed_artists, st.session_state.recs,
                     relevance, mode_fit, expl_r, comment)
        st.session_state.step = "done"
        st.rerun()

elif st.session_state.step == "done":
    inject_css()
    st.markdown("""
    <div style="text-align:center; padding:40px 0;">
      <div style="width:70px; height:70px; margin:0 auto; border-radius:50%; background:linear-gradient(135deg, #A8C9BB, #E8BCC8); display:flex; align-items:center; justify-content:center; font-size:32px; color:white;">&#10003;</div>
      <h2 style="margin-top:20px;">Session Complete!</h2>
      <p style="color:#536071;">Thank you for participating.<br>Your anonymous feedback has been recorded.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start a new session"):
        for k in ["step", "seed_artists", "mode", "recs", "session_id"]:
            st.session_state.pop(k, None)
        st.rerun()
