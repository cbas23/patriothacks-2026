from .grader import grade_essay
from .detector import detect_ai_text, analyze_essay_authenticity
from .plagiarism import check_plagiarism

__all__ = [
    "grade_essay",
    "detect_ai_text",
    "analyze_essay_authenticity",
    "check_plagiarism",
]
