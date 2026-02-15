import base64
import io
import os
from typing import Literal

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont


def _get_text_dimensions(text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    left, top, right, bottom = font.getbbox(text)
    return int(right - left), int(bottom - top)


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        width, _ = _get_text_dimensions(test_line, font)
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def pdf_to_images(file_path: str) -> list[str]:
    images: list[str] = []
    doc = fitz.open(file_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_bytes = pix.tobytes("png")
        images.append(base64.b64encode(img_bytes).decode("utf-8"))

    doc.close()
    return images


def docx_to_image(file_path: str) -> str:
    from docx import Document

    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

    if not paragraphs:
        paragraphs = ["[Empty document]"]

    font_size = 24
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size
        )
    except Exception:
        font = ImageFont.load_default()

    line_height = font_size + 10
    padding = 40
    max_width = 1000

    wrapped_lines = []
    for para in paragraphs:
        wrapped = _wrap_text(para, font, max_width - padding * 2)
        wrapped_lines.extend(wrapped)
        wrapped_lines.append("")

    if not wrapped_lines:
        wrapped_lines = ["[No content]"]

    text_height = len(wrapped_lines) * line_height
    img_height = text_height + padding * 2
    img_width = max_width

    img = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(img)

    y = padding
    for line in wrapped_lines:
        draw.text((padding, y), line, fill="black", font=font)
        y += line_height

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def txt_to_image(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        text = "[Empty file]"

    font_size = 24
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size
        )
    except Exception:
        font = ImageFont.load_default()

    line_height = font_size + 10
    padding = 40
    max_width = 1000

    wrapped_lines = _wrap_text(text, font, max_width - padding * 2)
    text_height = len(wrapped_lines) * line_height
    img_height = text_height + padding * 2
    img_width = max_width

    img = Image.new("RGB", (img_width, img_height), color="white")
    draw = ImageDraw.Draw(img)

    y = padding
    for line in wrapped_lines:
        draw.text((padding, y), line, fill="black", font=font)
        y += line_height

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def image_to_png(file_path: str) -> str:
    img = Image.open(file_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def convert_to_image(
    file_path: str,
) -> dict[Literal["images"], list[str]]:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        images = pdf_to_images(file_path)
        return {"images": images}
    elif ext == ".docx":
        image = docx_to_image(file_path)
        return {"images": [image]}
    elif ext == ".txt":
        image = txt_to_image(file_path)
        return {"images": [image]}
    elif ext in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        image = image_to_png(file_path)
        return {"images": [image]}
    else:
        raise ValueError(f"Unsupported file type: {ext}")
