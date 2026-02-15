import { z } from "zod/v4";
import { join } from "path";

const BASE_URL = process.env.API_URL ?? "http://localhost:8000";
const ASSETS = join(import.meta.dirname, "assets");

const RootSchema = z.object({
	service: z.string(),
});

const HealthSchema = z.object({
	status: z.literal("ok"),
	gemini_configured: z.boolean(),
	model: z.string(),
});

const CriteriaFeedbackSchema = z.object({
	criteria_title: z.string(),
	score: z.number(),
	score_max: z.number(),
	feedback: z.string(),
});

const GradeSuccessSchema = z.object({
	name: z.string(),
	overall_feedback: z.string(),
	criteria_feedback: z.array(CriteriaFeedbackSchema),
});

const GradeErrorSchema = z.object({
	error: z.string(),
	detail: z.string().optional(),
});

const BatchResultItemSchema = z.union([
	GradeSuccessSchema,
	z.object({ name: z.string(), error: z.string() }),
]);

const BatchResponseSchema = z.object({
	results: z.array(BatchResultItemSchema),
	total: z.number(),
});

async function loadFile(name: string): Promise<File> {
	const buf = await Bun.file(join(ASSETS, name)).arrayBuffer();
	return new File([buf], name);
}

let passed = 0;
let failed = 0;

async function test(name: string, fn: () => Promise<void>) {
	try {
		await fn();
		passed++;
		console.log(`  ✓ ${name}`);
	} catch (e) {
		failed++;
		console.error(`  ✗ ${name}`);
		console.error(`    ${e instanceof Error ? e.message : e}`);
	}
}

function assert(condition: boolean, msg: string) {
	if (!condition) throw new Error(msg);
}

console.log("\n=== Backend API Tests ===\n");

console.log("GET /");
await test("returns service name", async () => {
	const res = await fetch(`${BASE_URL}/`);
	assert(res.ok, `status ${res.status}`);
	const body = RootSchema.parse(await res.json());
	assert(body.service === "Essay Auto-Grading API", `unexpected service: ${body.service}`);
});

console.log("\nGET /api/health");
await test("returns health status", async () => {
	const res = await fetch(`${BASE_URL}/api/health`);
	assert(res.ok, `status ${res.status}`);
	HealthSchema.parse(await res.json());
});

console.log("\nPOST /api/grade");
await test("grades a txt assignment with rubric", async () => {
	const form = new FormData();
	form.append("assignments", await loadFile("message.txt"));
	form.append("rubric", await loadFile("rubric.png"));

	const res = await fetch(`${BASE_URL}/api/grade`, { method: "POST", body: form });
	assert(res.ok, `status ${res.status}`);
	const body = await res.json();
	const parsed = GradeSuccessSchema.safeParse(body);
	if (!parsed.success) {
		const err = GradeErrorSchema.safeParse(body);
		if (err.success) throw new Error(`API error: ${err.data.error}`);
		throw new Error(`Invalid response shape: ${JSON.stringify(body).slice(0, 200)}`);
	}
	assert(parsed.data.criteria_feedback.length > 0, "expected at least one criteria");
});

await test("grades a pdf assignment with rubric", async () => {
	const form = new FormData();
	form.append("assignments", await loadFile("Initial Draft WonJune Lee.pdf"));
	form.append("rubric", await loadFile("rubric.png"));

	const res = await fetch(`${BASE_URL}/api/grade`, { method: "POST", body: form });
	assert(res.ok, `status ${res.status}`);
	const body = await res.json();
	const parsed = GradeSuccessSchema.safeParse(body);
	if (!parsed.success) {
		const err = GradeErrorSchema.safeParse(body);
		if (err.success) throw new Error(`API error: ${err.data.error}`);
		throw new Error(`Invalid response shape: ${JSON.stringify(body).slice(0, 200)}`);
	}
});

await test("accepts optional feedback_approach", async () => {
	const form = new FormData();
	form.append("assignments", await loadFile("message.txt"));
	form.append("rubric", await loadFile("rubric.png"));
	form.append("feedback_approach", "Be very detailed and constructive");

	const res = await fetch(`${BASE_URL}/api/grade`, { method: "POST", body: form });
	assert(res.ok, `status ${res.status}`);
	const body = await res.json();
	GradeSuccessSchema.parse(body);
});

console.log("\nPOST /api/grade/batch");
await test("grades multiple assignments in batch", async () => {
	const form = new FormData();
	form.append("assignments", await loadFile("message.txt"));
	form.append("assignments", await loadFile("Initial Draft WonJune Lee.pdf"));
	form.append("rubric", await loadFile("rubric.png"));

	const res = await fetch(`${BASE_URL}/api/grade/batch`, { method: "POST", body: form });
	assert(res.ok, `status ${res.status}`);
	const body = BatchResponseSchema.parse(await res.json());
	assert(body.total === 2, `expected total=2, got ${body.total}`);
	assert(body.results.length === 2, `expected 2 results, got ${body.results.length}`);
});

console.log("\n---");
console.log(`Results: ${passed} passed, ${failed} failed, ${passed + failed} total\n`);
process.exit(failed > 0 ? 1 : 0);
