import os

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def get_file_extension(file_path: str) -> str:
    """Get the lowercase file extension from a file path."""
    return os.path.splitext(file_path)[1].lower()


def validate_file(file_path: str) -> None:
    """
    Validate that a file exists, is not empty, and is within size limits.

    Raises:
        ValueError: If file is invalid
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    size = os.path.getsize(file_path)
    if size == 0:
        raise ValueError(f"File is empty: {file_path}")

    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"File exceeds 10MB limit: {file_path} ({size / 1024 / 1024:.1f}MB)"
        )
