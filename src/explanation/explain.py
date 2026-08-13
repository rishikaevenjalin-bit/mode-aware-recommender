import os

def _load_key():
    # 1. Streamlit secrets (deployed app)
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    # 2. .env file (local development)
    try:
        with open(".env") as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception:
        pass
    # 3. environment variable
    return os.getenv("GEMINI_API_KEY")

_API_KEY = _load_key()
_client = None

def _get_client():
    global _client
    if _client is None and _API_KEY:
        try:
            from google import genai
            _client = genai.Client(api_key=_API_KEY)
        except Exception:
            _client = None
    return _client


def _template_explanation(track, mode):
    name = track.get("name", "This track")
    e = track.get("energy", 0)
    t = track.get("tempo", 0)
    if mode == "Focus":
        return f"{name} is a calm, gentle pick, easy to concentrate to and right in line with your taste."
    if mode == "Energy":
        return f"{name} brings the energy up with a driving, upbeat feel to keep you moving, and it matches your taste."
    if mode == "Inspiration":
        acc = track.get("acclaim_score", 0) or 0
        return f"{name} is a critically loved gem worth discovering, aligned beautifully with the artists you enjoy."
    return f"{name} matches your taste profile."


def explain(track, mode):
    client = _get_client()
    if client is None:
        return _template_explanation(track, mode)
    signals = (
        f"Mode: {mode}. Track: {track.get('name')} by {track.get('artist')}. "
        f"energy={track.get('energy'):.2f}, tempo={track.get('tempo'):.0f}, "
        f"valence={track.get('valence'):.2f}, acousticness={track.get('acousticness'):.2f}, "
        f"instrumentalness={track.get('instrumentalness'):.2f}, "
        f"acclaim_score={track.get('acclaim_score', 0) or 0:.2f}, "
        f"taste_match={track.get('hybrid_score', 0):.2f}"
    )
    prompt = (
        "You are a warm, music-loving friend explaining why a song was recommended. "
        "Use ONLY the signals provided - never invent facts about the song, artist, lyrics, or meaning. "
        "Write ONE natural, inviting sentence (max 25 words). Vary your phrasing - avoid starting every "
        "explanation the same way, and avoid listing raw numbers like 'energy 0.54'. Instead describe the "
        "feel (calm, upbeat, uplifting, mellow) and connect it to the listener's mode and taste. "
        "Sound human and appealing, not technical.\n\n"
        f"Signals: {signals}"
    )
    try:
        resp = client.models.generate_content(
            model="gemini-flash-latest", contents=prompt
        )
        text = (resp.text or "").strip()
        return text if text else _template_explanation(track, mode)
    except Exception:
        return _template_explanation(track, mode)


if __name__ == "__main__":
    from src.recommender import generate_candidates_from_artists
    from src.ranking.focus import rank_focus
    cands = generate_candidates_from_artists(["Radiohead", "Coldplay"])
    ranked = rank_focus(cands)
    print("Testing explanations (Focus mode):\n")
    for _, row in ranked.head(3).iterrows():
        print("-", explain(row.to_dict(), "Focus"))
