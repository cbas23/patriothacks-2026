<script lang="ts">
	interface Props {
		rubricFile: FileList | null;
		feedbackType: string;
		studentFiles: FileList | null;
	}

	let { rubricFile, feedbackType, studentFiles }: Props = $props();
</script>

<div class="space-y-6">
	<div>
		<h2 class="mb-1 text-xl font-semibold">Review & Submit</h2>
		<p class="text-sm text-muted-foreground">Review your inputs before grading begins</p>
	</div>

	<div class="space-y-4 rounded-lg border bg-muted/50 p-4">
		<div>
			<h3 class="font-medium">Rubric File</h3>
			<p class="text-sm text-muted-foreground">
				{rubricFile?.length ? rubricFile[0]?.name : 'No file uploaded'}
			</p>
		</div>

		<div>
			<h3 class="font-medium">Feedback Approach</h3>
			<p class="text-sm text-muted-foreground">
				{feedbackType || 'Not specified'}
			</p>
		</div>

		<div>
			<h3 class="font-medium">Student Essays</h3>
			<p class="text-sm text-muted-foreground">
				{studentFiles?.length || 0} file(s) selected
			</p>
			{#if studentFiles && studentFiles.length > 0}
				<ul class="mt-2 space-y-1">
					{#each Array.from(studentFiles) as file, i (file.name + '-' + i)}
						<li class="text-sm text-muted-foreground">• {file.name}</li>
					{/each}
				</ul>
			{/if}
		</div>
	</div>
</div>
