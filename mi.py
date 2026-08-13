import html
import streamlit as st

_CSS = (
"<style>"
"@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');"
":root{--ink:#1B2140;--ink2:#5C6485;--ink3:#8A91AC;--acc:#8A7FE8;--glass:rgba(255,255,255,0.66);--glass2:rgba(255,255,255,0.85);--bd:rgba(255,255,255,0.75);--hair:rgba(27,33,64,0.07);--sh:0 8px 28px rgba(70,60,130,0.10);--ease:cubic-bezier(0.23,1,0.32,1);}"
".stApp{background:radial-gradient(760px 520px at 12% -6%,rgba(200,231,255,0.55),transparent 62%),radial-gradient(680px 480px at 92% 8%,rgba(243,196,251,0.42),transparent 62%),radial-gradient(720px 600px at 50% 108%,rgba(208,209,255,0.45),transparent 62%),linear-gradient(135deg,#F7FAFF 0%,#F6F0FF 52%,#FFF4FB 100%);background-attachment:fixed;}"
"header[data-testid='stHeader']{background:transparent!important;}"
".block-container{max-width:900px;padding:2.2rem 1.2rem 4rem;}"
"html,body,.stApp,button,input,textarea,select,[class*='css']{font-family:'Plus Jakarta Sans',ui-sans-serif,-apple-system,sans-serif!important;color:var(--ink);}"
"h1,h2,h3{color:var(--ink)!important;letter-spacing:-0.02em;}h1{font-size:2.4rem!important;font-weight:800!important;}"
"p,li,label{color:var(--ink);line-height:1.6;}"
".mi-center{text-align:center;}"
".mi-badge{display:inline-flex;align-items:center;gap:7px;padding:7px 16px;border-radius:999px;font-size:.76rem;font-weight:700;letter-spacing:.06em;border:1px solid var(--bd);}"
".mi-badge.focus{background:#D8DDFF;color:#3B45A8;}.mi-badge.energy{background:#FFCBF2;color:#9E3B78;}.mi-badge.inspiration{background:#E5D3FF;color:#6A3AAF;}"
".mi-badge.seed{background:linear-gradient(90deg,#D0D1FF,#FFCBF2);color:#4A3A78;letter-spacing:0;}"
".mi-card{background:var(--glass);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid var(--bd);border-radius:22px;box-shadow:var(--sh);padding:18px 20px;margin:0 0 10px;transition:transform 180ms var(--ease),box-shadow 180ms var(--ease);}"
".mi-card:hover{transform:translateY(-2px);box-shadow:0 16px 44px rgba(70,60,130,0.14);}"
".mi-head{display:flex;align-items:center;gap:15px;}"
".mi-rank{flex:0 0 34px;height:34px;border-radius:11px;background:var(--glass2);border:1px solid var(--hair);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;color:var(--acc);}"
".mi-art{flex:0 0 62px;width:62px;height:62px;border-radius:13px;object-fit:cover;background:linear-gradient(135deg,#D0D1FF,#FFCBF2);display:flex;align-items:center;justify-content:center;font-size:24px;color:#6A5FB8;}"
".mi-meta{flex:1 1 auto;min-width:0;}"
".mi-title{font-size:1.08rem;font-weight:700;line-height:1.3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}"
".mi-artist{font-size:.9rem;color:var(--ink2);margin-top:2px;}"
".mi-sig{display:flex;flex-wrap:wrap;gap:7px;margin-top:9px;}"
".mi-chip{background:var(--glass2);border:1px solid var(--hair);border-radius:10px;padding:5px 10px;font-size:.78rem;}"
".mi-chip .k{color:var(--ink3);font-weight:600;}.mi-chip .v{color:var(--ink);font-weight:700;margin-left:5px;}"
".mi-why{background:linear-gradient(135deg,rgba(255,255,255,0.80),rgba(243,241,255,0.60));border:1px solid var(--bd);border-radius:16px;padding:15px 17px;margin-top:14px;}"
".mi-why .l{font-size:.66rem;font-weight:700;letter-spacing:.12em;color:var(--acc);margin-bottom:6px;}"
".mi-why .b{font-size:.93rem;line-height:1.6;color:#3D4568;}"
".stButton>button,.stFormSubmitButton>button,[data-testid='stLinkButton']>a{width:100%;border-radius:14px;font-weight:700;font-size:.95rem;padding:.62rem 1rem;border:1px solid var(--bd);background:var(--glass2);color:var(--ink)!important;box-shadow:0 2px 10px rgba(70,60,130,0.06);text-decoration:none!important;transition:transform 150ms var(--ease),box-shadow 150ms var(--ease);}"
".stButton>button:hover,[data-testid='stLinkButton']>a:hover{transform:translateY(-2px);box-shadow:var(--sh);}"
".stButton>button[kind='primary'],.stFormSubmitButton>button[kind='primary']{background:linear-gradient(90deg,#9B93F0,#C9A8F0 55%,#E9A9D6);color:#fff!important;border:none;box-shadow:0 8px 24px rgba(138,127,232,0.34);}"
"[class*='st-key-spotify'] a{background:rgba(29,185,84,0.11)!important;border:1px solid rgba(29,185,84,0.35)!important;color:#0F7C39!important;}"
"[class*='st-key-youtube'] a{background:rgba(226,63,63,0.09)!important;border:1px solid rgba(226,63,63,0.30)!important;color:#B02626!important;}"
"[class*='st-key-like'] button,[class*='st-key-dislike'] button{border-radius:999px!important;background:rgba(255,255,255,0.5)!important;color:var(--ink2)!important;font-weight:600!important;box-shadow:none!important;}"
"[data-testid='stMultiSelect'] div[data-baseweb='select']>div,.stSelectbox div[data-baseweb='select']>div{background:var(--glass2)!important;border:1px solid var(--bd)!important;border-radius:14px!important;min-height:50px;}"
"[data-testid='stMultiSelect'] span[data-baseweb='tag']{background:linear-gradient(90deg,#A79CF0,#D6A6E8)!important;border-radius:999px!important;color:#fff!important;}"
"div[data-baseweb='popover'] ul[role='listbox']{background:rgba(255,255,255,0.97)!important;border-radius:16px!important;box-shadow:0 16px 48px rgba(70,60,130,0.16)!important;}"
"div[data-baseweb='popover'] li{color:var(--ink)!important;}"
".stTextInput input,.stTextArea textarea{background:var(--glass2)!important;border:1px solid var(--bd)!important;border-radius:14px!important;color:var(--ink)!important;}"
"[data-testid='stRadio'] label{background:rgba(255,255,255,0.45);border:1px solid var(--bd);border-radius:16px;padding:13px 15px;width:100%;}"
"[data-testid='stRadio'] label:has(input:checked){background:var(--glass2);border-color:var(--acc);box-shadow:0 0 0 4px rgba(138,127,232,0.16);}"
"[data-testid='stSlider'] div[role='slider']{background:var(--acc)!important;}"
"[data-testid='stSlider'] [data-baseweb='slider']>div>div{background:var(--acc)!important;}"
".mi-check{width:100px;height:100px;border-radius:50%;margin:0 auto 22px;background:linear-gradient(135deg,#A79CF0,#D8BBFF 45%,#FFCBF2);display:flex;align-items:center;justify-content:center;color:#fff;font-size:44px;box-shadow:0 14px 40px rgba(138,127,232,0.38);}"
"@media(max-width:640px){.mi-title{white-space:normal;}.mi-art{flex:0 0 50px;width:50px;height:50px;}}"
"</style>"
)


def theme():
    st.markdown(_CSS, unsafe_allow_html=True)


def _e(v):
    return html.escape(str(v))


def badge(mode):
    icon = {"focus": "\u25CE", "energy": "\u26A1", "inspiration": "\u2726"}.get(mode.lower(), "\u2726")
    h = ('<div class="mi-center"><span class="mi-badge ' + mode.lower() + '">'
         + icon + " " + _e(mode).upper() + "</span></div>")
    st.markdown(h, unsafe_allow_html=True)


def song_card(rank, title, artist, energy, tempo, valence, why,
              art_url=None, is_seed=False):
    art = ('<img class="mi-art" src="' + _e(art_url) + '" alt="">') if art_url \
        else '<div class="mi-art">&#9834;</div>'
    seed = '<span class="mi-badge seed">&#10022; From your picks</span>' if is_seed else ""
    h = (
        '<div class="mi-card"><div class="mi-head">'
        '<div class="mi-rank">' + _e(rank) + '</div>' + art +
        '<div class="mi-meta">'
        '<div class="mi-title">' + _e(title) + '</div>'
        '<div class="mi-artist">' + _e(artist) + '</div>'
        '<div class="mi-sig">'
        '<span class="mi-chip"><span class="k">Energy</span><span class="v">' + _e(energy) + '</span></span>'
        '<span class="mi-chip"><span class="k">Tempo</span><span class="v">' + _e(tempo) + ' BPM</span></span>'
        '<span class="mi-chip"><span class="k">Valence</span><span class="v">' + _e(valence) + '</span></span>'
        + seed +
        '</div></div></div>'
        '<div class="mi-why"><div class="l">WHY THIS TRACK</div>'
        '<div class="b">' + _e(why) + '</div></div>'
        '</div>'
    )
    st.markdown(h, unsafe_allow_html=True)


def complete(title="Thanks for listening.", body="Your anonymous feedback has been recorded."):
    h = ('<div class="mi-center" style="padding:34px 0 8px;">'
         '<div class="mi-check">&#10003;</div>'
         '<h1>' + _e(title) + '</h1>'
         '<p style="color:#5C6485;font-size:1.05rem;">' + _e(body) + '</p></div>')
    st.markdown(h, unsafe_allow_html=True)
