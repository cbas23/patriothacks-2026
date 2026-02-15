import asyncio
import logging
import os
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from services.file_to_image import convert_to_image
from services.graderv2 import grade_work

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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


@app.post("/api/gradev2")
async def gradev2(
    assignment: UploadFile = File(...),
    rubric: UploadFile = File(...),
    notes: str = "",
):
    logger.info(
        f"Received gradev2 request - assignment: {assignment.filename}, rubric: {rubric.filename}"
    )
    rubric_path = None
    assignment_path = None
    try:
        logger.info("Reading rubric file")
        rubric.file.seek(0)
        rubric_bytes = rubric.file.read()

        logger.info("Reading assignment file")
        assignment.file.seek(0)
        assignment_bytes = assignment.file.read()

        assignment_ext = os.path.splitext(assignment.filename or "")[1].lower()
        allowed_ext = {
            ".pdf",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".webp",
            ".txt",
        }

        assignment_path = None
        if assignment_ext in allowed_ext:
            assignment_path = _save_temp(assignment)
            image_task = asyncio.to_thread(convert_to_image, assignment_path)
        else:

            async def no_image():
                return {}

            image_task = no_image()

        grading_task = asyncio.to_thread(
            grade_work,
            rubric=rubric_bytes,
            rubric_filename=rubric.filename or "rubric.pdf",
            notes=notes,
            assignment=assignment_bytes,
            assignment_filename=assignment.filename or "assignment.pdf",
        )

        result, image_result = await asyncio.gather(grading_task, image_task)

        if "error" in result:
            logger.error(f"Grade work returned error: {result}")
            return result

        if assignment_ext in allowed_ext:
            result["images"] = image_result.get("images", []) if image_result else []
            logger.info("Image conversion completed")

        logger.info("gradev2 request completed successfully")
        return result

    except Exception as e:
        logger.error(f"gradev2 request failed: {str(e)}")
        return {"error": "Grading failed", "detail": str(e)}
    finally:
        if rubric_path and os.path.isfile(rubric_path):
            os.unlink(rubric_path)
        if assignment_path and os.path.isfile(assignment_path):
            os.unlink(assignment_path)
