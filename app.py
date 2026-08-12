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

MODE_THEME = {
    "Focus":       {"accent": "#A8C9BB", "tint": "#F0F8F4", "icon": "\u25CE"},
    "Energy":      {"accent": "#F0B89A", "tint": "#FFF3EC", "icon": "\u26A1"},
    "Inspiration": {"accent": "#E8BCC8", "tint": "#FFF1F6", "icon": "\u2727"},
}

def inject_css(mode=None):
    tint = MODE_THEME[mode]["tint"] if mode else "#EAF0FB"
    accent = MODE_THEME[mode]["accent"] if mode else "#B4A7C3"
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Quicksand', sans-serif; }}
    .stApp {{
        background:
            radial-gradient(circle at 15% 15%, rgba(180,167,195,0.35), transparent 45%),
            radial-gradient(circle at 85% 20%, {accent}55, transparent 45%),
            radial-gradient(circle at 50% 95%, rgba(232,188,200,0.4), transparent 50%),
            linear-gradient(145deg, #EDF2FB 0%, #F3ECF7 55%, {tint} 100%);
        background-attachment: fixed;
    }}
    .stApp, .stApp p, .stApp label, .stApp span, .stMarkdown,
    [data-testid="stCaptionContainer"], .stRadio label, h1, h2, h3 {{ color: #1B2436 !important; }}
    .block-container {{ max-width: 820px; padding-top: 2.5rem; }}
    h1, h2, h3 {{ font-weight: 700; }}
    .stButton > button {{
        width: 100%; min-height: 48px; border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.6);
        background: linear-gradient(135deg, rgba(180,167,195,0.85), rgba(232,188,200,0.85));
        color: #ffffff !important; font-weight: 700;
        backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 8px 24px rgba(120,110,160,0.25), inset 0 1px 1px rgba(255,255,255,0.6);
        transition: all 0.25s ease;
    }}
    .stButton > button:hover {{ transform: translateY(-2px); }}
    .stMultiSelect > div > div, .stTextArea > div > div {{
        border-radius: 16px !important;
        background: rgba(255,255,255,0.45) !important;
        border: 1px solid rgba(255,255,255,0.6) !important;
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    }}
    </style>
    """, unsafe_allow_html=True)

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
                st.session_state.recs = RANKERS[mode](cands).head(8).to_dict("records")
            st.session_state.step = "results"
            st.rerun()

elif st.session_state.step == "results":
    mode = st.session_state.mode
    theme = MODE_THEME[mode]
    inject_css(mode)
    st.markdown(f"<div style='text-align:center; margin-bottom:8px;'><span style='display:inline-block; padding:6px 18px; border-radius:20px; font-weight:700; font-size:14px; color:#172033; background:{theme['accent']};'>{theme['icon']} {mode.upper()}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#536071;'>Based on: {', '.join(st.session_state.seed_artists)}</p>", unsafe_allow_html=True)
    for i, t in enumerate(st.session_state.recs, 1):
        expl = explain(t, mode)
        st.markdown(f"""
        <div style="background:linear-gradient(145deg, rgba(255,255,255,0.82), rgba(255,255,255,0.48)); border:1px solid rgba(255,255,255,0.85); border-radius:18px; padding:18px; margin-bottom:14px; box-shadow:0 5px 18px rgba(60,70,100,0.08);">
          <div style="font-size:11px; font-weight:700; color:#7D8A9A;">#{i}</div>
          <div style="font-size:17px; font-weight:700;">{t['name']}</div>
          <div style="font-size:12px; color:#667085; margin-bottom:12px;">{t['artist']}</div>
          <div style="display:flex; gap:8px; margin-bottom:12px;">
            <div style="flex:1; background:rgba(255,255,255,0.55); border-radius:12px; padding:8px 6px; text-align:center;"><div style="font-size:10px; font-weight:600; color:#687384;">ENERGY</div><div style="font-size:14px; font-weight:700;">{t['energy']:.2f}</div></div>
            <div style="flex:1; background:rgba(255,255,255,0.55); border-radius:12px; padding:8px 6px; text-align:center;"><div style="font-size:10px; font-weight:600; color:#687384;">TEMPO</div><div style="font-size:14px; font-weight:700;">{t['tempo']:.0f}</div></div>
            <div style="flex:1; background:rgba(255,255,255,0.55); border-radius:12px; padding:8px 6px; text-align:center;"><div style="font-size:10px; font-weight:600; color:#687384;">VALENCE</div><div style="font-size:14px; font-weight:700;">{t['valence']:.2f}</div></div>
          </div>
          <div style="border-top:1px solid rgba(150,160,180,0.15); padding-top:10px; font-size:12px; line-height:1.5; color:#4F5B6B;"><strong>Why this was recommended</strong><br>{expl}</div>
        </div>
        """, unsafe_allow_html=True)
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
