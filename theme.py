import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root{
  --bg-primary:#F7FAFF; --bg-secondary:#F6F0FF; --bg-tertiary:#FFF4FB;
  --glass:rgba(255,255,255,0.60); --glass-strong:rgba(255,255,255,0.82); --glass-soft:rgba(255,255,255,0.42);
  --border-glass:rgba(255,255,255,0.70); --border-hair:rgba(27,33,64,0.07);
  --text-primary:#1B2140; --text-secondary:#5C6485; --text-tertiary:#8A91AC;
  --accent-primary:#8A7FE8; --accent-primary-soft:#D0D1FF; --accent-secondary:#D46BB3; --accent-secondary-soft:#FFCBF2;
  --focus-accent:#6E7BE8; --focus-soft:#D8DDFF; --focus-ink:#3B45A8;
  --energy-accent:#D46BB3; --energy-soft:#FFCBF2; --energy-ink:#9E3B78;
  --inspiration-accent:#9B6BE8; --inspiration-soft:#E5D3FF; --inspiration-ink:#6A3AAF;
  --shadow-sm:0 2px 10px rgba(70,60,130,0.06); --shadow-md:0 8px 28px rgba(70,60,130,0.09);
  --shadow-lg:0 16px 48px rgba(70,60,130,0.13); --glow:0 0 0 4px rgba(138,127,232,0.16);
  --r-sm:12px; --r-md:16px; --r-lg:22px; --r-xl:28px; --ease:cubic-bezier(0.23,1,0.32,1);
}
.stApp{
  background:
    radial-gradient(760px 520px at 12% -6%, rgba(200,231,255,0.55), transparent 62%),
    radial-gradient(680px 480px at 92% 8%, rgba(243,196,251,0.42), transparent 62%),
    radial-gradient(720px 600px at 50% 108%, rgba(208,209,255,0.45), transparent 62%),
    linear-gradient(135deg,var(--bg-primary) 0%,var(--bg-secondary) 52%,var(--bg-tertiary) 100%);
  background-attachment:fixed;
}
header[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stDecoration"]{display:none;}
.block-container{max-width:960px;padding:2.4rem 1.4rem 5rem;}
html,body,.stApp,button,input,textarea,select,[class*="css"]{
  font-family:'Plus Jakarta Sans',ui-sans-serif,-apple-system,sans-serif!important;
  color:var(--text-primary); -webkit-font-smoothing:antialiased;
}
h1,h2,h3,h4{color:var(--text-primary)!important;letter-spacing:-0.02em;}
h1{font-size:2.5rem!important;font-weight:800!important;line-height:1.14!important;}
h2{font-size:1.5rem!important;font-weight:700!important;}
h3{font-size:1.15rem!important;font-weight:700!important;}
p,li,label{color:var(--text-primary);line-height:1.62;}
[data-testid="stCaptionContainer"] p{color:var(--text-secondary)!important;font-size:.88rem!important;}
.badge{display:inline-flex;align-items:center;gap:7px;padding:7px 15px;border-radius:999px;font-size:.76rem;font-weight:700;letter-spacing:.06em;border:1px solid var(--border-glass);}
.badge.focus{background:var(--focus-soft);color:var(--focus-ink);}
.badge.energy{background:var(--energy-soft);color:var(--energy-ink);}
.badge.inspiration{background:var(--inspiration-soft);color:var(--inspiration-ink);}
.song-card{background:var(--glass);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid var(--border-glass);border-radius:var(--r-lg);box-shadow:var(--shadow-sm);padding:18px 20px;margin-bottom:6px;transition:transform 180ms var(--ease),box-shadow 180ms var(--ease);}
.song-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-md);}
.song-card.is-seed{border-color:rgba(138,127,232,0.42);box-shadow:var(--shadow-md);}
.song-head{display:flex;align-items:center;gap:16px;}
.song-rank{flex:0 0 34px;height:34px;border-radius:11px;background:var(--glass-strong);border:1px solid var(--border-hair);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;color:var(--accent-primary);}
.song-meta{flex:1 1 auto;min-width:0;}
.song-title{font-size:1.08rem;font-weight:700;line-height:1.3;}
.song-artist{font-size:.9rem;color:var(--text-secondary);margin-top:2px;}
.song-tags{display:flex;flex-wrap:wrap;gap:7px;margin-top:9px;}
.explanation-card{background:linear-gradient(135deg,rgba(255,255,255,0.78),rgba(243,241,255,0.62));border:1px solid var(--border-glass);border-radius:var(--r-md);padding:17px 19px;margin-top:14px;}
.explanation-card .exp-label{font-size:.68rem;font-weight:700;letter-spacing:.12em;color:var(--accent-primary);margin-bottom:8px;}
.explanation-card .exp-body{font-size:.93rem;line-height:1.62;color:#3D4568;}
.stButton>button,.stFormSubmitButton>button,[data-testid="stLinkButton"]>a{width:100%;border-radius:14px;font-weight:700;font-size:.97rem;padding:.68rem 1.1rem;border:1px solid var(--border-glass);background:var(--glass-strong);color:var(--text-primary)!important;box-shadow:var(--shadow-sm);text-decoration:none!important;transition:transform 150ms var(--ease),box-shadow 150ms var(--ease),background 150ms var(--ease);}
.stButton>button:hover,.stFormSubmitButton>button:hover,[data-testid="stLinkButton"]>a:hover{transform:translateY(-2px);box-shadow:var(--shadow-md);background:#fff;}
.stButton>button[kind="primary"]{background:linear-gradient(90deg,#9B93F0 0%,#C9A8F0 55%,#E9A9D6 100%);color:#fff!important;border:none;box-shadow:0 8px 24px rgba(138,127,232,0.34);}
[class*="st-key-spotify"] a,[class*="st-key-spotify"] button{background:rgba(29,185,84,0.11)!important;border:1px solid rgba(29,185,84,0.35)!important;color:#0F7C39!important;font-size:.87rem!important;box-shadow:none!important;}
[class*="st-key-youtube"] a,[class*="st-key-youtube"] button{background:rgba(226,63,63,0.09)!important;border:1px solid rgba(226,63,63,0.30)!important;color:#B02626!important;font-size:.87rem!important;box-shadow:none!important;}
[class*="st-key-like"] button,[class*="st-key-dislike"] button{background:var(--glass-soft)!important;border:1px solid var(--border-hair)!important;color:var(--text-secondary)!important;font-size:.87rem!important;font-weight:600!important;box-shadow:none!important;border-radius:999px!important;}
[class*="st-key-like"] button:hover{background:rgba(208,209,255,0.5)!important;color:var(--focus-ink)!important;}
[class*="st-key-dislike"] button:hover{background:rgba(255,203,242,0.5)!important;color:var(--energy-ink)!important;}
[data-testid="stMultiSelect"] div[data-baseweb="select"]>div{background:var(--glass-strong)!important;border:1px solid var(--border-glass)!important;border-radius:14px!important;min-height:52px;box-shadow:var(--shadow-sm);}
[data-testid="stMultiSelect"] span[data-baseweb="tag"]{background:linear-gradient(90deg,#A79CF0,#D6A6E8)!important;border-radius:999px!important;color:#fff!important;font-weight:600;}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg{fill:#fff;}
.stTextInput input,.stTextArea textarea{background:var(--glass-strong)!important;border:1px solid var(--border-glass)!important;border-radius:14px!important;color:var(--text-primary)!important;padding:12px 15px!important;}
.stTextArea textarea:focus,.stTextInput input:focus{border-color:var(--accent-primary)!important;box-shadow:var(--glow)!important;}
[data-testid="stRadio"]>div{gap:11px;}
[data-testid="stRadio"] label{background:var(--glass-soft);border:1px solid var(--border-glass);border-radius:var(--r-md);padding:14px 16px;width:100%;box-shadow:var(--shadow-sm);align-items:flex-start;transition:background 160ms var(--ease),border-color 160ms var(--ease),transform 160ms var(--ease);}
[data-testid="stRadio"] label:hover{background:var(--glass);transform:translateY(-1px);}
[data-testid="stRadio"] label:has(input:checked){background:var(--glass-strong);border-color:var(--accent-primary);box-shadow:var(--shadow-md),var(--glow);}
[data-testid="stRadio"] label p{font-weight:600;}
[data-testid="stSlider"] div[role="slider"]{background:var(--accent-primary)!important;box-shadow:0 2px 10px rgba(138,127,232,0.5)!important;}
[data-testid="stSlider"] [data-baseweb="slider"]>div>div{background:var(--accent-primary)!important;}
[data-testid="stTickBarMin"],[data-testid="stTickBarMax"]{color:var(--text-tertiary)!important;font-weight:600;}
[data-testid="stAlert"]{background:var(--glass-strong)!important;border:1px solid var(--border-glass)!important;border-radius:var(--r-md)!important;color:var(--text-primary)!important;box-shadow:var(--shadow-sm);}
hr{border-color:var(--border-hair)!important;}
.mi-complete{text-align:center;padding:34px 0 10px;}
.mi-check{width:104px;height:104px;border-radius:50%;margin:0 auto 24px;background:linear-gradient(135deg,#A79CF0,#D8BBFF 45%,#FFCBF2);display:flex;align-items:center;justify-content:center;color:#fff;font-size:46px;box-shadow:0 14px 40px rgba(138,127,232,0.38);}
@media (max-width:640px){.block-container{padding:1.4rem .9rem 3.5rem;}h1{font-size:1.95rem!important;}.song-head{gap:12px;}.song-title{white-space:normal;}}
</style>
"""

def inject_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
