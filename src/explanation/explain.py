import os

def _load_key():
    # Read GEMINI_API_KEY directly from .env (robust against parser quirks)
    try:
        with open(".env") as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception:
        pass
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
        return f"{name} fits Focus: energy {e:.2f} and higher acousticness keep it low-distraction while matching your taste."
    if mode == "Energy":
        return f"{name} fits Energy: high energy {e:.2f} and tempo {t:.0f} bpm lift intensity while staying in your taste."
    if mode == "Inspiration":
        acc = track.get("acclaim_score", 0) or 0
        return f"{name} fits Inspiration: a critically recognised track (acclaim {acc:.2f}) aligned with your taste."
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
        "You explain why a music recommendation was made. "
        "Use ONLY the signals provided. Do NOT invent facts about the song, artist, or lyrics. "
        "Write ONE short friendly sentence (max 25 words) on why this track fits the chosen mode "
        "and the listener's taste, referencing the relevant signals.\n\n"
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
