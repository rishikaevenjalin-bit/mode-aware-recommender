import html
import urllib.parse

import pandas as pd
import streamlit as st

import mi
from src.recommender import generate_candidates_from_artists
from src.ranking.focus import rank_focus
from src.ranking.energy import rank_energy
from src.ranking.inspiration import rank_inspiration
from src.explanation.explain import explain
from src.db.database import (
    init_db,
    new_session_id,
    save_session,
    init_track_feedback,
    save_track_feedback,
)

st.set_page_config(page_title="MusicIntent", page_icon="♫", layout="centered")

init_db()
init_track_feedback()
mi.theme()

MODE_DETAILS = {
    "Focus": {
        "symbol": "☾",
        "short": "Quiet your mind",
        "description": "Low-distraction sounds for deep work, reading and calm concentration.",
    },
    "Energy": {
        "symbol": "ϟ",
        "short": "Find your momentum",
        "description": "Upbeat, high-energy tracks for movement, motivation and a brighter mood.",
    },
    "Inspiration": {
        "symbol": "✧",
        "short": "Follow your curiosity",
        "description": "Acclaimed music chosen to open the door to discovery and exploration.",
    },
}
RANKERS = {"Focus": rank_focus, "Energy": rank_energy, "Inspiration": rank_inspiration}


@st.cache_data
def load_artists():
    music = pd.read_csv("data/processed/music_expanded_clean.csv", low_memory=False)
    return music["artist"].dropna().value_counts().index.tolist()


artists = load_artists()

if "step" not in st.session_state:
    st.session_state.step = "welcome"
    st.session_state.seed_artists = []
    st.session_state.mode = None
    st.session_state.recs = None
    st.session_state.session_id = new_session_id()


def section_label(text):
    st.markdown('<div style="font-size:.72rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#8175d3;margin:8px 0 10px;">' + html.escape(text) + '</div>', unsafe_allow_html=True)


def render_welcome():
    st.markdown(
        '<div style="position:relative;overflow:hidden;text-align:center;padding:34px 24px 26px;margin:4px auto 22px;border:1px solid rgba(255,255,255,.88);border-radius:32px;background:rgba(255,255,255,.48);backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);box-shadow:0 18px 55px rgba(89,78,153,.09);">'
        '<div style="position:absolute;width:230px;height:230px;border-radius:50%;background:rgba(205,216,255,.55);filter:blur(55px);top:-120px;left:-65px;"></div>'
        '<div style="position:absolute;width:230px;height:230px;border-radius:50%;background:rgba(255,203,237,.5);filter:blur(55px);bottom:-135px;right:-70px;"></div>'
        '<div style="position:relative;z-index:1;">'
        '<div style="display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;background:rgba(137,126,232,.10);color:#796dcc;font-size:.7rem;font-weight:800;letter-spacing:.15em;">✦ YOUR MUSIC, YOUR MOMENT ✦</div>'
        '<div style="font-size:clamp(3.2rem,8vw,5.3rem);font-weight:800;letter-spacing:-.075em;line-height:1.04;margin:17px 0 8px;color:#202342;">Music<span style="background:linear-gradient(100deg,#897ee8,#d982bd);-webkit-background-clip:text;background-clip:text;color:transparent;">Intent</span></div>'
        '<div style="font-size:1.08rem;font-weight:600;color:#555d80;">Music that understands your moment.</div>'
        '<div style="max-width:590px;margin:12px auto 0;color:#737b98;font-size:.9rem;line-height:1.75;">Not just what you listen to — how you want to feel. Choose your artists and your intention, then discover tracks selected for the moment you are in.</div>'
        '<div style="display:flex;justify-content:center;align-items:center;gap:8px;margin:24px auto 0;">'
        '<div style="width:42px;height:42px;border-radius:50%;background:linear-gradient(145deg,#d8ddff,#c3b8f2);display:flex;align-items:center;justify-content:center;color:#6259a9;font-size:20px;box-shadow:0 5px 15px rgba(137,126,232,.15);">♫</div>'
        '<div style="display:flex;align-items:center;gap:4px;height:30px;">'
        '<span style="width:3px;height:9px;border-radius:9px;background:#a49ae9;"></span><span style="width:3px;height:19px;border-radius:9px;background:#d99acb;"></span><span style="width:3px;height:13px;border-radius:9px;background:#a49ae9;"></span><span style="width:3px;height:25px;border-radius:9px;background:#d99acb;"></span><span style="width:3px;height:10px;border-radius:9px;background:#a49ae9;"></span><span style="width:3px;height:18px;border-radius:9px;background:#d99acb;"></span><span style="width:3px;height:7px;border-radius:9px;background:#a49ae9;"></span>'
        '</div><span style="font-size:.72rem;color:#9298b0;font-weight:700;letter-spacing:.08em;">A LITTLE MORE YOU</span></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="text-align:center;font-size:1.3rem;font-weight:800;letter-spacing:-.04em;color:#252846;margin:8px 0 4px;">Find your listening mood</div><div style="text-align:center;color:#858ba5;font-size:.84rem;margin-bottom:16px;">Three intentions. One personal soundtrack.</div>', unsafe_allow_html=True)

    columns = st.columns(3, gap="medium")
    cards = [
        ("☾", "Focus", "Calm, low-distraction music for concentration and deep work.", "#e4e7ff", "#454da4"),
        ("ϟ", "Energy", "Upbeat, high-tempo tracks for workouts and motivation.", "#ffe2f4", "#a0447d"),
        ("✧", "Inspiration", "Acclaimed music for discovery and fresh perspectives.", "#eee2ff", "#7048ae"),
    ]
    for col, (symbol, name, description, tint, ink) in zip(columns, cards):
        with col:
            st.markdown(
                '<div style="height:100%;min-height:155px;text-align:center;padding:18px 13px;border:1px solid rgba(255,255,255,.9);border-radius:23px;background:rgba(255,255,255,.56);backdrop-filter:blur(16px);box-shadow:0 10px 30px rgba(89,78,153,.06);">'
                '<div style="width:46px;height:46px;margin:0 auto 10px;border-radius:17px;background:' + tint + ';color:' + ink + ';display:flex;align-items:center;justify-content:center;font-size:23px;">' + symbol + '</div>'
                '<div style="font-weight:800;color:#252846;font-size:1rem;margin-bottom:6px;">' + name + '</div>'
                '<div style="font-size:.76rem;line-height:1.6;color:#747b98;">' + description + '</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        if st.button("Begin your journey  →", type="primary", use_container_width=True):
            st.session_state.step = "setup"
            st.rerun()
    st.markdown('<div class="mi-footnote">A thoughtful music discovery experience · No account needed</div>', unsafe_allow_html=True)


def render_setup():
    mi.page_header("LET'S SET THE SCENE", "Build your moment", "Start with artists you love, then choose what you want your music to do for you.")
    st.markdown('<div class="mi-card"><div style="font-weight:800;font-size:1rem;margin-bottom:4px;">01 · Your artists</div><div style="color:#737b98;font-size:.84rem;margin-bottom:13px;">Choose up to five artists to guide your recommendations.</div></div>', unsafe_allow_html=True)
    chosen = st.multiselect(
        "Select artists you enjoy",
        options=artists,
        default=st.session_state.seed_artists,
        max_selections=5,
        placeholder="Search for an artist...",
        help="Pick at least one artist. Your selections are used to find relevant tracks.",
    )
    st.markdown('<div style="height:10px;"></div><div class="mi-card"><div style="font-weight:800;font-size:1rem;margin-bottom:4px;">02 · Your intention</div><div style="color:#737b98;font-size:.84rem;">What kind of listening moment are you creating?</div></div>', unsafe_allow_html=True)
    mode = st.radio(
        "Choose your listening mode",
        options=["Focus", "Energy", "Inspiration"],
        format_func=lambda value: f"{MODE_DETAILS[value]['symbol']}  {value}  ·  {MODE_DETAILS[value]['short']}",
        index=["Focus", "Energy", "Inspiration"].index(st.session_state.mode) if st.session_state.mode in MODE_DETAILS else None,
        captions=[MODE_DETAILS[x]["description"] for x in ["Focus", "Energy", "Inspiration"]],
    )
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1])
    with left:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = "welcome"
            st.rerun()
    with right:
        if st.button("Find my music  ✦", type="primary", use_container_width=True):
            if not chosen:
                st.error("Choose at least one artist to continue.")
            elif mode is None:
                st.error("Choose a listening mode to continue.")
            else:
                st.session_state.seed_artists = chosen
                st.session_state.mode = mode
                with st.spinner("Finding tracks for your moment..."):
                    candidates = generate_candidates_from_artists(chosen)
                    ranked = RANKERS[mode](candidates).reset_index(drop=True)
                    # Preserve the existing behaviour: pin the best-ranked track
                    # from each selected artist before filling the remaining list.
                    pinned_indices = []
                    for artist in chosen:
                        hit = ranked[ranked["artist"] == artist]
                        if not hit.empty:
                            pinned_indices.append(hit.index[0])
                    if pinned_indices:
                        pinned = ranked.loc[pinned_indices]
                        rest = ranked.drop(index=pinned_indices)
                        ranked = pd.concat([pinned, rest], ignore_index=True)
                    st.session_state.recs = ranked.head(8).to_dict("records")
                st.session_state.step = "results"
                st.rerun()


def render_results():
    mode = st.session_state.mode
    mi.page_header("MADE FOR THIS MOMENT", "Your soundtrack is here", "A collection shaped by your artists and the listening mode you chose.")
    mi.badge(mode)
    st.markdown('<div style="text-align:center;color:#737b98;font-size:.82rem;margin:-2px 0 20px;">Inspired by: ' + html.escape(", ".join(st.session_state.seed_artists)) + '</div>', unsafe_allow_html=True)

    for index, track in enumerate(st.session_state.recs, 1):
        explanation = explain(track, mode)
        is_seed = track["artist"] in st.session_state.seed_artists
        mi.song_card(
            index,
            track["name"],
            track["artist"],
            f"{float(track['energy']):.2f}",
            f"{float(track['tempo']):.0f}",
            f"{float(track['valence']):.2f}",
            explanation,
            is_seed=is_seed,
        )
        query = urllib.parse.quote(f"{track['name']} {track['artist']}")
        spotify_url = f"https://open.spotify.com/search/{query}"
        youtube_url = f"https://www.youtube.com/results?search_query={query}"
        c1, c2, c3, c4 = st.columns(4, gap="small")
        with c1:
            st.link_button("Spotify ↗", spotify_url, key=f"spotify_{index}", use_container_width=True)
        with c2:
            st.link_button("YouTube ↗", youtube_url, key=f"youtube_{index}", use_container_width=True)
        with c3:
            if st.button("♡ Like", key=f"like_{index}", use_container_width=True):
                save_track_feedback(st.session_state.session_id, mode, track["name"], track["artist"], "like")
                st.toast("Added to your likes")
        with c4:
            if st.button("Not for me", key=f"dislike_{index}", use_container_width=True):
                save_track_feedback(st.session_state.session_id, mode, track["name"], track["artist"], "dislike")
                st.toast("Feedback noted")
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="mi-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:#737b98;font-size:.84rem;margin-bottom:10px;">Help us make the experience better with a little feedback.</div>', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        if st.button("Rate this session  →", type="primary", use_container_width=True):
            st.session_state.step = "feedback"
            st.rerun()


def render_feedback():
    mi.page_header("ONE LAST THING", "How did it feel?", "Your anonymous feedback helps us understand how well each listening mode works.")
    mi.badge(st.session_state.mode)
    st.markdown('<div class="mi-card"><div style="font-weight:800;margin-bottom:4px;">A few quick reflections</div><div style="font-size:.83rem;color:#737b98;">There are no right or wrong answers. Share what you genuinely experienced.</div></div>', unsafe_allow_html=True)
    relevance = st.slider("How relevant were the recommendations to your taste?", 1, 5, 3, help="1 = Not relevant · 5 = Very relevant")
    mode_fit = st.slider("How well did the tracks match your chosen mode?", 1, 5, 3, help="1 = Not at all · 5 = Extremely well")
    explanation_rating = st.slider("How useful were the explanations for each track?", 1, 5, 3, help="1 = Not useful · 5 = Very useful")
    comment = st.text_area("Anything else you'd like to share? (Optional)", placeholder="Tell us what worked well or what could be improved...", height=120)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1])
    with left:
        if st.button("← Back to recommendations", use_container_width=True):
            st.session_state.step = "results"
            st.rerun()
    with right:
        if st.button("Submit feedback  ✦", type="primary", use_container_width=True):
            save_session(
                st.session_state.session_id,
                st.session_state.mode,
                st.session_state.seed_artists,
                st.session_state.recs,
                relevance,
                mode_fit,
                explanation_rating,
                comment,
            )
            st.session_state.step = "done"
            st.rerun()


def render_done():
    mi.complete("Thank you for listening.", "Your anonymous feedback has been recorded. It means a lot.")
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        if st.button("Start a new listening session", type="primary", use_container_width=True):
            for key in ["step", "seed_artists", "mode", "recs", "session_id"]:
                st.session_state.pop(key, None)
            st.rerun()
    st.markdown('<div class="mi-footnote">MusicIntent · Find the sound for right now</div>', unsafe_allow_html=True)


if st.session_state.step == "welcome":
    render_welcome()
elif st.session_state.step == "setup":
    render_setup()
elif st.session_state.step == "results":
    render_results()
elif st.session_state.step == "feedback":
    render_feedback()
elif st.session_state.step == "done":
    render_done()
