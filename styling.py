import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');

    :root{
      --mi-navy:#172033;
      --mi-muted:#5A6478;
      --mi-mauve:#B4A7C3;
      --mi-rose:#E8BCC8;
      --mi-sage:#A8C9BB;
      --mi-peach:#F0B89A;
      --mi-card:rgba(255,255,255,0.62);
      --mi-card-strong:rgba(255,255,255,0.86);
      --mi-border:rgba(255,255,255,0.75);
      --mi-shadow:0 8px 24px rgba(23,32,51,0.07);
      --mi-radius:18px;
    }

    .stApp{
      background:linear-gradient(180deg,#F7FBFF 0%,#EEF3FC 45%,#F9EEF5 100%);
      background-attachment:fixed;
    }
    header[data-testid="stHeader"]{background:transparent;}
    [data-testid="stToolbar"]{right:12px;}
    .block-container{max-width:720px;padding-top:2.2rem;padding-bottom:4rem;}

    html,body,[class*="css"],.stApp,button,input,textarea,select{
      font-family:'Quicksand',ui-rounded,-apple-system,sans-serif !important;
      color:var(--mi-navy);
    }
    h1,h2,h3,h4{color:var(--mi-navy) !important;font-weight:700 !important;letter-spacing:-0.01em;}
    h1{font-size:2rem !important;line-height:1.25 !important;}
    h2{font-size:1.35rem !important;}
    p,li,label,.stMarkdown{color:var(--mi-navy);line-height:1.6;}
    [data-testid="stCaptionContainer"] p{color:var(--mi-muted) !important;font-size:0.86rem !important;}

    .mi-card{
      background:var(--mi-card);
      border:1px solid var(--mi-border);
      border-radius:var(--mi-radius);
      box-shadow:var(--mi-shadow);
      padding:16px 18px;
      margin-bottom:12px;
    }

    .mi-badge{
      display:inline-flex;align-items:center;gap:8px;
      padding:7px 16px;border-radius:999px;
      font-size:0.78rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
    }
    .mi-badge.focus{background:rgba(168,201,187,0.28);color:#2F6B55;}
    .mi-badge.energy{background:rgba(240,184,154,0.30);color:#A85A2A;}
    .mi-badge.inspiration{background:rgba(232,188,200,0.32);color:#9B4A67;}

    .mi-song{
      background:var(--mi-card);
      border:1px solid var(--mi-border);
      border-radius:var(--mi-radius);
      box-shadow:var(--mi-shadow);
      padding:14px 16px;margin-bottom:10px;
    }
    .mi-song-top{display:flex;align-items:flex-start;gap:14px;}
    .mi-rank{
      flex:0 0 30px;height:30px;border-radius:10px;
      background:rgba(180,167,195,0.22);color:#6B5E7D;
      display:flex;align-items:center;justify-content:center;
      font-weight:700;font-size:0.85rem;
    }
    .mi-song-main{flex:1 1 auto;min-width:0;}
    .mi-track{font-size:1.02rem;font-weight:700;color:var(--mi-navy);
      overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
    .mi-artist{font-size:0.85rem;color:var(--mi-muted);margin-top:2px;
      overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
    .mi-metrics{display:flex;gap:8px;margin-top:11px;flex-wrap:wrap;}
    .mi-metric{
      background:rgba(255,255,255,0.72);
      border:1px solid rgba(23,32,51,0.06);
      border-radius:10px;padding:6px 10px;min-width:74px;
    }
    .mi-metric-label{font-size:0.66rem;letter-spacing:0.06em;text-transform:uppercase;color:var(--mi-muted);}
    .mi-metric-value{font-size:0.92rem;font-weight:700;color:var(--mi-navy);margin-top:1px;}
    .mi-why{
      margin-top:12px;padding-top:11px;
      border-top:1px solid rgba(23,32,51,0.07);
      font-size:0.87rem;line-height:1.55;color:#3A465C;
    }
    .mi-why b{color:var(--mi-navy);font-weight:700;}

    .stButton>button,.stFormSubmitButton>button{
      width:100%;
      background:linear-gradient(90deg,#A9B6E8 0%,#B4A7C3 100%);
      color:#fff !important;border:none;border-radius:14px;
      padding:0.72rem 1.1rem;font-weight:700;font-size:1rem;
      box-shadow:0 6px 18px rgba(180,167,195,0.38);
      transition:transform 140ms ease-out, box-shadow 140ms ease-out, filter 140ms ease-out;
    }
    .stButton>button:hover,.stFormSubmitButton>button:hover{
      filter:brightness(1.04);
      box-shadow:0 8px 22px rgba(232,188,200,0.5);
      transform:translateY(-1px);color:#fff !important;
    }
    .stButton>button:active{transform:translateY(0);}
    .stButton>button[kind="secondary"]{
      background:var(--mi-card-strong);color:var(--mi-navy) !important;
      border:1px solid rgba(23,32,51,0.08);box-shadow:var(--mi-shadow);
    }

    [data-testid="stMultiSelect"] div[data-baseweb="select"]>div{
      background:var(--mi-card-strong);
      border:1px solid rgba(23,32,51,0.10) !important;
      border-radius:14px;min-height:48px;box-shadow:var(--mi-shadow);
    }
    [data-testid="stMultiSelect"] span[data-baseweb="tag"]{
      background:var(--mi-mauve) !important;border-radius:999px;color:#fff !important;font-weight:600;
    }

    [data-testid="stRadio"]>div{gap:10px;}
    [data-testid="stRadio"] label{
      background:var(--mi-card);border:1px solid var(--mi-border);
      border-radius:14px;padding:12px 14px;width:100%;
      box-shadow:var(--mi-shadow);align-items:flex-start;
      transition:border-color 140ms ease-out,background 140ms ease-out;
    }
    [data-testid="stRadio"] label:hover{background:var(--mi-card-strong);}
    [data-testid="stRadio"] label p{font-weight:600;font-size:0.95rem;}
    [data-testid="stRadio"] label:has(input:checked){
      border-color:var(--mi-mauve);background:rgba(255,255,255,0.9);
    }

    [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]{
      background:var(--mi-mauve) !important;box-shadow:0 2px 8px rgba(180,167,195,0.5);
    }
    [data-testid="stSlider"] [data-baseweb="slider"]>div>div{background:var(--mi-mauve) !important;}
    [data-testid="stSlider"] [data-testid="stTickBarMin"],
    [data-testid="stSlider"] [data-testid="stTickBarMax"]{color:var(--mi-muted);font-weight:600;}

    .stTextArea textarea,.stTextInput input{
      background:var(--mi-card-strong);
      border:1px solid rgba(23,32,51,0.10);
      border-radius:14px;color:var(--mi-navy);padding:12px 14px;
    }
    .stTextArea textarea:focus,.stTextInput input:focus{
      border-color:var(--mi-mauve);box-shadow:0 0 0 3px rgba(180,167,195,0.25);
    }

    .mi-complete{text-align:center;padding:26px 0;}
    .mi-check{
      width:92px;height:92px;border-radius:50%;margin:0 auto 20px;
      background:linear-gradient(135deg,#A9B6E8 0%,#E8BCC8 100%);
      display:flex;align-items:center;justify-content:center;
      color:#fff;font-size:44px;font-weight:700;
      box-shadow:0 10px 30px rgba(180,167,195,0.45);
    }
    </style>
    """, unsafe_allow_html=True)
    