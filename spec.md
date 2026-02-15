# API Specification

## Backend APIs

Base URL: `http://localhost:8000`

---

### GET /

Root endpoint.

**Response**

```json
{
  "service": "Essay Auto-Grading API"
}
```

---

### GET /api/health

Health check endpoint.

**Response**

```json
{
  "status": "ok",
  "gemini_configured": true,
  "model": "gemini-2.0-flash"
}
```

| Field               | Type    | Description                                           |
| ------------------- | ------- | ----------------------------------------------------- |
| `status`            | string  | Service status (`"ok"`)                               |
| `gemini_configured` | boolean | Whether GEMINI_API_KEY is set                         |
| `model`             | string  | Gemini model being used (default: `gemini-2.0-flash`) |

---

### POST /api/grade

Grade a single assignment.

**Content-Type:** `multipart/form-data`

**Request**

| Parameter           | Type   | Required | Description                                                 |
| ------------------- | ------ | -------- | ----------------------------------------------------------- |
| `assignments`       | file[] | Yes      | assignment file to grade (TXT, PDF, PNG)              |
| `rubric`            | file   | Yes      | Rubric file (PDF, Images, TXT)                                |
| `feedback_approach` | string | No       | A sentence/paragraph describing how feedback should be made |

**Allowed Assignment File Extensions:** `.pdf`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.txt`

**Response (Success)**

```json
{
  "name": "John Doe",
  "overall_feedback": "Great job on the assignment! Your thesis was clear and your evidence was strong. Keep up the good work!",
  "criteria_feedback": [
    {
      "criteria_title": "Thesis Statement",
      "score": 7.5,
      "score_max": 8,
      "feedback": "Your thesis statement is clear and well-defined. It sets a strong foundation for your assignment."
    }
  ]
}
```

| Field               | Type   | Description                                 |
| ------------------- | ------ | ------------------------------------------- |
| `name`              | string | Student's name (if detected)                |
| `overall_feedback`  | string | General feedback on the essay               |
| `criteria_feedback` | array  | Array of feedback for each grading criteria |

| Criteria Feedback Field | Type   | Description                                |
| ----------------------- | ------ | ------------------------------------------ |
| `criteria_title`        | string | Title of the grading criteria              |
| `score`                 | number | Score awarded for this criteria            |
| `score_max`             | number | Maximum possible score for this criteria   |
| `feedback`              | string | Specific feedback related to this criteria |

**Response (Error)**

```json
{
  "error": "Unsupported file type: .exe"
}
```

or

```json
{
  "error": "Grading failed",
  "detail": "Error message here"
}
```

---

### POST /api/grade/batch

Grade multiple essays in a single request.

**Content-Type:** `multipart/form-data`

**Request**

| Parameter           | Type   | Required | Description                                     |
| ------------------- | ------ | -------- | ----------------------------------------------- |
| `assignments`       | file[] | Yes      | assignment files to grade (TXT, PDF, PNG) |
| `rubric`            | file   | Yes      | Rubric file (PDF, Image, TXT)                    |
| `feedback_approach` | string | No       | Feedback approach (e.g., "detailed", "brief")   |

**Allowed Assignment File Extensions:** `.pdf`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.txt`

**Response**

```json
{
  "results": [
    {
      "name": "John Doe",
      "overall_feedback": "Great job on the assignment!",
      "criteria_feedback": [
        {
          "criteria_title": "Thesis Statement",
          "score": 7.5,
          "score_max": 8,
          "feedback": "Your thesis statement is clear and well-defined."
        }
      ]
    }
  ],
  "total": 1
}
```

| Field     | Type   | Description                   |
| --------- | ------ | ----------------------------- |
| `results` | array  | Array of grading results      |
| `total`   | number | Total number of essays graded |

**Result Item**

```json
{
  "name": "John Doe",
  "overall_feedback": "Great job on the assignment! Your thesis was clear and your evidence was strong. Keep up the good work!",
  "criteria_feedback": [
    {
      "criteria_title": "Thesis Statement",
      "score": 7.5,
      "score_max": 8,
      "feedback": "Your thesis statement is clear and well-defined. It sets a strong foundation for your assignment."
    }
  ]
}
```

or (on error)

```json
{
  "name": "essay1.pdf",
  "error": "Unsupported file type: .exe"
}
```

---

## Error Responses

All endpoints may return errors in the following format:

```json
{
  "error": "Error message"
}
```
