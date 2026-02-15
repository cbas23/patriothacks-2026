<script lang="ts">
	import type { GradingResult } from '$lib/types/grading';
	import * as Accordion from '$lib/components/ui/accordion';
	import * as Resizable from '$lib/components/ui/resizable';
	import { Check, AlertTriangle, X } from '@lucide/svelte';

	interface Props {
		results: GradingResult[];
	}

	let { results }: Props = $props();

	console.log('===Grading results===', results);

	let selectedIndex = $state(0);

	function getGradePercentage(result: GradingResult): number {
		const totalScore = result.criteria_feedback.reduce((sum, c) => sum + c.score, 0);
		const totalMax = result.criteria_feedback.reduce((sum, c) => sum + c.score_max, 0);
		return totalMax > 0 ? Math.round((totalScore / totalMax) * 100) : 0;
	}

	function getCriteriaStatus(score: number, maxScore: number): 'perfect' | 'warning' | 'fail' {
		const percentage = score / maxScore;
		if (percentage === 1) return 'perfect';
		if (percentage > 0.6) return 'warning';
		return 'fail';
	}

	function selectStudent(index: number) {
		selectedIndex = index;
	}

	$effect(() => {
		if (results.length > 0 && selectedIndex >= results.length) {
			selectedIndex = 0;
		}
	});
</script>

<Resizable.PaneGroup direction="horizontal" class="h-[calc(100vh-4rem)]">
	<!-- Column 1: Student List -->
	<Resizable.Pane defaultSize={20} minSize={15} maxSize={35}>
		<div class="flex h-full flex-col gap-2 overflow-y-auto border-r p-4">
			<h2 class="text-lg font-semibold">Students</h2>
			{#each results as result, index (result.name)}
				<button
					type="button"
					class="flex h-auto flex-col items-start justify-start gap-1 rounded-md border bg-background px-3 py-2 text-left transition-colors hover:bg-muted {selectedIndex ===
					index
						? 'border-primary bg-primary/10'
						: ''}"
					onclick={() => selectStudent(index)}
				>
					<span class="font-medium">{result.name}</span>
					<span class="text-sm text-muted-foreground">
						Grade: {getGradePercentage(result)}%
					</span>
				</button>
			{/each}
		</div>
	</Resizable.Pane>

	<Resizable.Handle />

	<!-- Column 2: Submitted Images -->
	<Resizable.Pane defaultSize={50} minSize={30}>
		<div class="flex h-full flex-col overflow-y-auto border-r p-4">
			<h2 class="mb-4 text-lg font-semibold">Submitted Items</h2>
			{#if results[selectedIndex]}
				{@const student = results[selectedIndex]}
				<div class="flex flex-col gap-4">
					{#if student.images && student.images.length > 0}
						{#each student.images as image, i (i)}
							<img
								src="data:image/png;base64,{image}"
								alt="Submission page {i + 1} for {student.name}"
								class="w-full rounded-lg object-contain"
							/>
						{/each}
					{:else}
						<div class="flex h-48 w-full items-center justify-center rounded-lg bg-muted">
							<span class="text-muted-foreground">No preview available</span>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</Resizable.Pane>

	<Resizable.Handle />

	<!-- Column 3: Grade Details -->
	<Resizable.Pane defaultSize={30} minSize={20} maxSize={50}>
		<div class="flex h-full flex-col overflow-y-auto">
			<h2 class="m-4 mb-4 text-lg font-semibold">Grade Details</h2>
			{#if results[selectedIndex]}
				{@const student = results[selectedIndex]}
				<Accordion.Root type="single" class="w-full">
					{#each student.criteria_feedback as criteria, i (criteria.criteria_title)}
						{@const status = getCriteriaStatus(criteria.score, criteria.score_max)}
						<Accordion.Item value="item-{i}">
							<Accordion.Trigger class="px-4 text-left">
								<span
									class="mr-2 flex size-5 shrink-0 items-center justify-center rounded-sm {status ===
									'perfect'
										? 'bg-green-900'
										: status === 'warning'
											? 'bg-yellow-900'
											: 'bg-red-900'}"
								>
									{#if status === 'perfect'}
										<Check class="size-3 text-green-200" />
									{:else if status === 'warning'}
										<AlertTriangle class="size-3 text-yellow-200" />
									{:else}
										<X class="size-3 text-red-200" />
									{/if}
								</span>
								<span class="flex-1">{criteria.criteria_title}</span>
								<span class="ml-2 text-sm text-muted-foreground">
									{criteria.score}/{criteria.score_max}
								</span>
							</Accordion.Trigger>
							<Accordion.Content>
								<p class="px-4 text-sm text-muted-foreground">{criteria.feedback}</p>
							</Accordion.Content>
						</Accordion.Item>
					{/each}
				</Accordion.Root>
			{/if}
		</div>
	</Resizable.Pane>
</Resizable.PaneGroup>
