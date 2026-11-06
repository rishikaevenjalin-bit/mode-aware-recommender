if st.session_state.step == "welcome":
    inject_css()

    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #F7FAFF 0%, #F0F0FF 42%, #F6F0FF 72%, #FFF4FB 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 4rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, div, span {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .mi-hero {
        position: relative;
        text-align: center;
        padding: 55px 35px 38px;
        margin: 0 auto 38px;
        border: 1px solid rgba(255,255,255,0.8);
        border-radius: 32px;
        background: rgba(255,255,255,0.42);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 15px 50px rgba(105,100,180,0.07);
        overflow: hidden;
    }

    .mi-hero:before {
        content: '';
        position: absolute;
        width: 240px;
        height: 240px;
        border-radius: 50%;
        background: rgba(216,221,255,0.35);
        filter: blur(45px);
        top: -100px;
        left: -65px;
    }

    .mi-hero:after {
        content: '';
        position: absolute;
        width: 230px;
        height: 230px;
        border-radius: 50%;
        background: rgba(255,203,242,0.35);
        filter: blur(45px);
        bottom: -130px;
        right: -65px;
    }

    .mi-hero-inner {
        position: relative;
        z-index: 1;
    }

    .mi-eyebrow {
        display: inline-block;
        padding: 8px 17px;
        border-radius: 30px;
        background: rgba(138,127,232,0.10);
        color: #766ACF;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 19px;
    }

    .mi-title {
        color: #1B2140;
        font-size: clamp(42px, 6vw, 65px);
        font-weight: 800;
        letter-spacing: -3px;
        line-height: 1.15;
        margin: 0 0 15px;
    }

    .mi-title span {
        background: linear-gradient(100deg, #8A7FE8, #D46BB3);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .mi-tagline {
        color: #5C6485;
        font-size: 18px;
        font-weight: 500;
        margin: 0 0 17px;
    }

    .mi-description {
        max-width: 680px;
        margin: 0 auto;
        color: #747B99;
        font-size: 14px;
        line-height: 1.9;
    }

    .mi-section-heading {
        color: #1B2140;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        margin: 0 0 7px;
    }

    .mi-section-sub {
        color: #858BA5;
        font-size: 13px;
        text-align: center;
        margin-bottom: 25px;
    }

    .mi-mode-card {
        min-height: 210px;
        padding: 27px 19px;
        text-align: center;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.88);
        background: rgba(255,255,255,0.55);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(83,76,150,0.055);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .mi-mode-card:hover {
        transform: translateY(-7px);
        box-shadow: 0 17px 35px rgba(83,76,150,0.12);
    }

    .mi-mode-icon {
        width: 57px;
        height: 57px;
        margin: 0 auto 17px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 19px;
        font-size: 25px;
    }

    .mi-mode-name {
        color: #1B2140;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 9px;
    }

    .mi-mode-desc {
        color: #737B98;
        font-size: 12px;
        line-height: 1.8;
    }

    .mi-focus .mi-mode-icon {
        background: #D8DDFF;
        color: #3B45A8;
    }

    .mi-energy .mi-mode-icon {
        background: #FFCBF2;
        color: #9E3B78;
    }

    .mi-inspiration .mi-mode-icon {
        background: #E5D3FF;
        color: #6A3AAF;
    }

    div.stButton {
        display: flex;
        justify-content: center;
        margin-top: 25px;
    }

    div.stButton > button {
        background: linear-gradient(110deg, #8A7FE8, #B58AE8, #D46BB3);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 14px 43px;
        min-height: 53px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.3px;
        box-shadow: 0 9px 25px rgba(138,127,232,0.27);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        color: white;
        border: none;
        transform: translateY(-3px);
        box-shadow: 0 13px 30px rgba(138,127,232,0.38);
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 1.5rem;
        }
        .mi-hero {
            padding: 38px 20px;
            border-radius: 25px;
        }
        .mi-title {
            letter-spacing: -2px;
        }
        .mi-tagline {
            font-size: 15px;
        }
        .mi-mode-card {
            min-height: 190px;
            padding: 20px 10px;
        }
    }
    </style>""", unsafe_allow_html=True)

    st.markdown("""<div class="mi-hero"><div class="mi-hero-inner"><div class="mi-eyebrow">✦ MUSIC DISCOVERY, REIMAGINED ✦</div><h1 class="mi-title">Music<span>Intent</span></h1><p class="mi-tagline">Music that understands your moment.</p><p class="mi-description">Most music apps recommend songs based on your general taste. MusicIntent takes a different approach. Choose what you're listening for, discover music that matches your intent, and explore personalised recommendations with an explanation for every track.</p></div></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="mi-section-heading">Find your listening mood</div><div class="mi-section-sub">Three ways to experience music, one personalised journey.</div>""", unsafe_allow_html=True)

    _w1, _w2, _w3 = st.columns(3, gap="medium")

    with _w1:
        st.markdown("""<div class="mi-mode-card mi-focus"><div class="mi-mode-icon">☾</div><div class="mi-mode-name">Focus</div><div class="mi-mode-desc">Calm, low-distraction music for concentration and deep work.</div></div>""", unsafe_allow_html=True)

    with _w2:
        st.markdown("""<div class="mi-mode-card mi-energy"><div class="mi-mode-icon">⚡</div><div class="mi-mode-name">Energy</div><div class="mi-mode-desc">Upbeat, high-tempo tracks for workouts and motivation.</div></div>""", unsafe_allow_html=True)

    with _w3:
        st.markdown("""<div class="mi-mode-card mi-inspiration"><div class="mi-mode-icon">✧</div><div class="mi-mode-name">Inspiration</div><div class="mi-mode-desc">Critically acclaimed music for discovery and exploration.</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    if st.button("Get Started  →", use_container_width=False):
        st.session_state.step = "setup"
        st.rerun()
        