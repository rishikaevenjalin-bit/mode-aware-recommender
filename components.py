import html
import streamlit as st

MODE_META = {
    "focus":       {"icon": "\u25CE", "label": "Focus",       "desc": "Concentration and deep work"},
    "energy":      {"icon": "\u26A1", "label": "Energy",      "desc": "Workouts and motivation"},
    "inspiration": {"icon": "\u2726", "label": "Inspiration", "desc": "Discovery and acclaimed music"},
}

def _e(v):
    return html.escape(str(v))

def mode_badge(mode):
    m = MODE_META[mode.lower()]
    st.markdown(
        f'<div class="mi-center"><span class="badge {mode.lower()}">{m["icon"]} {m["label"].upper()}</span></div>',
        unsafe_allow_html=True)

def mode_grid(selected):
    cards = "".join(
        f'<div class="mode-card {k}{" selected" if k == selected.lower() else ""}">'
        f'<div class="mode-icon">{v["icon"]}</div>'
        f'<div class="mode-name">{v["label"]}</div>'
        f'<div class="mode-desc">{v["desc"]}</div></div>'
        for k, v in MODE_META.items())
    st.markdown(f'<div class="mode-grid">{cards}</div>', unsafe_allow_html=True)

def artist_chips(artists):
    if not artists:
        return
    chips = "".join(f'<span class="artist-chip"><span class="dot"></span>{_e(a)}</span>' for a in artists)
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

def song_card(rank, title, artist, mode, hook, explanation,
              signals=None, art_url=None, is_seed=False):
    if art_url:
        art = f'<img class="song-art" src="{_e(art_url)}" alt="Album art">'
    else:
        art = '<div class="song-art" aria-hidden="true">\u266A</div>'
    tags = f'<span class="badge {mode.lower()}">{MODE_META[mode.lower()]["label"]} fit</span>'
    if is_seed:
        tags += '<span class="badge seed">\u2726 From your picks</span>'
    sig = ""
    if signals:
        sig = '<div class="signal-row">' + "".join(
            f'<span class="signal"><span class="k">{_e(k)}</span><span class="v">{_e(v)}</span></span>'
            for k, v in signals.items()) + "</div>"
    seed_cls = " is-seed" if is_seed else ""
    st.markdown(f"""<div class="song-card mi-fade{seed_cls}">
  <div class="song-head">
    <div class="song-rank">{rank}</div>
    {art}
    <div class="song-meta">
      <div class="song-title">{_e(title)}</div>
      <div class="song-artist">{_e(artist)}</div>
      <div class="song-tags">{tags}</div>
    </div>
  </div>
  <div class="explanation-card">
    <div class="exp-label">WHY THIS TRACK</div>
    <div class="exp-hook">{_e(hook)}</div>
    <div class="exp-body">{_e(explanation)}</div>
    {sig}
  </div>
</div>""", unsafe_allow_html=True)

def completion(title="Thanks for listening.",
               body="Your anonymous feedback has been recorded.<br>It genuinely helps the study."):
    st.markdown(f"""<div class="mi-complete">
  <div class="mi-check" role="img" aria-label="Complete">\u2713</div>
  <h1>{_e(title)}</h1>
  <p class="mi-lede" style="margin:12px auto 0;">{body}</p>
</div>""", unsafe_allow_html=True)
