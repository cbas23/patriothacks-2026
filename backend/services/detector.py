import os
from typing import Optional

import requests


def detect_ai_with_sapling(text: str, api_key: Optional[str] = None) -> dict:
    """
    Detect whether the given text was written by AI or a human
    using the Sapling.ai AI Detector API.

    Args:
        text: The essay text to analyze
        api_key: Uses SAPLING_API_KEY environment variable

    Returns:
        Dictionary with detection results or error dict
    """
    if api_key is None:
        api_key = os.getenv("SAPLING_API_KEY", "").strip()

    if not api_key:
        return {
            "error": "SAPLING_API_KEY is not set",
            "is_ai_generated": False,
            "ai_probability": 0.0,
            "overall_score": 0.0,
            "sentence_scores": [],
            "confidence": "unknown",
            "threshold_used": 0.5,
        }

    if not text or len(text.strip()) < 10:
        return {
            "error": "Text too short for reliable detection",
            "is_ai_generated": False,
            "ai_probability": 0.0,
            "overall_score": 0.0,
            "sentence_scores": [],
            "confidence": "unknown",
            "threshold_used": 0.5,
        }

    try:
        truncated_text = text[:200000]

        response = requests.post(
            "https://api.sapling.ai/api/v1/aidetect",
            json={"key": api_key, "text": truncated_text},
            timeout=30,
        )

        if response.status_code != 200:
            return {
                "error": f"Sapling API error: HTTP {response.status_code}",
                "is_ai_generated": False,
                "ai_probability": 0.0,
                "overall_score": 0.0,
                "sentence_scores": [],
                "confidence": "unknown",
                "threshold_used": 0.5,
            }

        data = response.json()
        ai_score = float(data.get("score", 0.0))

        sentence_scores = [
            float(s.get("score", 0.0)) for s in data.get("sentence_scores", [])
        ]

        if ai_score > 0.8 or ai_score < 0.2:
            confidence = "high"
        elif ai_score > 0.6 or ai_score < 0.4:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "is_ai_generated": ai_score > 0.5,
            "ai_probability": round(ai_score, 4),
            "overall_score": round(ai_score, 4),
            "sentence_scores": sentence_scores,
            "confidence": confidence,
            "threshold_used": 0.5,
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Sapling API request timed out",
            "is_ai_generated": False,
            "ai_probability": 0.0,
            "overall_score": 0.0,
            "sentence_scores": [],
            "confidence": "unknown",
            "threshold_used": 0.5,
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}",
            "is_ai_generated": False,
            "ai_probability": 0.0,
            "overall_score": 0.0,
            "sentence_scores": [],
            "confidence": "unknown",
            "threshold_used": 0.5,
        }
    except Exception as e:
        return {
            "error": f"Detection failed: {str(e)}",
            "is_ai_generated": False,
            "ai_probability": 0.0,
            "overall_score": 0.0,
            "sentence_scores": [],
            "confidence": "unknown",
            "threshold_used": 0.5,
        }


def analyze_essay_authenticity(essay_text: str, api_key: Optional[str] = None) -> dict:
    """
    Analyze the authenticity of an essay by detecting AI-generated content.

    Args:
        essay_text: The essay text to analyze
        api_key: Optional API key for Sapling AI Detector

    Returns:
        Dictionary with authenticity analysis
    """
    ai_detection = detect_ai_with_sapling(essay_text, api_key)

    flags = []
    authentic = True

    if "error" in ai_detection:
        flags.append(
            {
                "code": "AI_DETECTION_ERROR",
                "message": f"AI detection failed: {ai_detection['error']}",
                "severity": "low",
            }
        )
        authentic = True
    else:
        if ai_detection["is_ai_generated"]:
            authentic = False

            if ai_detection["confidence"] == "high":
                flags.append(
                    {
                        "code": "AI_GENERATED_HIGH",
                        "message": f"High confidence (AI probability: {ai_detection['ai_probability']}) that this essay was AI-generated",
                        "severity": "high",
                    }
                )
            elif ai_detection["confidence"] == "medium":
                flags.append(
                    {
                        "code": "AI_GENERATED_MEDIUM",
                        "message": f"Medium confidence (AI probability: {ai_detection['ai_probability']}) that this essay may be AI-generated",
                        "severity": "medium",
                    }
                )
            else:
                flags.append(
                    {
                        "code": "AI_SUSPECTED",
                        "message": f"Low confidence (AI probability: {ai_detection['ai_probability']}) that this essay may be AI-generated",
                        "severity": "low",
                    }
                )
        else:
            authentic = True

    return {"authentic": authentic, "flags": flags, "ai_detection": ai_detection}


def detect_ai_text(text: str) -> dict:
    """Detect whether the given text was written by AI or a human."""
    return detect_ai_with_sapling(text)
