<script lang="ts">
	import FilePit from '$lib/file-pit.svelte';
	import { Label } from '$lib/components/ui/label';

	interface Props {
		rubricFile: FileList | null;
		feedbackType: string;
	}

	let { rubricFile = $bindable(null), feedbackType = $bindable('') }: Props = $props();
</script>

<div class="space-y-6">
	<div>
		<h2 class="mb-1 text-xl font-semibold">Upload Rubric</h2>
		<p class="text-sm text-muted-foreground">Upload your grading rubric file (PDF, Image, or TXT)</p>
	</div>

	<div class="space-y-2">
		<Label for="rubric-file">Rubric File</Label>
		<FilePit bind:value={rubricFile} accept=".pdf,.txt" multiple={false} />
	</div>

	<div class="space-y-2">
		<Label for="feedback-type">Feedback Approach</Label>
		<p class="text-xs text-muted-foreground">
			Describe the type of feedback you want the grader to provide
		</p>
		<textarea
			id="feedback-type"
			bind:value={feedbackType}
			placeholder="e.g., Provide constructive criticism with specific examples, encouraging tone with actionable suggestions, detailed feedback focusing on clarity and structure..."
			class="min-h-30 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50"
		></textarea>
	</div>
</div>
