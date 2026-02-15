<script lang="ts">
	import { ChevronLeft, ChevronRight, Loader2 } from '@lucide/svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import Stepper from '$lib/components/stepper.svelte';
	import RubricStep from '$lib/components/grader/rubric-step.svelte';
	import StudentFilesStep from '$lib/components/grader/student-files-step.svelte';
	import ReviewStep from '$lib/components/grader/review-step.svelte';
	import GraderLoading from '$lib/components/grader/grader-loading.svelte';
	import GraderFinished from '$lib/components/grader/grader-finished.svelte';
	import { type GradingResult } from '$lib/types/grading';
	import { env } from '$env/dynamic/public';

	let currentStep = $state(0);
	let rubricFile = $state<FileList | null>(null);
	let feedbackType = $state('');
	let studentFiles = $state<FileList | null>(null);
	let isGrading = $state(false);
	let isFinished = $state(false);
	let gradingResults = $state<GradingResult[]>([]);
	let gradingError = $state<string | null>(null);
	let preFetchedResults = $state<GradingResult[]>([]);
	let preFetchError = $state<string | null>(null);

	const steps = [
		{ title: 'Rubric', description: 'Upload rubric & feedback type' },
		{ title: 'Assignments', description: 'Upload essays to grade' },
		{ title: 'Review', description: 'Confirm & submit' }
	];

	function nextStep() {
		if (currentStep === 1 && preFetchedResults.length > 0) {
			gradingResults = preFetchedResults;
		}
		if (currentStep < 2) currentStep++;
	}

	function prevStep() {
		if (currentStep === 2) {
			preFetchedResults = [];
			preFetchError = null;
			gradingResults = [];
			gradingError = null;
		}
		if (currentStep > 0) currentStep--;
	}

	async function handleSubmit() {
		if (preFetchedResults.length > 0) {
			gradingResults = preFetchedResults;
			isFinished = true;
			return;
		}

		if (!rubricFile || !studentFiles) return;

		isGrading = true;
		gradingError = null;

		try {
			const rubricData = rubricFile[0];
			const studentFileList = Array.from(studentFiles);

			console.log('[Grader] Starting concurrent grading', {
				rubric: rubricData.name,
				studentFiles: studentFileList.map((f) => f.name),
				notes: feedbackType
			});

			const gradingPromises = studentFileList.map(async (studentFile) => {
				const formData = new FormData();
				formData.append('rubric', rubricData);
				formData.append('assignment', studentFile);
				if (feedbackType) {
					formData.append('notes', feedbackType);
				}

				console.log('[Grader] Submitting:', studentFile.name);

				const response = await fetch(`${env.PUBLIC_BACKEND_URL}/api/gradev2/`, {
					method: 'POST',
					body: formData
				});

				if (!response.ok) {
					const errorData = await response.json().catch(() => ({}));
					throw new Error(errorData.error || `HTTP ${response.status}`);
				}

				const result = await response.json();
				console.log('[Grader] Completed:', studentFile.name, result);
				return result;
			});

			const results = await Promise.all(gradingPromises);
			console.log('[Grader] All grading complete', { total: results.length });

			gradingResults = results;
		} catch (err) {
			gradingError = err instanceof Error ? err.message : 'Grading failed';
			console.error('[Grader] Error:', gradingError);
			return;
		} finally {
			isGrading = false;
		}

		if (gradingError === null) {
			isFinished = true;
		}
	}

	async function prefetchGrading() {
		if (!rubricFile || !studentFiles || preFetchedResults.length > 0 || preFetchError) return;

		preFetchError = null;

		try {
			const rubricData = rubricFile[0];
			const studentFileList = Array.from(studentFiles);

			console.log('[Grader] Prefetching grading', {
				rubric: rubricData.name,
				studentFiles: studentFileList.map((f) => f.name)
			});

			const gradingPromises = studentFileList.map(async (studentFile) => {
				const formData = new FormData();
				formData.append('rubric', rubricData);
				formData.append('assignment', studentFile);
				if (feedbackType) {
					formData.append('notes', feedbackType);
				}

				const response = await fetch(`${env.PUBLIC_BACKEND_URL}/api/gradev2/`, {
					method: 'POST',
					body: formData
				});

				if (!response.ok) {
					const errorData = await response.json().catch(() => ({}));
					throw new Error(errorData.error || `HTTP ${response.status}`);
				}

				return response.json();
			});

			const results = await Promise.all(gradingPromises);
			preFetchedResults = results;
		} catch (err) {
			preFetchError = err instanceof Error ? err.message : 'Prefetch failed';
			console.error('[Grader] Prefetch error:', preFetchError);
		}
	}
</script>

{#if isGrading}
	<GraderLoading />
{:else if isFinished}
	<GraderFinished results={gradingResults} />
{:else}
	<div class="h-[calc(100vh-4rem)] bg-background p-4 text-foreground md:p-8">
		<div class="mx-auto max-w-3xl">
			<h1 class="mb-8 text-center text-3xl font-bold md:text-4xl">Grading Portal</h1>

			<Stepper {steps} {currentStep} />

			<Card.Root class="mt-10 border-2 shadow-xl">
				<Card.Content class="pt-6">
					{#if gradingError}
						<div
							class="mb-4 rounded-md bg-red-50 p-4 text-red-600 dark:bg-red-900/20 dark:text-red-400"
						>
							{gradingError}
						</div>
					{/if}

					{#if currentStep === 0}
						<RubricStep bind:rubricFile bind:feedbackType />
					{:else if currentStep === 1}
						<StudentFilesStep bind:studentFiles />
					{:else if currentStep === 2}
						<ReviewStep {rubricFile} {feedbackType} {studentFiles} />
					{/if}

					<div class="mt-8 flex justify-between">
						<Button variant="outline" onclick={prevStep} disabled={currentStep === 0}>
							<ChevronLeft class="mr-2 size-4" />
							Back
						</Button>

						{#if currentStep < 2}
							<Button
								onclick={nextStep}
								onmouseenter={currentStep === 1 ? prefetchGrading : undefined}
							>
								Next
								<ChevronRight class="ml-2 size-4" />
							</Button>
						{:else}
							<Button onclick={handleSubmit} disabled={isGrading}>
								{#if isGrading}
									<Loader2 class="mr-2 size-4 animate-spin" />
									Grading...
								{:else}
									Start Grading
								{/if}
							</Button>
						{/if}
					</div>
				</Card.Content>
			</Card.Root>
		</div>
	</div>
{/if}

<style>
	:global(body) {
		overflow: hidden;
	}
</style>
