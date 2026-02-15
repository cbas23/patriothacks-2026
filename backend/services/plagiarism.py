import os

from utils import parse_json_response


def check_plagiarism(texts: list[str], filenames: list[str] | None = None) -> dict:
    """
    Use Gemini to compare essays and return the highest pairwise similarity as a percentage.

    Args:
        texts: List of essay text strings.
        filenames: Optional (unused in Gemini version).

    Returns:
        {"overall_max_percent": 35.2}
    """
    n = len(texts)
    if n < 2:
        return {"overall_max_percent": 0.0}

    valid = [t.strip() for t in texts if t and len(t.strip()) > 50]
    if len(valid) < 2:
        return {"overall_max_percent": 0.0}

    api_key = (
        os.getenv("GEMINI_API_KEY", "").strip()
        or os.getenv("GOOGLE_API_KEY", "").strip()
    )
    if not api_key:
        return {"overall_max_percent": 0.0}

    max_chars_per_essay = 4000
    truncated = [t[:max_chars_per_essay] for t in valid]

    parts = []
    for i, t in enumerate(truncated, 1):
        parts.append(f"=== Essay {i} ===\n{t}\n")
    parts.append(
        "Compare the above essays for plagiarism/similarity (content overlap, phrasing, structure). "
        "Return a single JSON object with one number: the highest similarity percentage (0-100) between ANY two essays. "
        'Example: {"overall_max_percent": 35}. Return ONLY valid JSON, nothing else.'
    )
    prompt = "\n".join(parts)

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 100,
                "response_mime_type": "application/json",
            },
        )
        content = response.text
        if content is None:
            return {"overall_max_percent": 0.0}
        data = parse_json_response(content.strip())
        pct = float(data.get("overall_max_percent", 0))
        pct = max(0.0, min(100.0, pct))
        return {"overall_max_percent": round(pct, 2)}
    except Exception:
        return {"overall_max_percent": 0.0}
