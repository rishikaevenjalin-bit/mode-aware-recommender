import html
import streamlit as st


# ============================================================
# MUSICINTENT — CELESTIAL MUSIC STUDIO
# ============================================================

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #252142;
    --muted: #817D9D;
    --soft: #A9A4BE;
    --lav: #9186E9;
    --lav-dark: #786DCE;
    --pink: #E6A5CF;
    --line: rgba(255,255,255,.78);
    --glass: rgba(255,255,255,.66);
    --shadow: 0 18px 55px rgba(91,78,150,.10);
    --ease: cubic-bezier(.2,.8,.2,1);
}

* {
    font-family: 'Plus Jakarta Sans', 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 5%, rgba(189,207,255,.62), transparent 32%),
        radial-gradient(ellipse at 95% 10%, rgba(255,195,230,.50), transparent 30%),
        radial-gradient(ellipse at 55% 100%, rgba(211,195,255,.56), transparent 38%),
        linear-gradient(135deg,#F9FBFF 0%,#F3F0FF 52%,#FFF5FB 100%);
    background-attachment: fixed;
    color: var(--ink);
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1000px;
    padding: 1.4rem 1.5rem 4rem;
}

h1, h2, h3 {
    color: var(--ink) !important;
    letter-spacing: -.045em;
    font-weight: 800 !important;
}

h1 {
    font-size: clamp(2rem,5vw,3rem) !important;
}

h2 {
    font-size: 1.65rem !important;
}

p, li, label {
    color: var(--ink);
}

[data-testid="stCaptionContainer"] p {
    color: var(--muted);
}

div[data-testid="stVerticalBlock"] {
    gap: .85rem;
}

/* ---------------- TOP NAVIGATION ---------------- */

.mi-topline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.mi-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: -.05em;
    color: var(--ink);
}

.mi-brand-mark {
    width: 37px;
    height: 37px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    background: linear-gradient(145deg,#9388EC,#E6A5CF);
    color: white;
    font-size: 19px;
    box-shadow: 0 7px 20px #A89AE955;
}

.mi-top-pill {
    border: 1px solid white;
    background: #FFFFFF85;
    border-radius: 999px;
    padding: 8px 13px;
    color: #8177B9;
    font-size: .66rem;
    font-weight: 800;
    letter-spacing: .09em;
}

/* ---------------- HERO ---------------- */

.mi-hero {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    text-align: center;
    padding: 40px 26px 29px;
    border: 1px solid var(--line);
    border-radius: 34px;
    background: linear-gradient(145deg,rgba(255,255,255,.79),rgba(255,255,255,.40));
    backdrop-filter: blur(22px);
    box-shadow: var(--shadow);
    margin-bottom: 27px;
}

.mi-hero:before,
.mi-hero:after {
    content: "";
    position: absolute;
    z-index: -1;
    border-radius: 50%;
    pointer-events: none;
}

.mi-hero:before {
    width: 320px;
    height: 320px;
    left: -150px;
    top: -190px;
    background: radial-gradient(circle,#BFC8FF88,transparent 70%);
}

.mi-hero:after {
    width: 330px;
    height: 330px;
    right: -150px;
    bottom: -210px;
    background: radial-gradient(circle,#FFC5E588,transparent 70%);
}

.mi-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 15px;
    margin-bottom: 15px;
    border: 1px solid white;
    border-radius: 999px;
    background: #F4F0FFCC;
    color: #8277C7;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .14em;
}

.mi-hero-title {
    font-size: clamp(3rem,8vw,5.5rem);
    line-height: 1;
    letter-spacing: -.085em;
    font-weight: 800;
    color: #282344;
    margin: 4px 0 13px;
}

.mi-hero-title span {
    background: linear-gradient(100deg,#8278E5,#C17ED1 60%,#E49BC6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.mi-tagline {
    font-size: clamp(1rem,2.5vw,1.22rem);
    font-weight: 700;
    color: #625D83;
    margin-bottom: 10px;
}

.mi-description {
    max-width: 610px;
    margin: 0 auto;
    color: #85809F;
    font-size: .86rem;
    line-height: 1.85;
}

.mi-decor {
    position: absolute;
    pointer-events: none;
    animation: mi-float 5s ease-in-out infinite;
}

.mi-decor.d1 {
    left: 10%;
    top: 21%;
    font-size: 26px;
    color: #A69AEF;
}

.mi-decor.d2 {
    right: 12%;
    top: 17%;
    font-size: 22px;
    color: #E5A1D0;
    animation-delay: -2s;
}

.mi-decor.d3 {
    right: 18%;
    bottom: 17%;
    font-size: 16px;
    color: #B7A7F2;
    animation-delay: -1s;
}

.mi-decor.d4 {
    left: 17%;
    bottom: 15%;
    font-size: 17px;
    color: #E6A8D4;
    animation-delay: -3s;
}

@keyframes mi-float {
    0%,100% { transform: translateY(0) rotate(-5deg); }
    50% { transform: translateY(-10px) rotate(8deg); }
}

/* ---------------- VINYL MASCOT ---------------- */

.mi-orbit {
    position: relative;
    width: 116px;
    height: 116px;
    margin: 0 auto 18px;
    display: grid;
    place-items: center;
}

.mi-vinyl {
    position: relative;
    width: 96px;
    height: 96px;
    border-radius: 50%;
    background:
        repeating-radial-gradient(circle at center,
        #29253F 0 3px,
        #423A58 4px 5px,
        #29253F 6px 8px);
    box-shadow: 0 12px 28px #6C5D9A55;
    animation: mi-spin 13s linear infinite;
    display: grid;
    place-items: center;
}

.mi-vinyl:before {
    content: "";
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg,#E9B3D9,#A69AF0);
    border: 4px solid #F8E9F5;
}

.mi-vinyl:after {
    content: "";
    position: absolute;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: white;
}

@keyframes mi-spin {
    to { transform: rotate(360deg); }
}

.mi-mascot {
    position: absolute;
    right: -3px;
    bottom: -1px;
    width: 40px;
    height: 40px;
    border-radius: 14px 14px 17px 17px;
    background: linear-gradient(145deg,#FFF2A9,#FFC9E8);
    box-shadow: 0 5px 15px #A18BC455;
    display: grid;
    place-items: center;
    font-size: 22px;
    transform: rotate(9deg);
    animation: mi-bob 3s ease-in-out infinite;
}

@keyframes mi-bob {
    0%,100% { transform: translateY(0) rotate(9deg); }
    50% { transform: translateY(-5px) rotate(0deg); }
}

/* ---------------- MINI MUSIC PLAYER ---------------- */

.mi-player {
    display: flex;
    align-items: center;
    gap: 12px;
    max-width: 365px;
    margin: 21px auto 0;
    padding: 11px 15px;
    border: 1px solid white;
    border-radius: 18px;
    background: #FFFFFF90;
    box-shadow: 0 8px 25px #7D70B01A;
    text-align: left;
}

.mi-player-icon {
    width: 37px;
    height: 37px;
    flex-shrink: 0;
    border-radius: 12px;
    background: linear-gradient(135deg,#D8D2FF,#F7CDEB);
    display: grid;
    place-items: center;
    color: #7569BD;
}

.mi-player-copy {
    flex: 1;
    min-width: 0;
}

.mi-player-copy b {
    display: block;
    font-size: .72rem;
    color: #514B76;
}

.mi-player-copy span {
    display: block;
    font-size: .62rem;
    color: #9993B1;
    margin-top: 3px;
}

.mi-wave {
    height: 23px;
    display: flex;
    align-items: center;
    gap: 3px;
}

.mi-wave i {
    display: block;
    width: 3px;
    border-radius: 8px;
    background: linear-gradient(#A99CF0,#E8A9D2);
    animation: mi-wave 1s ease-in-out infinite alternate;
}

.mi-wave i:nth-child(1) { height: 8px; }
.mi-wave i:nth-child(2) { height: 17px; animation-delay: .2s; }
.mi-wave i:nth-child(3) { height: 12px; animation-delay: .4s; }
.mi-wave i:nth-child(4) { height: 21px; animation-delay: .1s; }
.mi-wave i:nth-child(5) { height: 10px; animation-delay: .3s; }
.mi-wave i:nth-child(6) { height: 16px; animation-delay: .5s; }

@keyframes mi-wave {
    to { transform: scaleY(.45); opacity: .6; }
}

/* ---------------- SECTION HEADINGS ---------------- */

.mi-section-title {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -.045em;
    color: #302A50;
    margin: 8px 0 4px;
}

.mi-section-sub {
    text-align: center;
    color: #9690AD;
    font-size: .79rem;
    line-height: 1.6;
    margin: 0 0 17px;
}

/* ---------------- MOOD CARDS ---------------- */

.mi-mode-card {
    position: relative;
    height: 100%;
    min-height: 185px;
    padding: 21px 16px;
    text-align: center;
    border: 1px solid white;
    border-radius: 25px;
    background: #FFFFFFA0;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px #796BA512;
    transition: all .25s var(--ease);
}

.mi-mode-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 19px 38px #796BA526;
}

.mi-mode-icon {
    width: 51px;
    height: 51px;
    border-radius: 18px;
    margin: 0 auto 12px;
    display: grid;
    place-items: center;
    font-size: 24px;
}

.mi-mode-card b {
    display: block;
    font-size: .95rem;
    color: #302A50;
    margin-bottom: 7px;
}

.mi-mode-card p {
    font-size: .72rem;
    color: #8883A1;
    line-height: 1.65;
    margin: 0;
}

.mi-focus .mi-mode-icon {
    background: #E2E5FF;
    color: #6268B7;
}

.mi-energy .mi-mode-icon {
    background: #FFE0F2;
    color: #B75C98;
}

.mi-inspiration .mi-mode-icon {
    background: #EEE1FF;
    color: #8766BD;
}

/* ---------------- PROGRESS ---------------- */

.mi-progress {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    margin: 6px 0 19px;
}

.mi-progress span {
    height: 6px;
    width: 43px;
    border-radius: 99px;
    background: #E5E0F3;
}

.mi-progress span.active {
    background: linear-gradient(90deg,#9388E9,#DDA4D5);
}

.mi-progress-label {
    font-size: .66rem;
    color: #928BAE;
    text-align: center;
    letter-spacing: .12em;
    font-weight: 800;
    margin-bottom: 8px;
}

/* ---------------- GLASS PANELS ---------------- */

.mi-panel {
    padding: 24px;
    border: 1px solid white;
    border-radius: 26px;
    background: #FFFFFF8C;
    box-shadow: var(--shadow);
    backdrop-filter: blur(18px);
}

/* ---------------- MODE BADGES ---------------- */

.mi-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 8px 15px;
    border-radius: 999px;
    font-size: .7rem;
    font-weight: 800;
    letter-spacing: .08em;
    border: 1px solid white;
}

.mi-badge.focus {
    background: #E2E5FF;
    color: #535DAF;
}

.mi-badge.energy {
    background: #FFE0F2;
    color: #A64F87;
}

.mi-badge.inspiration {
    background: #EEE1FF;
    color: #7956B1;
}

.mi-badge.seed {
    background: linear-gradient(90deg,#E5E0FF,#FFE0F2);
    color: #735B9D;
    letter-spacing: 0;
    font-size: .63rem;
    padding: 5px 9px;
}

.mi-center {
    text-align: center;
}

/* ---------------- SONG CARDS ---------------- */

.mi-card {
    position: relative;
    overflow: hidden;
    background: #FFFFFFC2;
    backdrop-filter: blur(18px);
    border: 1px solid white;
    border-radius: 24px;
    box-shadow: 0 12px 34px #7164A014;
    padding: 20px;
    margin: 0 0 11px;
    transition: transform .22s var(--ease), box-shadow .22s var(--ease);
}

.mi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 19px 44px #7164A025;
}

.mi-card:before {
    content: "";
    position: absolute;
    right: -45px;
    top: -60px;
    width: 145px;
    height: 145px;
    border-radius: 50%;
    background: radial-gradient(circle,#E8DFFF80,transparent 70%);
    pointer-events: none;
}

.mi-head {
    display: flex;
    align-items: center;
    gap: 13px;
    position: relative;
}

.mi-rank {
    flex: 0 0 35px;
    height: 35px;
    border-radius: 13px;
    background: #F1EEFF;
    border: 1px solid white;
    display: grid;
    place-items: center;
    font-weight: 800;
    font-size: .8rem;
    color: #8277C7;
}

.mi-art {
    flex: 0 0 60px;
    width: 60px;
    height: 60px;
    border-radius: 18px;
    object-fit: cover;
    background: linear-gradient(145deg,#D8D2FF,#F7D2EA);
    display: grid;
    place-items: center;
    font-size: 25px;
    color: #8175C5;
}

.mi-meta {
    flex: 1;
    min-width: 0;
}

.mi-track {
    font-size: 1rem;
    font-weight: 800;
    color: #302A50;
    line-height: 1.35;
    overflow-wrap: anywhere;
}

.mi-artist {
    font-size: .77rem;
    color: #8883A1;
    margin-top: 4px;
}

.mi-sig {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 11px;
}

.mi-chip {
    background: #F8F6FF;
    border: 1px solid #EEEAF9;
    border-radius: 10px;
    padding: 5px 9px;
    font-size: .65rem;
    color: #706B8D;
}

.mi-chip .k {
    color: #A19BB7;
    font-weight: 600;
}

.mi-chip .v {
    color: #514B76;
    font-weight: 800;
    margin-left: 4px;
}

.mi-why {
    background: linear-gradient(120deg,#F8F6FF,#FFF7FC);
    border: 1px solid #F0EAFB;
    border-radius: 17px;
    padding: 14px 15px;
    margin-top: 15px;
}

.mi-why .l {
    font-size: .61rem;
    font-weight: 800;
    letter-spacing: .13em;
    color: #9488D8;
    margin-bottom: 6px;
}

.mi-why .b {
    font-size: .8rem;
    line-height: 1.75;
    color: #5E587B;
}

/* ---------------- STREAMLIT BUTTONS ---------------- */

.stButton > button,
.stFormSubmitButton > button,
[data-testid="stLinkButton"] > a {
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: .83rem !important;
    padding: .65rem 1rem !important;
    border: 1px solid white !important;
    background: #FFFFFFC2 !important;
    color: #514B76 !important;
    box-shadow: 0 4px 14px #766AA010 !important;
    transition: all .2s var(--ease) !important;
}

.stButton > button:hover,
[data-testid="stLinkButton"] > a:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 22px #766AA022 !important;
    border-color: #DCD5FA !important;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(100deg,#9186E9,#B59AEF 55%,#E5A3D0) !important;
    color: white !important;
    border: 0 !important;
    box-shadow: 0 9px 24px #A18DEB55 !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 13px 30px #A18DEB70 !important;
}

[data-testid="stLinkButton"] a {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* ---------------- INPUTS ---------------- */

[data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #FFFFFFD9 !important;
    border: 1px solid white !important;
    border-radius: 14px !important;
    min-height: 48px;
}

[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: linear-gradient(90deg,#9589E9,#D4A0DB) !important;
    border-radius: 999px !important;
    color: white !important;
}

div[data-baseweb="popover"] ul[role="listbox"] {
    background: #FFFDFF !important;
    border-radius: 15px !important;
}

div[data-baseweb="popover"] li {
    color: #302A50 !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #FFFFFFD9 !important;
    border: 1px solid white !important;
    border-radius: 14px !important;
    color: #302A50 !important;
}

[data-testid="stRadio"] > div {
    gap: 8px;
}

[data-testid="stRadio"] label {
    background: #FFFFFF8C;
    border: 1px solid white;
    border-radius: 14px;
    padding: 10px 13px;
}

[data-testid="stRadio"] label:has(input:checked) {
    background: #F0ECFF;
    border-color: #B9ACEF;
    box-shadow: 0 0 0 3px #A99BEF22;
}

[data-testid="stSlider"] [role="slider"] {
    background: #9186E9 !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: #9186E9 !important;
}

[data-testid="stAlert"] {
    border-radius: 14px;
}

/* ---------------- COMPLETION ---------------- */

.mi-complete {
    position: relative;
    overflow: hidden;
    padding: 39px 23px;
    text-align: center;
    border: 1px solid white;
    border-radius: 31px;
    background: #FFFFFF99;
    box-shadow: var(--shadow);
}

.mi-check {
    width: 84px;
    height: 84px;
    border-radius: 28px;
    margin: 0 auto 19px;
    background: linear-gradient(145deg,#A99DF0,#EAB1D7);
    display: grid;
    place-items: center;
    color: white;
    font-size: 38px;
    box-shadow: 0 12px 28px #A18DEB55;
    transform: rotate(-5deg);
}

.mi-footer {
    text-align: center;
    color: #AAA4BE;
    font-size: .66rem;
    margin-top: 29px;
    letter-spacing: .06em;
}

/* ---------------- RESPONSIVE ---------------- */

@media (max-width: 640px) {
    .block-container {
        padding: 1rem .8rem 3rem;
    }

    .mi-hero {
        padding: 30px 16px 23px;
        border-radius: 26px;
    }

    .mi-decor.d1 { left: 5%; }
    .mi-decor.d2 { right: 6%; }

    .mi-panel {
        padding: 16px;
    }

    .mi-card {
        padding: 15px;
    }

    .mi-art {
        flex-basis: 49px;
        width: 49px;
        height: 49px;
        border-radius: 15px;
    }

    .mi-track {
        font-size: .9rem;
    }

    .mi-mode-card {
        min-height: 165px;
        padding: 16px 10px;
    }

    .mi-top-pill {
        font-size: .55rem;
        padding: 7px 9px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *:before, *:after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
"""


# ============================================================
# CORE HELPERS
# ============================================================

def theme():
    st.markdown(_CSS, unsafe_allow_html=True)


def _e(value):
    return html.escape(str(value))


# ============================================================
# NAVIGATION
# ============================================================

def topbar():
    st.markdown(
        '<div class="mi-topline">'
        '<div class="mi-brand">'
        '<span class="mi-brand-mark">♫</span> MusicIntent'
        '</div>'
        '<div class="mi-top-pill">YOUR PERSONAL MUSIC UNIVERSE ✦</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def progress(step):
    labels = {
        "setup": 1,
        "results": 2,
        "feedback": 3,
        "done": 3,
    }

    active = labels.get(step, 1)

    dots = "".join(
        f'<span class="{"active" if i <= active else ""}"></span>'
        for i in range(1, 4)
    )

    captions = {
        1: "01  ·  YOUR TASTE",
        2: "02  ·  YOUR DISCOVERY",
        3: "03  ·  YOUR FEEDBACK",
    }

    st.markdown(
        f'<div class="mi-progress-label">{captions[active]}</div>'
        f'<div class="mi-progress">{dots}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# WELCOME PAGE
# ============================================================

def hero():
    st.markdown(
        '<div class="mi-hero">'
        '<span class="mi-decor d1">✦</span>'
        '<span class="mi-decor d2">♫</span>'
        '<span class="mi-decor d3">✧</span>'
        '<span class="mi-decor d4">♪</span>'

        '<div class="mi-orbit">'
        '<div class="mi-vinyl"></div>'
        '<div class="mi-mascot">✦</div>'
        '</div>'

        '<div class="mi-eyebrow">✧ MUSIC DISCOVERY, REIMAGINED ✧</div>'

        '<div class="mi-hero-title">Music<span>Intent</span></div>'

        '<div class="mi-tagline">'
        'A little music magic for whatever moment you are in.'
        '</div>'

        '<p class="mi-description">'
        'Your listening mood matters. Choose what you need right now, '
        'discover tracks that fit your intention, and find out why '
        'each song made your mix.'
        '</p>'

        '<div class="mi-player">'
        '<div class="mi-player-icon">♫</div>'
        '<div class="mi-player-copy">'
        '<b>your moment, your soundtrack</b>'
        '<span>curated around how you feel</span>'
        '</div>'
        '<div class="mi-wave">'
        '<i></i><i></i><i></i><i></i><i></i><i></i>'
        '</div>'
        '</div>'

        '</div>',
        unsafe_allow_html=True,
    )


def section_heading(title, subtitle=""):
    st.markdown(
        f'<div class="mi-section-title">{_e(title)}</div>'
        f'<div class="mi-section-sub">{_e(subtitle)}</div>',
        unsafe_allow_html=True,
    )


def mode_card(mode, icon, description):
    cls = str(mode).lower()

    st.markdown(
        f'<div class="mi-mode-card mi-{cls}">'
        f'<div class="mi-mode-icon">{_e(icon)}</div>'
        f'<b>{_e(mode)}</b>'
        f'<p>{_e(description)}</p>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# MODE BADGES
# ============================================================

def badge(mode):
    key = str(mode).lower()

    icons = {
        "focus": "☾",
        "energy": "⚡",
        "inspiration": "✧",
    }

    icon = icons.get(key, "♫")

    st.markdown(
        '<div class="mi-center">'
        f'<span class="mi-badge {key}">'
        f'{icon} {_e(mode).upper()} MODE'
        '</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# RECOMMENDATION CARDS
# ============================================================

def song_card(
    rank,
    title,
    artist,
    energy,
    tempo,
    valence,
    why,
    art_url=None,
    is_seed=False,
):
    if art_url:
        art = (
            f'<img class="mi-art" src="{_e(art_url)}" alt="Album artwork">'
        )
    else:
        art = '<div class="mi-art">♫</div>'

    seed = (
        '<span class="mi-badge seed">✦ From your picks</span>'
        if is_seed
        else ""
    )

    markup = (
        '<div class="mi-card">'
        '<div class="mi-head">'

        f'<div class="mi-rank">{_e(rank)}</div>'
        f'{art}'

        '<div class="mi-meta">'
        f'<div class="mi-track">{_e(title)}</div>'
        f'<div class="mi-artist">{_e(artist)}</div>'

        '<div class="mi-sig">'
        f'<span class="mi-chip">'
        f'<span class="k">Energy</span>'
        f'<span class="v">{_e(energy)}</span>'
        '</span>'

        f'<span class="mi-chip">'
        f'<span class="k">Tempo</span>'
        f'<span class="v">{_e(tempo)} BPM</span>'
        '</span>'

        f'<span class="mi-chip">'
        f'<span class="k">Valence</span>'
        f'<span class="v">{_e(valence)}</span>'
        '</span>'

        f'{seed}'
        '</div>'
        '</div>'
        '</div>'

        '<div class="mi-why">'
        '<div class="l">A LITTLE NOTE ABOUT THIS TRACK ✧</div>'
        f'<div class="b">{_e(why)}</div>'
        '</div>'

        '</div>'
    )

    st.markdown(markup, unsafe_allow_html=True)


# ============================================================
# COMPLETION
# ============================================================

def complete(
    title="Thanks for listening.",
    body="Your anonymous feedback has been recorded.",
):
    st.markdown(
        '<div class="mi-complete">'
        '<div class="mi-decor d1">✦</div>'
        '<div class="mi-check">✓</div>'
        f'<h1>{_e(title)}</h1>'
        f'<p style="color:#817B9D">{_e(body)}</p>'
        '<div style="font-size:1.4rem;letter-spacing:12px;'
        'color:#B3A6E9;margin-top:15px">✧ ♡ ✧</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

def footer():
    st.markdown(
        '<div class="mi-footer">'
        'MADE FOR YOUR MOMENT · MUSICINTENT ✦'
        '</div>',
        unsafe_allow_html=True,
    )
