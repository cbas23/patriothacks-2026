import os

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".docx", ".txt"}

GEMINI_NATIVE_FORMATS = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

DEFAULT_GRADING_SCALE = {"type": "numeric", "max_points": 10}

STANDARD_LETTER_GRADE_BOUNDARIES = {
    "A": 93.0,
    "A-": 90.0,
    "B+": 87.0,
    "B": 83.0,
    "B-": 80.0,
    "C+": 77.0,
    "C": 73.0,
    "C-": 70.0,
    "D+": 67.0,
    "D": 63.0,
    "D-": 60.0,
    "F": 0.0,
}

DEFAULT_ESSAY_RUBRIC = {
    "type": "ESSAY",
    "grading_scale": {"type": "numeric", "max_points": 10},
    "criteria": [
        {
            "id": "thesis",
            "name": "Thesis/Claim",
            "max_points": 2,
            "description": "Clear, specific main claim.",
        },
        {
            "id": "evidence",
            "name": "Evidence/Support",
            "max_points": 3,
            "description": "Uses relevant evidence/examples and explains them.",
        },
        {
            "id": "organization",
            "name": "Organization",
            "max_points": 2,
            "description": "Logical flow; clear structure.",
        },
        {
            "id": "clarity",
            "name": "Clarity",
            "max_points": 2,
            "description": "Clear wording; minimal ambiguity.",
        },
        {
            "id": "grammar",
            "name": "Grammar/Mechanics",
            "max_points": 1,
            "description": "Few grammar/spelling errors.",
        },
    ],
    "must_quote_evidence": True,
    "max_evidence_quotes": 3,
}


def get_gemini_model() -> str:
    """Get the configured Gemini model."""
    return os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def get_api_key() -> str:
    """Get the Gemini API key from environment."""
    return (
        os.getenv("GEMINI_API_KEY", "").strip()
        or os.getenv("GOOGLE_API_KEY", "").strip()
    )
