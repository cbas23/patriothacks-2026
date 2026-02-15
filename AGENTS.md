# Agent Guidelines for This Project

This is a monorepo with a SvelteKit frontend and FastAPI backend.

## Project Structure

```
patriothacks2026/
├── frontend/          # SvelteKit + TypeScript + Tailwind CSS + Vitest
│   ├── src/
│   │   ├── lib/      # Shared components and utilities ($lib alias)
│   │   └── routes/   # SvelteKit routes
│   └── package.json
└── backend/          # Python FastAPI
    ├── main.py       # FastAPI app entry point
    ├── essay_grader.py  # Essay grading logic
    └── pyproject.toml
```

## Build/Lint/Test Commands

### Frontend (SvelteKit)

| Command | Description |
|---------|-------------|
| `bun install` | Install dependencies |
| `bun run dev` | Start development server |
| `bun run build` | Production build |
| `bun run lint` | Run ESLint + Prettier checks |
| `bun run format` | Format code with Prettier |
| `bun run check` | Run Svelte check + TypeScript |
| `bun run test` | Run all unit tests (Vitest) |
| `bun run test:unit` | Run tests in watch mode |

**Run a single test:**
```bash
# Run a specific test file
bun vitest run src/routes/page.svelte.spec.ts

# Run tests matching a pattern
bun vitest run --grep "should render"
```

### Backend (FastAPI)

```bash
cd backend
uv sync          # Install dependencies
uv run fastapi dev main.py  # Start dev server
uv run python -m pytest     # Run tests (if pytest configured)
```

## Code Style Guidelines

### TypeScript (Frontend)

- **Use TypeScript for all new code** with strict mode enabled
- **Enable strict type checking** in tsconfig.json
- **Prefer interfaces over types** for object shapes
- **Use explicit return types** for functions where helpful

### Svelte 5

This project uses Svelte 5 with runes (`$state`, `$props`, `$derived`, `$effect`).

```svelte
<script lang="ts">
  let { value = $bindable(0), label }: { value: number, label: string } = $props();
</script>
```

### Imports

- Use ES module imports (`import`/`export`)
- Use absolute imports with `$lib` alias for project code
- Group imports: external libraries first, then internal modules

```typescript
// External
import { useState } from 'svelte';
import { cn } from 'clsx';

// Internal
import { Button } from '$lib/components/ui/button';
import { calculateScore } from '$lib/utils';
```

### Naming Conventions

- **Variables/functions:** camelCase
- **Classes/interfaces/types:** PascalCase
- **Files:** kebab-case (e.g., `essay-grader.ts`)
- **Constants:** UPPER_SNAKE_CASE
- **Components:** PascalCase (e.g., `Button.svelte`)

### Formatting

- Uses **Prettier** with:
  - Single quotes (`'`)
  - Tabs for indentation
  - 100 character line width
  - No trailing commas

- Run `bun run format` before committing

### Error Handling

- Use try-catch blocks for async operations
- Return proper error types with meaningful messages
- For FastAPI: use HTTPException for HTTP errors, custom exceptions for business logic
- Frontend: handle errors gracefully with user feedback

### Python (Backend)

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return types
- Use `python-dotenv` for environment variables (see `.env` file)
- Use `pydantic` for data validation in FastAPI

## Testing

### Frontend Tests (Vitest)

- Tests live alongside components with `.spec.ts` or `.test.ts` suffix
- Use `vitest-browser-svelte` for component testing
- Use Playwright for browser testing

```typescript
import { render } from 'vitest-browser-svelte';
import Page from './+page.svelte';

describe('/+page.svelte', () => {
  it('should render', async () => {
    render(Page);
    // assertions...
  });
});
```

### Running Tests

```bash
# All tests
bun run test

# Single file
bun vitest run src/routes/page.svelte.spec.ts

# Watch mode
bun run test:unit
```

## Environment Variables

### Frontend
- No required env vars for development

### Backend
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` - For AI grading (optional, falls back to mock)
- `GEMINI_MODEL` - Model to use (default: `gemini-2.0-flash`)

## Important File Patterns

- UI components: `src/lib/components/ui/[component-name]/`
- Utilities: `src/lib/utils.ts`
- Routes: `src/routes/[path]/+page.svelte`
- Route tests: `src/routes/[path]/+page.svelte.spec.ts`

## Lint/Typecheck Before Commit

Always run before committing:

```bash
cd frontend
bun run lint
bun run check
```

## Additional Notes

- The frontend uses **shadcn-svelte** for UI components (built on Tailwind CSS)
- The frontend uses Tailwind CSS v4 with `@tailwindcss/vite`
- The project uses bun as the package manager
- SvelteKit is configured with adapter-auto
- ESLint is configured with TypeScript and Svelte plugins
- Use lucide svelte icons, here's an example of how to use them:

```svelte
<script>
  import { Skull } from '@lucide/svelte';
</script>

<Skull />
```

### Adding New shadcn Components

```bash
# Add a new shadcn component
cd frontend
bunx shadcn-svelte@latest add button
```

### shadcn Component Structure

Components are stored in `src/lib/components/ui/[component-name]/` with:
- `[component-name].svelte` - The main component
- `index.ts` - Barrel export
