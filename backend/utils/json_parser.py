import json
import re


def parse_json_response(content: str) -> dict:
    """
    Extract JSON from Gemini response (handles markdown/code blocks).

    Args:
        content: The raw response content from Gemini

    Returns:
        Parsed JSON dictionary

    Raises:
        ValueError: If no valid JSON can be extracted
    """
    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    if "```" in content:
        lines = content.split("\n")
        json_lines = []
        inside = False
        for line in lines:
            if line.startswith("```"):
                if not inside:
                    inside = True
                else:
                    break
                continue
            if inside:
                json_lines.append(line)
        if json_lines:
            try:
                return json.loads("\n".join(json_lines))
            except json.JSONDecodeError:
                pass

    m = re.search(r"\{[\s\S]*\}", content)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract valid JSON from response: {content[:200]}")
