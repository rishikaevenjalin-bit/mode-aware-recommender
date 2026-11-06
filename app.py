import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import streamlit as st

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
    init_users,
    create_user,
    authenticate,
    get_user_liked_artists,
)
import mi


# ── Page configuration ─────────────────────────────────────────────────────

st.set_page_config(
    page_title="MusicIntent",
    page_icon="♫",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ── Research database ──────────────────────────────────────────────────────

# Preserve anonymous research logging and track-level feedback.
init_db()
init_track_feedback()
init_users()


# ── Data and recommendation configuration ──────────────────────────────────

@st.cache_data
def load_artists():
    music = pd.read_csv(
        "data/processed/music_expanded_clean.csv",
        low_memory=False,
    )
    return music["artist"].value_counts().index.tolist()


artists = load_artists()

RANKERS = {
    "Focus": rank_focus,
    "Energy": rank_energy,
    "Inspiration": rank_inspiration,
}

MODE_DETAILS = {
    "Focus": {
        "icon": "☾",
        "description": "Calm sounds for concentration and deep work.",
        "caption": "Calm · Concentration",
    },
    "Energy": {
        "icon": "⚡",
        "description": "Upbeat tracks to lift your mood and keep you moving.",
        "caption": "Upbeat · Motivation",
    },
    "Inspiration": {
        "icon": "✧",
        "description": "Acclaimed music and discoveries to spark curiosity.",
        "caption": "Discovery · Acclaim",
    },
}


# ── Session state ──────────────────────────────────────────────────────────

DEFAULT_STATE = {
    "step": "intro",
    "seed_artists": [],
    "mode": None,
    "recs": None,
    "session_id": None,
}

for key, default_value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = (
            new_session_id() if key == "session_id" else default_value
        )

# Persistent sign-in state (survives "start a new session" resets).
for key in ("user_id", "username"):
    if key not in st.session_state:
        st.session_state[key] = None


# ── Shared helpers ─────────────────────────────────────────────────────────

def set_page_style():
    """Apply the shared MusicIntent visual system."""
    mi.theme()
    mi.topbar()


def reset_session():
    """Start a fresh listening session, keeping the user signed in."""
    for key in DEFAULT_STATE:
        st.session_state.pop(key, None)

    for key, default_value in DEFAULT_STATE.items():
        st.session_state[key] = (
            new_session_id() if key == "session_id" else default_value
        )

    # Signed-in users go back to the welcome screen, not the landing page.
    st.session_state.step = "welcome" if st.session_state.get("user_id") else "intro"
    st.rerun()


def do_logout():
    st.session_state.user_id = None
    st.session_state.username = None
    reset_session()


def go_to(step):
    """Navigate between the app's stages."""
    st.session_state.step = step
    st.rerun()


def account_bar():
    """Small signed-in indicator with a log-out control."""
    if not st.session_state.get("user_id"):
        return
    left, right = st.columns([3, 1])
    with left:
        st.caption(f"✦ Signed in as **{st.session_state.username}** — "
                   "recommendations personalise as you like songs.")
    with right:
        if st.button("Log out", key="logout_btn", use_container_width=True):
            do_logout()


def generate_mix(chosen_artists, selected_mode, profile_artists=None):
    """
    Generate hybrid recommendations, rank them by listening mode,
    preserve seed-artist pinning, and prepare explanations in parallel.

    profile_artists: a signed-in user's previously-liked artists, blended
    into the taste profile for personalisation (None for guests).
    """

    candidates = generate_candidates_from_artists(
        chosen_artists,
        profile_artists=profile_artists,
    )

    if candidates is None or candidates.empty:
        return []

    ranked = RANKERS[selected_mode](candidates).reset_index(drop=True)

    # Keep the highest-ranked available track from each selected artist
    # at the beginning of the recommendation collection.
    pinned_indices = []

    for artist in chosen_artists:
        matching_tracks = ranked[ranked["artist"] == artist]

        if not matching_tracks.empty:
            pinned_indices.append(matching_tracks.index[0])

    if pinned_indices:
        pinned = ranked.loc[pinned_indices]
        remaining = ranked.drop(index=pinned_indices)

        ranked = pd.concat(
            [pinned, remaining],
            ignore_index=True,
        )

    recommendations = ranked.head(8).to_dict("records")

    # Generate explanations once, in parallel.
    if recommendations:
        with ThreadPoolExecutor(
            max_workers=min(8, len(recommendations))
        ) as pool:
            explanations = list(
                pool.map(
                    lambda track: explain(track, selected_mode),
                    recommendations,
                )
            )

        for track, explanation in zip(recommendations, explanations):
            track["explanation"] = explanation

    return recommendations


def render_footer():
    mi.footer()


# ── Intro (landing page) ─────────────────────────────────────────────────────

if st.session_state.step == "intro":

    mi.theme()
    mi.hero()

    st.markdown(
        "<div style='height:20px'></div>",
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.6, 1])
    with center:
        if st.button(
            "Continue  ✦",
            type="primary",
            use_container_width=True,
        ):
            go_to("auth")

    render_footer()


# ── Sign in / Sign up ───────────────────────────────────────────────────────

elif st.session_state.step == "auth":

    mi.theme()
    mi.topbar()

    mi.section_heading(
        "Welcome to MusicIntent",
        "Use it as a guest, or sign in so your music gets more you over time.",
    )

    left, center, right = st.columns([1, 1.6, 1])
    with center:
        if st.button(
            "Continue as guest  →",
            type="primary",
            use_container_width=True,
        ):
            go_to("setup")

    st.markdown(
        "<div class='mi-center' style='color:#8B85A5;font-size:0.82rem;"
        "margin:14px 0 6px'>— or —</div>",
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["Log in", "Create account"])

    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            lu = st.text_input("Username", key="login_user")
            lp = st.text_input("Password", type="password", key="login_pass")
            submitted = st.form_submit_button(
                "Log in  ✦", type="primary", use_container_width=True
            )
        if submitted:
            uid = authenticate(lu, lp)
            if uid:
                st.session_state.user_id = uid
                st.session_state.username = lu.strip()
                go_to("setup")
            else:
                st.error("Incorrect username or password.")

    with tab_signup:
        with st.form("signup_form", clear_on_submit=False):
            su = st.text_input("Choose a username", key="signup_user",
                               help="At least 3 characters.")
            sp = st.text_input("Choose a password", type="password",
                               key="signup_pass", help="At least 4 characters.")
            created = st.form_submit_button(
                "Create account  ♡", type="primary", use_container_width=True
            )
        if created:
            ok, result = create_user(su, sp)
            if ok:
                st.session_state.user_id = result
                st.session_state.username = su.strip()
                st.success("Account created — you're signed in!")
                go_to("setup")
            else:
                st.error(result)

    st.caption(
        "Having an account lets MusicIntent remember the songs you like and "
        "use them to personalise future recommendations. Guest sessions work "
        "fully — they just start fresh each time."
    )

    render_footer()


# ── Setup ──────────────────────────────────────────────────────────────────

elif st.session_state.step == "setup":

    set_page_style()
    mi.progress("setup")

    account_bar()

    mi.section_heading(
        "Let's make your mix",
        "Pick artists you love, then tap a mood.",
    )

    # Personalisation note for signed-in users with history.
    liked_history = (
        get_user_liked_artists(st.session_state.user_id)
        if st.session_state.get("user_id") else []
    )
    if liked_history:
        st.markdown(
            f"<div class='mi-center' style='margin:4px 0 10px;padding:10px;"
            f"border-radius:14px;background:rgba(145,134,233,0.08);"
            f"color:#777493;font-size:0.84rem'>"
            f"✦ Personalised for you — blending in {len(liked_history)} "
            f"artist(s) you've liked before.</div>",
            unsafe_allow_html=True,
        )

    # Artist selection.
    with st.container(border=True):

        st.markdown("### ♡  Artists you already love")

        chosen = st.multiselect(
            "Choose between 1 and 5 artists",
            options=artists,
            default=st.session_state.seed_artists,
            max_selections=5,
            placeholder="Search for an artist...",
            label_visibility="collapsed",
            key="artist_select",
        )

        if chosen:
            st.caption(f"✦ {len(chosen)} of 5 selected")

    # Listening intention — the mood boxes themselves are clickable.
    mi.section_heading(
        "What's your vibe today?",
        "Three moods. Endless possibilities. Find your sound.",
    )

    # Real Streamlit buttons styled to look like the mode cards. A real button
    # click reruns in-session reliably (no overlay, no page reload).
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button[kind="primary"]{
            min-height: 132px;
            border-radius: 24px;
            border: 1px solid #ffffff;
            background: #FFFFFFA6;
            box-shadow: 0 10px 30px #796BA512;
            color: #302A50;
            font-size: 1.12rem;
            font-weight: 700;
            white-space: pre-line;
            line-height: 1.5;
            padding: 18px 14px;
            transition: all .25s ease;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover{
            transform: translateY(-6px);
            box-shadow: 0 19px 38px #796BA526;
            border-color: #ffffff;
            background: #FFFFFFD8;
            color: #302A50;
        }
        div[data-testid="stButton"] button[kind="primary"]:focus:not(:active){
            border-color: #9186E9;
            color: #302A50;
        }
        div[data-testid="stButton"] button[kind="primary"] p{
            font-size: .76rem; font-weight: 500; color: #8883A1; margin: 0;
        }
        div[data-testid="stButton"] button[kind="primary"] p::first-line{
            font-size: 1.15rem; font-weight: 700; color: #302A50;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def _launch(selected_mode):
        """Validate the artist picks, then build and show the mix."""
        if not chosen:
            st.error("Choose at least one artist first.")
            return

        st.session_state.seed_artists = chosen
        st.session_state.mode = selected_mode

        # Signed-in users: blend their liked history into the profile.
        profile_artists = (
            get_user_liked_artists(st.session_state.user_id)
            if st.session_state.get("user_id") else None
        )

        try:
            with st.spinner("Gathering a little music magic..."):
                recommendations = generate_mix(
                    chosen, selected_mode, profile_artists=profile_artists
                )

            if not recommendations:
                st.warning(
                    "We couldn't find enough recommendations this time. "
                    "Try selecting different artists."
                )
            else:
                st.session_state.recs = recommendations
                st.session_state.step = "results"
                st.rerun()

        except Exception as error:
            st.error(
                "Something went wrong while creating your mix. "
                "Please try again."
            )
            print(f"MusicIntent recommendation error: {error}")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        if st.button(
            "☾  Focus\nSoft, low-distraction sounds for deep work and concentration.",
            key="pick_focus", type="primary", use_container_width=True,
        ):
            _launch("Focus")
    with col2:
        if st.button(
            "⚡  Energy\nUpbeat tracks to lift your mood and keep you moving.",
            key="pick_energy", type="primary", use_container_width=True,
        ):
            _launch("Energy")
    with col3:
        if st.button(
            "✧  Inspiration\nAcclaimed music and fresh discoveries to spark curiosity.",
            key="pick_inspiration", type="primary", use_container_width=True,
        ):
            _launch("Inspiration")

    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True,
    )

    back, spacer = st.columns([1, 3])
    with back:
        if st.button("← Back", use_container_width=True):
            go_to("auth")

    render_footer()


# ── Recommendations ────────────────────────────────────────────────────────

elif st.session_state.step == "results":

    set_page_style()
    mi.progress("results")

    mode = st.session_state.mode
    recommendations = st.session_state.recs or []

    # Listening mode identity.
    mi.badge(mode)

    st.markdown(
        f"""
        <div class="mi-center"
             style="
                color: #8B85A5;
                font-size: 0.84rem;
                margin: 12px 0 18px;
             ">
            A little collection inspired by
            <strong>{mi._e(", ".join(st.session_state.seed_artists))}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mi.section_heading(
        "Your little collection",
        "Eight tracks selected for the way you want to listen.",
    )

    # Small collection summary.
    st.markdown(
        f"""
        <div class="mi-center"
             style="
                margin: 12px 0 20px;
                color: #777493;
                font-size: 0.82rem;
             ">
            ♫ &nbsp; {len(recommendations)} recommended tracks
            &nbsp; · &nbsp;
            {MODE_DETAILS.get(mode, {}).get("caption", "")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not recommendations:

        st.info(
            "Your collection is empty. Let's try creating another mix."
        )

        if st.button(
            "← Back to choices",
            type="primary",
            use_container_width=True,
        ):
            go_to("setup")

    else:

        # Render each recommendation.
        for index, track in enumerate(recommendations, 1):

            explanation = (
                track.get("explanation")
                or explain(track, mode)
            )

            is_seed = (
                track["artist"] in st.session_state.seed_artists
            )

            mi.song_card(
                index,
                track["name"],
                track["artist"],
                f'{track["energy"]:.2f}',
                f'{track["tempo"]:.0f}',
                f'{track["valence"]:.2f}',
                explanation,
                is_seed=is_seed,
            )

            # External listening links.
            query = urllib.parse.quote(
                f'{track["name"]} {track["artist"]}'
            )

            spotify_url = (
                f"https://open.spotify.com/search/{query}"
            )

            youtube_url = (
                f"https://www.youtube.com/results?search_query={query}"
            )

            c1, c2, c3, c4 = st.columns(4, gap="small")

            with c1:
                st.link_button(
                    "♫ Spotify",
                    spotify_url,
                    key=f"spotify_{index}",
                    use_container_width=True,
                )

            with c2:
                st.link_button(
                    "▶ YouTube",
                    youtube_url,
                    key=f"youtube_{index}",
                    use_container_width=True,
                )

            with c3:
                if st.button(
                    "♡ Like",
                    key=f"like_{index}",
                    use_container_width=True,
                ):
                    save_track_feedback(
                        st.session_state.session_id,
                        mode,
                        track["name"],
                        track["artist"],
                        "like",
                        user_id=st.session_state.user_id,
                    )

                    st.toast("Added a little love ♡")

            with c4:
                if st.button(
                    "Not for me",
                    key=f"dislike_{index}",
                    use_container_width=True,
                ):
                    save_track_feedback(
                        st.session_state.session_id,
                        mode,
                        track["name"],
                        track["artist"],
                        "dislike",
                        user_id=st.session_state.user_id,
                    )

                    st.toast("Thanks for your feedback ✦")

            st.markdown(
                "<div style='height:10px'></div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='height:16px'></div>",
            unsafe_allow_html=True,
        )

        # Results navigation.
        left, spacer, right = st.columns([1, 0.5, 1.5])

        with left:
            if st.button(
                "← Change choices",
                use_container_width=True,
            ):
                go_to("setup")

        with right:
            if st.button(
                "Rate this mix  ✧",
                type="primary",
                use_container_width=True,
            ):
                go_to("feedback")

    render_footer()


# ── Feedback ───────────────────────────────────────────────────────────────

elif st.session_state.step == "feedback":

    set_page_style()
    mi.progress("feedback")

    mi.section_heading(
        "How did your mix feel?",
        "Your thoughts help us evaluate the recommendations.",
    )

    mi.badge(st.session_state.mode)

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

    # Anonymous research feedback.
    with st.container(border=True):

        st.markdown("### ♡  Your listening experience")

        relevance = st.slider(
            "How relevant were the recommendations?",
            1,
            5,
            3,
        )

        mode_fit = st.slider(
            "Did the songs suit your chosen mode?",
            1,
            5,
            3,
        )

        explanation_rating = st.slider(
            "Were the explanations useful?",
            1,
            5,
            3,
        )

        st.markdown(
            "<div style='height:8px'></div>",
            unsafe_allow_html=True,
        )

        comment = st.text_area(
            "Anything else you would like to tell us? (optional)",
            placeholder=(
                "Share a thought about your listening experience..."
            ),
            height=110,
        )

        st.caption(
            "Your feedback helps support the evaluation of MusicIntent."
        )

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

    # Feedback navigation.
    back, spacer, submit = st.columns([1, 0.5, 1.5])

    with back:
        if st.button(
            "← Back to mix",
            use_container_width=True,
        ):
            go_to("results")

    with submit:
        if st.button(
            "Send feedback  ♡",
            type="primary",
            use_container_width=True,
        ):

            try:
                save_session(
                    st.session_state.session_id,
                    st.session_state.mode,
                    st.session_state.seed_artists,
                    st.session_state.recs,
                    relevance,
                    mode_fit,
                    explanation_rating,
                    comment,
                    user_id=st.session_state.user_id,
                )

                st.session_state.step = "done"
                st.rerun()

            except Exception as error:
                st.error(
                    "We couldn't save your feedback. "
                    "Please try again."
                )
                print(f"MusicIntent feedback error: {error}")

    render_footer()


# ── Completion ─────────────────────────────────────────────────────────────

elif st.session_state.step == "done":

    mi.theme()
    mi.topbar()

    mi.complete(
        "A lovely session. Thank you!",
        (
            "Your feedback has been recorded. "
            "You helped us make music discovery better."
        ),
    )

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.8, 1])

    with center:
        if st.button(
            "Start a new listening journey  ✨",
            type="primary",
            use_container_width=True,
        ):
            reset_session()

    render_footer()
