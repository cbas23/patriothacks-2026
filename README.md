# AI Essay Grader

An AI-powered essay grading application built for **PatriotHacks 2026**. Save time and ensure consistency by automatically grading student essays against your custom rubrics.

## Features

- **AI-Powered Grading**: Leverages Google Gemini to evaluate essays against your rubric
- **Multi-Format Support**: Accepts PDF, TXT, PNG, JPG, and more
- **Detailed Feedback**: Provides criterion-by-criterion scores and feedback
- **Batch Processing**: Grade multiple essays at once
- **Fast & Accurate**: Get results in seconds, not hours

## Tech Stack

- **Frontend**: SvelteKit, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **AI**: Google Gemini 3 Flash (2.0 flash for fallback)

## Getting Started

### Prerequisites

- [Bun](https://bun.sh/) for the frontend
- [Python 3.12+](https://www.python.org/) for the backend
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd patriothacks2026
```

2. **Set up the backend**

```bash
cd backend
cp .env.example .env  # or create .env manually
# Add your GEMINI_API_KEY to .env
uv sync
```

3. **Set up the frontend**

```bash
cd frontend
bun install
```

### Running the Application

**Backend** (Terminal 1):

```bash
cd backend
uv run fastapi dev main.py
```

The API will be available at `http://localhost:8000`

**Frontend** (Terminal 2):

```bash
cd frontend
bun run dev
```

The app will be available at `http://localhost:5173`

## Usage

1. Navigate to the grader page
2. Upload your grading rubric (PDF, Image or TXT)
3. Upload student essays (single or multiple)
4. Add optional instructor notes for context
5. Click "Grade" and receive instant feedback

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/api/health` | GET | Health check |
| `/api/gradev2` | POST | Grade a single essay |

## Environment Variables

### Backend

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key (required) |
| `GEMINI_MODEL` | Model to use (default: `gemini-2.0-flash`) |

## Project Structure

```
patriothacks2026/
├── frontend/          # SvelteKit frontend
│   ├── src/
│   │   ├── lib/      # Shared components
│   │   └── routes/   # App routes
│   └── package.json
└── backend/          # FastAPI backend
    ├── main.py       # API entry point
    ├── services/     # Business logic
    └── pyproject.toml
```

## License

MIT
