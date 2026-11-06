import html
import streamlit as st

# Shared visual system for every MusicIntent screen.
# All markup passed to st.markdown is kept on one line for predictable rendering.
_CSS = (
"<style>"
"@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');"
":root{--ink:#202342;--muted:#68708f;--soft:#9299b2;--violet:#897ee8;--pink:#d982bd;--glass:rgba(255,255,255,.62);--glass-strong:rgba(255,255,255,.84);--line:rgba(255,255,255,.82);--shadow:0 18px 55px rgba(89,78,153,.10);--ease:cubic-bezier(.2,.8,.2,1);}"
".stApp{min-height:100vh;background:radial-gradient(ellipse at 8% 5%,rgba(205,224,255,.66),transparent 35%),radial-gradient(ellipse at 92% 8%,rgba(255,210,239,.58),transparent 34%),radial-gradient(ellipse at 55% 100%,rgba(218,207,255,.52),transparent 42%),linear-gradient(135deg,#f8fbff 0%,#f5f1ff 52%,#fff5fb 100%);background-attachment:fixed;}"
"header[data-testid='stHeader']{background:transparent!important;}"
".block-container{max-width:1040px;padding:1.5rem 1.35rem 4rem;}"
"html,body,.stApp,button,input,textarea,[class*='css']{font-family:'Plus Jakarta Sans',ui-sans-serif,-apple-system,sans-serif!important;color:var(--ink);}"
"h1,h2,h3{color:var(--ink)!important;letter-spacing:-.035em;}h1{font-size:clamp(2rem,4vw,2.8rem)!important;font-weight:800!important;}h2{font-weight:800!important;}p,li,label{line-height:1.65;}"
".mi-page-head{text-align:center;margin:0 auto 1.35rem;max-width:760px;}"
".mi-kicker{display:inline-flex;align-items:center;gap:8px;padding:7px 13px;border:1px solid rgba(137,126,232,.16);border-radius:999px;background:rgba(255,255,255,.55);color:#786bd0;font-size:.72rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase;}"
".mi-page-title{font-size:clamp(2rem,4vw,2.8rem);font-weight:800;letter-spacing:-.055em;line-height:1.12;color:var(--ink);margin:14px 0 8px;}"
".mi-page-sub{font-size:.98rem;color:var(--muted);max-width:650px;margin:0 auto;}"
".mi-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(137,126,232,.22),transparent);margin:24px 0;}"
".mi-card{position:relative;background:var(--glass);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);padding:20px 22px;margin:0 0 13px;transition:transform .22s var(--ease),box-shadow .22s var(--ease);}"
".mi-card:hover{transform:translateY(-2px);box-shadow:0 22px 58px rgba(89,78,153,.15);}"
".mi-head{display:flex;align-items:center;gap:15px;}"
".mi-rank{flex:0 0 38px;width:38px;height:38px;border-radius:14px;background:linear-gradient(145deg,#fff,rgba(226,221,255,.85));border:1px solid rgba(137,126,232,.13);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.88rem;color:#8174db;}"
".mi-art{flex:0 0 66px;width:66px;height:66px;border-radius:18px;object-fit:cover;background:linear-gradient(135deg,#d8ddff,#f8d7f0);display:flex;align-items:center;justify-content:center;font-size:27px;color:#776bd0;box-shadow:inset 0 0 0 1px rgba(255,255,255,.7);}"
".mi-meta{flex:1 1 auto;min-width:0;}"
".mi-track-title{font-size:1.08rem;font-weight:800;line-height:1.3;overflow-wrap:anywhere;color:var(--ink);}"
".mi-artist{font-size:.9rem;color:var(--muted);margin-top:3px;}"
".mi-sig{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px;}"
".mi-chip{background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.9);border-radius:999px;padding:6px 11px;font-size:.76rem;}"
".mi-chip .k{color:var(--soft);font-weight:600;}.mi-chip .v{color:var(--ink);font-weight:800;margin-left:5px;}"
".mi-why{background:linear-gradient(120deg,rgba(255,255,255,.76),rgba(242,239,255,.68));border:1px solid rgba(255,255,255,.9);border-radius:17px;padding:14px 16px;margin-top:16px;}"
".mi-why-label{font-size:.66rem;font-weight:800;letter-spacing:.14em;color:#897ee8;margin-bottom:5px;}.mi-why-copy{font-size:.91rem;line-height:1.65;color:#454c70;}"
".mi-badge-wrap{text-align:center;margin:2px 0 12px;}"
".mi-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;font-size:.75rem;font-weight:800;letter-spacing:.09em;border:1px solid rgba(255,255,255,.9);box-shadow:0 5px 18px rgba(89,78,153,.07);}"
".mi-badge.focus{background:#e4e7ff;color:#454da4;}.mi-badge.energy{background:#ffe2f4;color:#a0447d;}.mi-badge.inspiration{background:#eee2ff;color:#7048ae;}"
".mi-badge.seed{background:linear-gradient(90deg,#e4e5ff,#ffe4f4);color:#66569c;letter-spacing:0;font-size:.68rem;padding:5px 9px;}"
".stButton>button,.stFormSubmitButton>button,[data-testid='stLinkButton']>a{width:100%;min-height:43px;border-radius:14px;font-weight:700;font-size:.88rem;padding:.62rem 1rem;border:1px solid rgba(255,255,255,.92);background:rgba(255,255,255,.72);color:var(--ink)!important;box-shadow:0 5px 16px rgba(89,78,153,.06);text-decoration:none!important;transition:transform .18s var(--ease),box-shadow .18s var(--ease),background .18s ease;}"
".stButton>button:hover,[data-testid='stLinkButton']>a:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(89,78,153,.12);border-color:rgba(137,126,232,.25);}"
".stButton>button[kind='primary'],.stFormSubmitButton>button[kind='primary']{background:linear-gradient(105deg,#897ee8,#b394eb 58%,#df9bc9);color:#fff!important;border:none;box-shadow:0 10px 26px rgba(137,126,232,.28);}"
"[class*='st-key-spotify'] a{background:rgba(36,183,97,.09)!important;border:1px solid rgba(36,183,97,.22)!important;color:#187744!important;}"
"[class*='st-key-youtube'] a{background:rgba(235,74,74,.08)!important;border:1px solid rgba(235,74,74,.2)!important;color:#b33b3b!important;}"
"[class*='st-key-like'] button{background:rgba(137,126,232,.10)!important;color:#6e62c2!important;border-color:rgba(137,126,232,.15)!important;}"
"[class*='st-key-dislike'] button{background:rgba(255,255,255,.6)!important;color:#747b95!important;}"
"[data-testid='stMultiSelect'] div[data-baseweb='select']>div,.stSelectbox div[data-baseweb='select']>div{background:rgba(255,255,255,.82)!important;border:1px solid rgba(255,255,255,.95)!important;border-radius:15px!important;min-height:48px;box-shadow:0 5px 18px rgba(89,78,153,.04);}"
"[data-testid='stMultiSelect'] span[data-baseweb='tag']{background:linear-gradient(90deg,#9388e9,#c69bdf)!important;border-radius:999px!important;color:#fff!important;}"
"div[data-baseweb='popover'] ul[role='listbox']{background:rgba(255,255,255,.98)!important;border-radius:16px!important;box-shadow:0 16px 48px rgba(70,60,130,.16)!important;}"
"div[data-baseweb='popover'] li{color:var(--ink)!important;}"
".stTextInput input,.stTextArea textarea{background:rgba(255,255,255,.82)!important;border:1px solid rgba(255,255,255,.95)!important;border-radius:14px!important;color:var(--ink)!important;}"
"[data-testid='stRadio']>div{gap:10px;}"
"[data-testid='stRadio'] label{background:rgba(255,255,255,.53);border:1px solid rgba(255,255,255,.9);border-radius:15px;padding:11px 14px;width:100%;}"
"[data-testid='stRadio'] label:has(input:checked){background:rgba(255,255,255,.9);border-color:rgba(137,126,232,.55);box-shadow:0 0 0 3px rgba(137,126,232,.10);}"
"[data-testid='stSlider'] div[role='slider']{background:var(--violet)!important;}"
"[data-testid='stSlider'] [data-baseweb='slider']>div>div{background:var(--violet)!important;}"
".stAlert{border-radius:15px!important;}"
".mi-success-orb{width:86px;height:86px;border-radius:30px;margin:0 auto 18px;background:linear-gradient(145deg,#a99ff0,#d7b9f0 55%,#f4c5e4);display:flex;align-items:center;justify-content:center;color:white;font-size:38px;box-shadow:0 14px 38px rgba(137,126,232,.28);transform:rotate(-7deg);}"
".mi-footnote{text-align:center;color:#9298b0;font-size:.75rem;margin-top:25px;}"
"@media(max-width:640px){.block-container{padding:1rem .8rem 3rem;}.mi-card{padding:16px;border-radius:20px;}.mi-art{flex:0 0 54px;width:54px;height:54px;border-radius:15px;}.mi-rank{flex-basis:32px;width:32px;height:32px;}.mi-chip{font-size:.72rem;padding:5px 9px;}.mi-page-sub{font-size:.9rem;}}"
"</style>"
)

def theme():
    st.markdown(_CSS, unsafe_allow_html=True)

def _e(value):
    return html.escape(str(value))

def page_header(kicker, title, subtitle):
    markup = ('<div class="mi-page-head"><div class="mi-kicker">✦ ' + _e(kicker) +
              ' ✦</div><div class="mi-page-title">' + _e(title) +
              '</div><div class="mi-page-sub">' + _e(subtitle) + '</div></div>')
    st.markdown(markup, unsafe_allow_html=True)

def badge(mode):
    key = str(mode).lower()
    icon = {"focus": "☾", "energy": "ϟ", "inspiration": "✧"}.get(key, "✧")
    st.markdown('<div class="mi-badge-wrap"><span class="mi-badge ' + _e(key) + '">' + icon + ' ' + _e(mode).upper() + ' MODE</span></div>', unsafe_allow_html=True)

def song_card(rank, title, artist, energy, tempo, valence, why, art_url=None, is_seed=False):
    art = '<img class="mi-art" src="' + _e(art_url) + '" alt="">' if art_url else '<div class="mi-art">♫</div>'
    seed = '<span class="mi-badge seed">✦ From your picks</span>' if is_seed else ''
    markup = ('<div class="mi-card"><div class="mi-head"><div class="mi-rank">' + _e(rank) +
              '</div>' + art + '<div class="mi-meta"><div class="mi-track-title">' + _e(title) +
              '</div><div class="mi-artist">' + _e(artist) + '</div><div class="mi-sig">' +
              '<span class="mi-chip"><span class="k">Energy</span><span class="v">' + _e(energy) + '</span></span>' +
              '<span class="mi-chip"><span class="k">Tempo</span><span class="v">' + _e(tempo) + ' BPM</span></span>' +
              '<span class="mi-chip"><span class="k">Valence</span><span class="v">' + _e(valence) + '</span></span>' +
              seed + '</div></div></div><div class="mi-why"><div class="mi-why-label">WHY THIS TRACK</div>' +
              '<div class="mi-why-copy">' + _e(why) + '</div></div></div>')
    st.markdown(markup, unsafe_allow_html=True)

def complete(title="Thanks for listening.", body="Your anonymous feedback has been recorded."):
    markup = ('<div style="text-align:center;padding:34px 0 12px;"><div class="mi-success-orb">✓</div><h1>' +
              _e(title) + '</h1><p style="color:#68708f;font-size:1rem;">' + _e(body) + '</p></div>')
    st.markdown(markup, unsafe_allow_html=True)
