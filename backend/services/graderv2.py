import io
import os

from google import genai
from google.genai import types

from utils import parse_json_response

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".txt"}

MIME_TYPE_MAP = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".txt": "text/plain",
}


def grade_work(
    rubric: bytes,
    rubric_filename: str,
    notes: str,
    assignment: bytes,
    assignment_filename: str,
) -> dict:
    rubric_ext = os.path.splitext(rubric_filename)[1].lower()
    assignment_ext = os.path.splitext(assignment_filename)[1].lower()

    if rubric_ext not in ALLOWED_EXTENSIONS:
        return {"error": f"Unsupported file type: {rubric_ext}"}

    if assignment_ext not in ALLOWED_EXTENSIONS:
        return {"error": f"Unsupported file type: {assignment_ext}"}

    api_key = (
        os.getenv("GEMINI_API_KEY", "").strip()
        or os.getenv("GOOGLE_API_KEY", "").strip()
    )
    if not api_key:
        return {"error": "Grading failed", "detail": "GEMINI_API_KEY not configured"}

    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    rubric_mime = MIME_TYPE_MAP.get(rubric_ext, "application/octet-stream")
    assignment_mime = MIME_TYPE_MAP.get(assignment_ext, "application/octet-stream")

    rubric_file = client.files.upload(
        file=io.BytesIO(rubric),
        config={"display_name": "rubric", "mime_type": rubric_mime},
    )

    assignment_file = client.files.upload(
        file=io.BytesIO(assignment),
        config={"display_name": "assignment", "mime_type": assignment_mime},
    )

    try:
        response_schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "name": types.Schema(type=types.Type.STRING),
                "overall_feedback": types.Schema(type=types.Type.STRING),
                "criteria_feedback": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "criteria_title": types.Schema(type=types.Type.STRING),
                            "score": types.Schema(type=types.Type.NUMBER),
                            "score_max": types.Schema(type=types.Type.NUMBER),
                            "feedback": types.Schema(type=types.Type.STRING),
                        },
                        required=["criteria_title", "score", "score_max", "feedback"],
                    ),
                ),
            },
            required=["overall_feedback", "criteria_feedback"],
        )

        system_instruction = (
            "You are an expert educational grading assistant.\n"
            f"Instructor notes: {notes}\n\n"
            "Grade the student assignment based on the attached rubric.\n"
            "Provide detailed feedback for each criterion.\n"
            "Calculate the score for each criterion and an overall score if applicable.\n"
            "When possible, make sure the name field is filled with the student's name\n"
            "Respond with valid JSON only."
        )

        response = client.models.generate_content(
            model=model,
            contents=[
                "=== RUBRIC ===",
                rubric_file,
                "\n=== STUDENT ASSIGNMENT ===",
                f"\n file: {assignment_filename}\n",
                assignment_file,
                "\nGrade this assignment according to the rubric. Following the instructor notes",
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.3,
                max_output_tokens=4000,
            ),
        )

        if response.text is None:
            return {"error": "Grading failed", "detail": "No content received from AI"}

        result = parse_json_response(response.text.strip())

        return {
            "name": result.get("name", ""),
            "overall_feedback": result.get("overall_feedback", ""),
            "criteria_feedback": result.get("criteria_feedback", []),
        }

    except Exception as e:
        return {"error": "Grading failed", "detail": str(e)}

    finally:
        if rubric_file.name:
            try:
                client.files.delete(name=rubric_file.name)
            except Exception:
                pass
        if assignment_file.name:
            try:
                client.files.delete(name=assignment_file.name)
            except Exception:
                pass
