import os
import tempfile
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOWED_EXTENSIONS
from services.grader import grade_essay
from services.graderv2 import grade_work
from services.detector import detect_ai_text
from services.plagiarism import check_plagiarism
from utils.text_extractor import extract_text
from services.file_to_image import convert_to_image

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _save_temp(upload_file: UploadFile) -> str:
    suffix = os.path.splitext(upload_file.filename or "")[1]
    upload_file.file.seek(0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(upload_file.file.read())
        return tmp.name


def _format_response(grading_result: dict, ai_detection: dict | None = None) -> dict:
    criteria_feedback = []
    score_breakdown = grading_result.get("score_breakdown", [])
    detailed_criteria = grading_result.get("feedback_detailed", {}).get(
        "criteria_feedback", []
    )

    for item in score_breakdown:
        cid = item.get("criterion_id", "")
        detail = next(
            (cf for cf in detailed_criteria if cf.get("criterion_id") == cid), {}
        )
        criteria_feedback.append(
            {
                "criteria_title": cid,
                "score": item.get("points", 0),
                "score_max": item.get("max_points", 0),
                "feedback": detail.get("feedback", item.get("rationale", "")),
            }
        )

    response = {
        "name": grading_result.get("name", ""),
        "overall_feedback": grading_result.get("feedback_detailed", {}).get(
            "overall", ""
        ),
        "criteria_feedback": criteria_feedback,
    }

    if ai_detection:
        response["ai_detection"] = ai_detection

    return response


@app.get("/")
def read_root():
    return {"service": "Essay Auto-Grading API"}


@app.get("/api/health")
def health():
    has_key = bool(os.getenv("GEMINI_API_KEY", "").strip())
    return {
        "status": "ok",
        "gemini_configured": has_key,
        "model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    }


@app.post("/api/grade")
async def grade(
    assignments: list[UploadFile] = File(...),
    rubric: UploadFile = File(...),
    feedback_approach: Optional[str] = Form(None),
):
    if not assignments:
        return {"error": "No assignment file provided"}

    essay = assignments[0]
    essay_path = None
    rubric_path = None
    try:
        ext = os.path.splitext(essay.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return {"error": f"Unsupported file type: {ext}"}

        essay_path = _save_temp(essay)
        rubric_path = _save_temp(rubric)

        result = grade_essay(
            essay_path, rubric=rubric_path, feedback_approach=feedback_approach
        )

        essay.file.seek(0)
        essay_bytes = essay.file.read()
        essay_text = extract_text(essay_bytes, essay.filename or "")
        ai_detection = detect_ai_text(essay_text) if essay_text else None

        return _format_response(result, ai_detection=ai_detection)

    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Grading failed", "detail": str(e)}
    finally:
        if essay_path and os.path.isfile(essay_path):
            os.unlink(essay_path)
        if rubric_path and os.path.isfile(rubric_path):
            os.unlink(rubric_path)


@app.post("/api/grade/batch")
async def grade_batch(
    assignments: list[UploadFile] = File(...),
    rubric: UploadFile = File(...),
    feedback_approach: Optional[str] = Form(None),
):
    rubric_path = None
    try:
        rubric_path = _save_temp(rubric)

        results = []
        for essay in assignments:
            essay_path = None
            try:
                ext = os.path.splitext(essay.filename or "")[1].lower()
                if ext not in ALLOWED_EXTENSIONS:
                    results.append(
                        {
                            "name": essay.filename,
                            "error": f"Unsupported file type: {ext}",
                        }
                    )
                    continue

                essay_path = _save_temp(essay)
                result = grade_essay(
                    essay_path, rubric=rubric_path, feedback_approach=feedback_approach
                )

                essay.file.seek(0)
                essay_bytes = essay.file.read()
                essay_text = extract_text(essay_bytes, essay.filename or "")
                ai_detection = detect_ai_text(essay_text) if essay_text else None

                results.append(_format_response(result, ai_detection=ai_detection))

            except Exception as e:
                results.append({"name": essay.filename, "error": str(e)})
            finally:
                if essay_path and os.path.isfile(essay_path):
                    os.unlink(essay_path)

        return {"results": results, "total": len(results)}

    except Exception as e:
        return {"error": "Batch grading failed", "detail": str(e)}
    finally:
        if rubric_path and os.path.isfile(rubric_path):
            os.unlink(rubric_path)


@app.post("/api/gradev2")
async def gradev2(
    assignment: UploadFile = File(...),
    rubric: UploadFile = File(...),
    notes: str = "",
):
    try:
        rubric.file.seek(0)
        rubric_bytes = rubric.file.read()

        assignment.file.seek(0)
        assignment_bytes = assignment.file.read()

        result = grade_work(
            rubric=rubric_bytes,
            rubric_filename=rubric.filename or "rubric.pdf",
            notes=notes,
            assignment=assignment_bytes,
            assignment_filename=assignment.filename or "assignment.pdf",
        )

        return result

    except Exception as e:
        return {"error": "Grading failed", "detail": str(e)}


@app.post("/api/plagiarism/check")
async def plagiarism_check(assignments: list[UploadFile] = File(...)):
    if len(assignments) < 2:
        return {
            "error": "At least 2 assignment files are required for plagiarism check."
        }

    texts = []
    filenames = []
    for f in assignments:
        ext = os.path.splitext(f.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            texts.append("")
            filenames.append(f.filename or "")
            continue
        f.file.seek(0)
        data = f.file.read()
        text = extract_text(data, f.filename or "")
        texts.append(text)
        filenames.append(f.filename or "")

    result = check_plagiarism(texts, filenames)
    return result


@app.post("/api/convert/to-image")
async def convert_file_to_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    allowed = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".docx", ".txt"}
    if ext not in allowed:
        return {"error": f"Unsupported file type: {ext}"}

    file_path = None
    try:
        file_path = _save_temp(file)
        result = convert_to_image(file_path)
        return result
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Conversion failed", "detail": str(e)}
    finally:
        if file_path and os.path.isfile(file_path):
            os.unlink(file_path)
