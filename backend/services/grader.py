import os
import time
from typing import Any

from utils import parse_json_response, extract_text, validate_file, get_file_extension

GEMINI_NATIVE_FORMATS = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

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


def _extract_text_from_docx(file_path: str) -> str:
    from docx import Document

    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def _read_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _prepare_for_gemini(input_value, client):
    import json

    uploaded_files = []

    if isinstance(input_value, dict):
        return [json.dumps(input_value, indent=2)], uploaded_files

    if not isinstance(input_value, str):
        return [str(input_value)], uploaded_files

    if os.path.isfile(input_value):
        validate_file(input_value)
        ext = get_file_extension(input_value)

        if ext == ".docx":
            text = _extract_text_from_docx(input_value)
            return [text], uploaded_files

        if ext == ".txt":
            text = _read_text_file(input_value)
            return [text], uploaded_files

        if ext in GEMINI_NATIVE_FORMATS:
            uploaded_file = client.files.upload(file=input_value)
            uploaded_files.append(uploaded_file)
            return [uploaded_file], uploaded_files

        try:
            text = _read_text_file(input_value)
            return [text], uploaded_files
        except Exception:
            raise ValueError(f"Unsupported file format: {ext}")

    return [input_value], uploaded_files


def grade_with_gemini(
    essay_input,
    rubric_input,
    api_key: str,
    max_retries: int = 2,
    feedback_approach: str | None = None,
) -> dict:
    from google import genai

    if not essay_input:
        raise ValueError("Essay input is empty.")

    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    client = genai.Client(api_key=api_key)

    essay_parts, essay_uploads = _prepare_for_gemini(essay_input, client)
    rubric_parts, rubric_uploads = _prepare_for_gemini(rubric_input, client)
    all_uploads = essay_uploads + rubric_uploads

    if feedback_approach == "brief":
        feedback_style = "\nFeedback style: BRIEF\n- feedback_short: 1-2 sentences only.\n- feedback_detailed.overall: 1-2 sentences max.\n- criteria_feedback: 1 sentence per criterion.\n- grammar_issues: top 3 only.\n- suggestions: 1-2 only.\n- Keep everything concise and to the point.\n"
    else:
        feedback_style = "\nFeedback style: DETAILED\n- feedback_detailed.overall: 2-4 sentences.\n- criteria_feedback: thorough explanation per criterion.\n- grammar_issues: list ALL found.\n- suggestions: 2-4 actionable suggestions.\n- Be as thorough and helpful as possible.\n"

    system_instruction = (
        "You are an expert educational grading assistant.\n"
        "You grade student essays/submissions based on a provided rubric and give feedback.\n\n"
        "You MUST respond with a JSON object with this EXACT schema:\n"
        '{"score_total": <number>,\n'
        ' "score_breakdown": [{"criterion_id": "<id>", "points": <number>, "max_points": <number>, "rationale": "<why this score>"}],\n'
        ' "rubric_checks": [{"criterion_id": "<id>", "met": <boolean>, "evidence_quote": "<direct quote from submission>"}],\n'
        ' "evidence_quotes": ["<direct quote 1>", "<direct quote 2>"],\n'
        ' "feedback_short": "<1-2 sentence summary>",\n'
        ' "feedback_detailed": {\n'
        '   "overall": "<2-4 sentence overall assessment>",\n'
        '   "strengths": ["<specific strength 1>"],\n'
        '   "weaknesses": ["<specific weakness 1>"],\n'
        '   "criteria_feedback": [{"criterion_id": "<id>", "status": "<met|partial|not_met>", "feedback": "<feedback>", "how_to_improve": "<advice or null>"}],\n'
        '   "grammar_issues": [{"location": "<where>", "original": "<text>", "correction": "<fix>", "rule": "<rule>"}],\n'
        '   "suggestions": ["<suggestion 1>"]\n'
        " },\n"
        ' "flags": [{"code": "<FLAG_CODE>", "message": "<explanation>"}],\n'
        ' "confidence": <number between 0.0 and 1.0>\n'
        "}\n\n"
        "Rules:\n"
        "- Read the rubric carefully and grade each criterion.\n"
        "- Quote directly from the submission as evidence.\n"
        "- This is a DRAFT grade. A professor will review it.\n"
        "- Add flags like LOW_EVIDENCE, AMBIGUOUS_RUBRIC_MATCH if applicable.\n"
        "- Return ONLY valid JSON." + feedback_style
    )

    contents = [
        "=== RUBRIC (grading criteria) ===",
        *rubric_parts,
        "\n=== STUDENT SUBMISSION (grade this) ===",
        *essay_parts,
        "\nGrade this submission according to the rubric. Provide detailed feedback for each criterion. Return JSON only.",
    ]

    last_error = None
    try:
        for attempt in range(max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.3,
                        "max_output_tokens": 4000,
                        "response_mime_type": "application/json",
                    },
                )

                content = response.text
                if content is None:
                    raise ValueError("No content received from Gemini")
                result = parse_json_response(content.strip())

                result.setdefault("score_total", 0)
                result.setdefault("score_breakdown", [])
                result.setdefault("rubric_checks", [])
                result.setdefault("evidence_quotes", [])
                result.setdefault("feedback_short", "")
                result.setdefault(
                    "feedback_detailed",
                    {
                        "overall": "",
                        "strengths": [],
                        "weaknesses": [],
                        "criteria_feedback": [],
                        "grammar_issues": [],
                        "suggestions": [],
                    },
                )
                result.setdefault("flags", [])
                result.setdefault("confidence", 0.85)

                return result

            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    print(f"[Gemini] Attempt {attempt + 1} failed: {e}")
                    time.sleep(1)
                    continue
                raise last_error

        if last_error:
            raise last_error
        raise RuntimeError("grade_with_gemini failed without error")

    finally:
        for f in all_uploads:
            try:
                client.files.delete(name=f.name)
            except Exception:
                pass


def _convert_score_to_scale(score: float, grading_scale: dict) -> dict[str, Any]:
    scale_type = grading_scale.get("type", "numeric")
    raw_max = 10.0
    percentage = (score / raw_max) * 100 if raw_max > 0 else 0.0

    result: dict[str, Any] = {
        "score_raw": float(score),
        "percentage": round(percentage, 2),
    }

    if scale_type == "numeric":
        max_points = int(grading_scale.get("max_points", 10))
        converted_score = (score / raw_max) * max_points
        result["score_total"] = round(converted_score, 2)

    elif scale_type == "letter":
        grade_letter = "F"
        for letter, threshold in sorted(
            STANDARD_LETTER_GRADE_BOUNDARIES.items(), key=lambda x: x[1], reverse=True
        ):
            if percentage >= threshold:
                grade_letter = letter
                break
        result["score_total"] = float(score)
        result["grade_letter"] = grade_letter

    elif scale_type == "pass_fail":
        passing_threshold = float(grading_scale.get("passing_threshold", 70.0))
        result["score_total"] = float(score)
        result["pass_fail"] = "P" if percentage >= passing_threshold else "F"

    else:
        result["score_total"] = float(score)

    return result


def _validate_result(result: dict, rubric: dict) -> dict[str, Any]:
    fd = result.get("feedback_detailed", {})
    if not isinstance(fd, dict):
        fd = {}

    validated_feedback = {
        "overall": str(fd.get("overall", "")),
        "strengths": fd.get("strengths", []),
        "weaknesses": fd.get("weaknesses", []),
        "criteria_feedback": fd.get("criteria_feedback", []),
        "grammar_issues": fd.get("grammar_issues", []),
        "suggestions": fd.get("suggestions", []),
    }

    grading_scale = rubric.get("grading_scale", DEFAULT_GRADING_SCALE.copy())

    if isinstance(grading_scale, dict) and "type" not in grading_scale:
        old_type = rubric.get("grading_scale_type", "numeric")
        if old_type == "points":
            grading_scale = {
                "type": "numeric",
                "max_points": rubric.get("scale_total", 10),
            }
        elif old_type == "pass_fail":
            grading_scale = {
                "type": "pass_fail",
                "passing_threshold": rubric.get("pass_threshold", 70),
            }
        elif old_type == "letter_grade":
            grading_scale = {"type": "letter"}

    raw_score = float(result.get("score_total", 0))
    converted = _convert_score_to_scale(raw_score, grading_scale)

    return {
        "score_total": converted["score_total"],
        "score_raw": converted["score_raw"],
        "percentage": converted["percentage"],
        "grade_letter": converted.get("grade_letter"),
        "pass_fail": converted.get("pass_fail"),
        "score_breakdown": result.get("score_breakdown", []),
        "rubric_checks": result.get("rubric_checks", []),
        "evidence_quotes": result.get("evidence_quotes", []),
        "feedback_short": str(result.get("feedback_short", "")),
        "feedback_detailed": validated_feedback,
        "flags": result.get("flags", []),
        "confidence": float(result.get("confidence", 0)),
        "grading_time_seconds": float(result.get("grading_time_seconds", 0)),
        "grading_scale": grading_scale,
    }


def _get_mock_grading_result(essay_input, rubric) -> dict:
    """Return a mock grading result when API is unavailable."""
    rubric_dict = (
        DEFAULT_ESSAY_RUBRIC
        if isinstance(rubric, str)
        else (rubric or DEFAULT_ESSAY_RUBRIC)
    )
    criteria = rubric_dict.get("criteria", [])

    score_breakdown = []
    criteria_feedback = []

    for criterion in criteria:
        cid = criterion.get("id", "")
        max_pts = criterion.get("max_points", 1)
        score = max(0, max_pts - 1)
        score_breakdown.append(
            {
                "criterion_id": cid,
                "points": score,
                "max_points": max_pts,
                "rationale": f"Mock grade for {criterion.get('name', cid)}",
            }
        )
        criteria_feedback.append(
            {
                "criterion_id": cid,
                "status": "partial" if score < max_pts else "met",
                "feedback": f"Mock feedback for {criterion.get('name', cid)}",
                "how_to_improve": "This is a mock response due to API rate limit.",
            }
        )

    total_score = sum(item["points"] for item in score_breakdown)
    max_total = sum(item["max_points"] for item in score_breakdown)

    return {
        "score_total": total_score,
        "score_breakdown": score_breakdown,
        "rubric_checks": [],
        "evidence_quotes": [],
        "feedback_short": "This is a mock grade due to API rate limit.",
        "feedback_detailed": {
            "overall": "Mock grade - API rate limit exceeded. Please try again later.",
            "strengths": ["Unable to assess due to rate limit"],
            "weaknesses": ["Unable to assess due to rate limit"],
            "criteria_feedback": criteria_feedback,
            "grammar_issues": [],
            "suggestions": ["Wait for rate limit to reset"],
        },
        "flags": [
            {"code": "MOCK_GRADE", "message": "Mock grade due to API rate limit"}
        ],
        "confidence": 0.0,
    }


def grade_essay(
    essay_input: str,
    rubric: dict | str | None = None,
    feedback_approach: str | None = None,
    check_ai: bool = True,
) -> dict[str, Any]:
    """
    Grade an essay using Google Gemini API with detailed feedback.

    Args:
        essay_input: Essay text string OR file path (PDF/image/DOCX/TXT)
        rubric: Rubric as dict, text string, file path, or None (uses default)
        feedback_approach: "brief" or "detailed" (default: "detailed")
        check_ai: Whether to perform AI-generated content detection (default: True)

    Returns:
        Grading result dictionary with detailed feedback
    """
    api_key = (
        os.getenv("GEMINI_API_KEY", "").strip()
        or os.getenv("GOOGLE_API_KEY", "").strip()
    )
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. Set it in .env or environment variables."
        )

    rubric_to_pass = rubric if rubric is not None else DEFAULT_ESSAY_RUBRIC

    start = time.time()
    try:
        result = grade_with_gemini(
            essay_input, rubric_to_pass, api_key, feedback_approach=feedback_approach
        )
    except Exception as e:
        if (
            "429" in str(e)
            or "RESOURCE_EXHAUSTED" in str(e)
            or "rate limit" in str(e).lower()
        ):
            result = _get_mock_grading_result(essay_input, rubric_to_pass)
        else:
            raise
    elapsed = round(time.time() - start, 2)

    result["grading_time_seconds"] = elapsed

    rubric_dict = (
        DEFAULT_ESSAY_RUBRIC if isinstance(rubric_to_pass, str) else rubric_to_pass
    )

    if check_ai:
        from services.detector import analyze_essay_authenticity

        if os.path.isfile(essay_input):
            with open(essay_input, "rb") as f:
                essay_bytes = f.read()
            essay_text = extract_text(essay_bytes, essay_input)
        else:
            essay_text = essay_input

        authenticity = analyze_essay_authenticity(essay_text)
        result["authenticity"] = authenticity
        result["flags"].extend(authenticity["flags"])
        result["is_authentic"] = authenticity["authentic"]

    return _validate_result(result, rubric_dict)
