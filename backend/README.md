# Essay Auto-Grading AI Backend

A FastAPI-based essay grading system that uses Google Gemini API to automatically grade essays with detailed feedback. The system supports multiple grading scales: Points-based, Pass/Fail, and Letter Grade.

## Features

- **Multiple Grading Scales**: Choose between Points, Pass/Fail, or Letter Grade
- **Detailed Feedback**: Get overall assessment, strengths, weaknesses, and per-criterion feedback
- **Multiple Input Formats**: Accept essays as text strings, PDF files, images, Word documents, or plain text
- **Customizable Rubrics**: Define your own grading criteria and scale
- **AI-Powered**: Uses Google Gemini API for intelligent grading
- **Draft Mode**: All grades are drafts that require professor finalization

## Installation

```bash
cd backend
uv sync
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
# or
GOOGLE_API_KEY=your_gemini_api_key_here
```

Optional:
```env
GEMINI_MODEL=gemini-2.0-flash  # Default model
SAPLING_API_KEY=your_sapling_api_key_here  # For AI-generated content detection
```

## Usage

### Basic Usage

```python
from essay_grader import grade_essay, DEFAULT_ESSAY_RUBRIC

# Grade an essay file
result = grade_essay("essay.pdf")

# Access the results
print(f"Final Grade: {result['final_grade']}")
print(f"Percentage: {result['score_percentage']}%")
print(f"Overall Feedback: {result['feedback_detailed']['overall']}")
```

### Interactive Grading

The system includes an interactive mode that prompts professors to choose their preferred grading scale before grading.

```python
from essay_grader import interactive_grade_essay

# This will prompt the professor to select a grading scale type
# and collect any necessary configuration details
result = interactive_grade_essay("essay.pdf")

# Results are automatically formatted based on the chosen scale
print(f"Final Grade: {result['final_grade']}")
```

**What happens during interactive grading:**

1. **Choose Grading Scale Type:**
   ```
   ============================================================
   Please choose a grading scale type:
   ============================================================
   1. Points-based (e.g., out of 10, out of 50, out of 100)
   2. Pass/Fail (e.g., Pass if 70% or higher)
   3. Letter Grade (e.g., A, B, C, D, F)
   ============================================================
   Enter your choice (1/2/3): 
   ```

2. **Configure the Selected Scale:**
   - **Points-based**: Enter total points (e.g., 50, 100)
   - **Pass/Fail**: Enter pass threshold percentage (default: 70%)
   - **Letter Grade**: Choose standard A/B/C/D/F or define custom boundaries

3. **Grade the Essay**: The system grades using your selected configuration

4. **View Results**: Final grade is displayed in the chosen format

**For frontend integration**, you can capture the user's grading scale preference and pass it as a rubric parameter to `grade_essay()`.

Run the interactive example to see it in action:
```bash
cd backend
python interactive_example.py
```

## Grading Scales

The system supports three types of grading scales:

### 1. Points-Based (Default)

Grades are displayed as "X/Y" (e.g., "8.5/10", "42/50", "85/100").

```python
from essay_grader import DEFAULT_ESSAY_RUBRIC

# Use default 10-point scale
result = grade_essay("essay.pdf")

# Custom point scale (e.g., out of 50)
rubric_50 = DEFAULT_ESSAY_RUBRIC.copy()
rubric_50["scale_total"] = 50
rubric_50["criteria"] = [
    {**c, "max_points": c["max_points"] * 5} 
    for c in DEFAULT_ESSAY_RUBRIC["criteria"]
]
result = grade_essay("essay.pdf", rubric=rubric_50)
# Output: "42.5/50"
```

### 2. Pass/Fail

Grades are displayed as "Pass" or "Fail" based on a percentage threshold.

```python
from essay_grader import DEFAULT_ESSAY_RUBRIC

# Default threshold is 70%
rubric_pf = DEFAULT_ESSAY_RUBRIC.copy()
rubric_pf["grading_scale_type"] = "pass_fail"
result = grade_essay("essay.pdf", rubric=rubric_pf)
# Output: "Pass" or "Fail"

# Custom threshold (e.g., 60% to pass)
rubric_pf_custom = DEFAULT_ESSAY_RUBRIC.copy()
rubric_pf_custom["grading_scale_type"] = "pass_fail"
rubric_pf_custom["pass_threshold"] = 60
result = grade_essay("essay.pdf", rubric=rubric_pf_custom)
```

### 3. Letter Grade

Grades are displayed as "A", "B", "C", "D", or "F".

```python
from essay_grader import DEFAULT_ESSAY_RUBRIC

# Default boundaries: A=90%, B=80%, C=70%, D=60%
rubric_letter = DEFAULT_ESSAY_RUBRIC.copy()
rubric_letter["grading_scale_type"] = "letter_grade"
result = grade_essay("essay.pdf", rubric=rubric_letter)
# Output: "A", "B", "C", "D", or "F"

# Custom boundaries (with plus/minus)
rubric_letter_custom = DEFAULT_ESSAY_RUBRIC.copy()
rubric_letter_custom["grading_scale_type"] = "letter_grade"
rubric_letter_custom["grade_boundaries"] = {
    "A": 93.0,
    "A-": 90.0,
    "B+": 87.0,
    "B": 83.0,
    "B-": 80.0,
    "C+": 77.0,
    "C": 73.0,
    "C-": 70.0,
    "D": 60.0,
    "F": 0.0,
}
result = grade_essay("essay.pdf", rubric=rubric_letter_custom)
# Output: "A", "A-", "B+", "B", "B-", etc.
```

## Rubric Configuration

### Default Essay Rubric

The system includes a default essay rubric:

```python
DEFAULT_ESSAY_RUBRIC = {
    "type": "ESSAY",
    "grading_scale_type": "points",  # or "pass_fail" or "letter_grade"
    "scale_total": 10,
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
}
```

### Custom Rubric

Create a completely custom rubric:

```python
custom_rubric = {
    "type": "ESSAY",
    "grading_scale_type": "letter_grade",
    "scale_total": 100,
    "grade_boundaries": {
        "A": 90.0,
        "B": 80.0,
        "C": 70.0,
        "D": 60.0,
        "F": 0.0,
    },
    "criteria": [
        {
            "id": "content",
            "name": "Content & Analysis",
            "max_points": 40,
            "description": "Depth of analysis, critical thinking.",
        },
        {
            "id": "structure",
            "name": "Structure & Organization",
            "max_points": 30,
            "description": "Logical flow, clear structure.",
        },
        {
            "id": "style",
            "name": "Style & Voice",
            "max_points": 20,
            "description": "Writing style, clarity.",
        },
        {
            "id": "mechanics",
            "name": "Grammar & Mechanics",
            "max_points": 10,
            "description": "Spelling, grammar, punctuation.",
        },
    ],
}

result = grade_essay("essay.pdf", rubric=custom_rubric)
```

## API Reference

### `grade_essay(essay_input, rubric=None)`

Grade an essay using Google Gemini API.

**Parameters:**
- `essay_input` (str): Essay text string OR file path (PDF/image/TXT)
- `rubric` (dict | str | None): Rubric configuration (uses default if None)

**Returns:**
A dictionary with the following fields:

```python
{
    # Score Information
    "score_total": float,              # Raw points earned
    "score_percentage": float,         # Percentage of total points
    "final_grade": str,                # Formatted based on grading_scale_type
    "score_breakdown": [dict],         # Per-criterion scores
    
    # Feedback
    "feedback_short": str,             # Brief summary
    "feedback_detailed": {
        "overall": str,                # Overall assessment
        "strengths": [str],            # List of strengths
        "weaknesses": [str],           # List of weaknesses
        "criteria_feedback": [dict],   # Per-criterion feedback
        "grammar_issues": [dict],      # Grammar corrections
        "suggestions": [str],          # Improvement suggestions
    },
    
    # Metadata
    "flags": [dict],                   # Any issues or warnings
    "confidence": float,               # AI confidence (0-1)
    "grading_time_seconds": float,     # Time taken to grade
}
```

## Running the Server

```bash
# Development server
uv run fastapi dev main.py

# Production server
uv run fastapi run main.py
```

The server will be available at `http://localhost:8000`

## API Endpoints

See `main.py` for available endpoints. Common endpoints include:

- `POST /grade` - Submit an essay for grading
- `GET /rubric` - Get default rubric
- `POST /rubric` - Submit custom rubric

## Testing

```bash
# Run tests (if pytest is configured)
uv run python -m pytest
```

## Example Scripts

See `example_grading_scales.py` for comprehensive examples of all grading scale configurations.

## Frontend Integration

To integrate with the frontend, send rubric configurations with grading scale settings. The `/api/grade` endpoint accepts:
- `essay`: File upload (PDF, image, or TXT)
- `rubric`: Optional file upload (JSON or text)
- `rubric_json`: Optional JSON string with rubric configuration

### Example 1: Points-Based Grading

```typescript
// Build rubric for points-based grading (out of 100)
const pointsRubric = {
  type: "ESSAY",
  grading_scale_type: "points",
  scale_total: 100,
  criteria: [
    {
      id: "thesis",
      name: "Thesis/Claim",
      max_points: 20,
      description: "Clear, specific main claim."
    },
    {
      id: "evidence",
      name: "Evidence/Support",
      max_points: 30,
      description: "Uses relevant evidence/examples and explains them."
    },
    {
      id: "organization",
      name: "Organization",
      max_points: 20,
      description: "Logical flow; clear structure."
    },
    {
      id: "clarity",
      name: "Clarity",
      max_points: 20,
      description: "Clear wording; minimal ambiguity."
    },
    {
      id: "grammar",
      name: "Grammar/Mechanics",
      max_points: 10,
      description: "Few grammar/spelling errors."
    }
  ]
};

// Send to backend using FormData
const formData = new FormData();
formData.append('essay', essayFile);
formData.append('rubric_json', JSON.stringify(pointsRubric));

const response = await fetch('/api/grade', {
  method: 'POST',
  body: formData
});

const result = await response.json();
// result.final_grade will be e.g., "85/100"
```

### Example 2: Pass/Fail Grading

```typescript
// Build rubric for pass/fail grading (70% threshold)
const passFailRubric = {
  type: "ESSAY",
  grading_scale_type: "pass_fail",
  pass_threshold: 70,  // 70% to pass
  scale_total: 10,
  criteria: [
    {
      id: "thesis",
      name: "Thesis/Claim",
      max_points: 2,
      description: "Clear, specific main claim."
    },
    {
      id: "evidence",
      name: "Evidence/Support",
      max_points: 3,
      description: "Uses relevant evidence/examples and explains them."
    },
    {
      id: "organization",
      name: "Organization",
      max_points: 2,
      description: "Logical flow; clear structure."
    },
    {
      id: "clarity",
      name: "Clarity",
      max_points: 2,
      description: "Clear wording; minimal ambiguity."
    },
    {
      id: "grammar",
      name: "Grammar/Mechanics",
      max_points: 1,
      description: "Few grammar/spelling errors."
    }
  ]
};

const formData = new FormData();
formData.append('essay', essayFile);
formData.append('rubric_json', JSON.stringify(passFailRubric));

const response = await fetch('/api/grade', {
  method: 'POST',
  body: formData
});

const result = await response.json();
// result.final_grade will be "Pass" or "Fail"
```

### Example 3: Letter Grade Grading

```typescript
// Build rubric for letter grade grading with plus/minus
const letterGradeRubric = {
  type: "ESSAY",
  grading_scale_type: "letter_grade",
  scale_total: 100,
  grade_boundaries: {
    "A": 93.0,
    "A-": 90.0,
    "B+": 87.0,
    "B": 83.0,
    "B-": 80.0,
    "C+": 77.0,
    "C": 73.0,
    "C-": 70.0,
    "D": 60.0,
    "F": 0.0
  },
  criteria: [
    {
      id: "thesis",
      name: "Thesis/Claim",
      max_points: 20,
      description: "Clear, specific main claim."
    },
    {
      id: "evidence",
      name: "Evidence/Support",
      max_points: 30,
      description: "Uses relevant evidence/examples and explains them."
    },
    {
      id: "organization",
      name: "Organization",
      max_points: 20,
      description: "Logical flow; clear structure."
    },
    {
      id: "clarity",
      name: "Clarity",
      max_points: 20,
      description: "Clear wording; minimal ambiguity."
    },
    {
      id: "grammar",
      name: "Grammar/Mechanics",
      max_points: 10,
      description: "Few grammar/spelling errors."
    }
  ]
};

const formData = new FormData();
formData.append('essay', essayFile);
formData.append('rubric_json', JSON.stringify(letterGradeRubric));

const response = await fetch('/api/grade', {
  method: 'POST',
  body: formData
});

const result = await response.json();
// result.final_grade will be e.g., "A-", "B+", "C", "F"
```

### Interactive Grading Scale Selection in Frontend

Create a UI component that lets the professor select the grading scale:

```svelte
<script lang="ts">
  import type { GradingScaleType } from '$lib/types';

  let gradingScaleType: GradingScaleType = 'points';
  let totalPoints = 100;
  let passThreshold = 70;
  let gradeBoundaries = {
    'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 0
  };

  async function submitEssay(essayFile: File) {
    const rubric = {
      type: "ESSAY",
      grading_scale_type: gradingScaleType,
      scale_total: totalPoints,
      ...(gradingScaleType === 'pass_fail' && { pass_threshold: passThreshold }),
      ...(gradingScaleType === 'letter_grade' && { grade_boundaries: gradeBoundaries }),
      criteria: [...]
    };

    const formData = new FormData();
    formData.append('essay', essayFile);
    formData.append('rubric_json', JSON.stringify(rubric));

    const response = await fetch('/api/grade', {
      method: 'POST',
      body: formData
    });

    return await response.json();
  }
</script>

<div class="grading-scale-selector">
  <h3>Choose Grading Scale:</h3>
  
  <select bind:value={gradingScaleType}>
    <option value="points">Points-based</option>
    <option value="pass_fail">Pass/Fail</option>
    <option value="letter_grade">Letter Grade</option>
  </select>

  {#if gradingScaleType === 'points'}
    <input type="number" bind:value={totalPoints} placeholder="Total points (e.g., 100)" />
  {:else if gradingScaleType === 'pass_fail'}
    <input type="number" bind:value={passThreshold} placeholder="Pass threshold % (e.g., 70)" />
  {:else if gradingScaleType === 'letter_grade'}
    <div class="grade-boundaries">
      <label>Grade Boundaries:</label>
      <!-- Allow custom boundary configuration -->
    </div>
  {/if}
</div>
```

### API Response Format

The API returns a grading result with the following structure:

```typescript
interface GradingResult {
  score_total: number;
  score_percentage: number;
  final_grade: string;  // Formatted based on grading_scale_type
  score_breakdown: Array<{
    criterion_id: string;
    points: number;
    max_points: number;
    rationale: string;
  }>;
  feedback_short: string;
  feedback_detailed: {
    overall: string;
    strengths: string[];
    weaknesses: string[];
    criteria_feedback: Array<{
      criterion_id: string;
      status: string;
      feedback: string;
      how_to_improve: string;
    }>;
    grammar_issues: Array<{
      location: string;
      original: string;
      correction: string;
      rule: string;
    }>;
    suggestions: string[];
  };
  flags: Array<{ code: string; message: string }>;
  confidence: number;  // 0-1
  grading_time_seconds: number;
}
```

## License

See project root for license information.