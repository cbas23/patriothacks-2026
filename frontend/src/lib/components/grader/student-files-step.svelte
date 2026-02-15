<script lang="ts">
	import FilePit from '$lib/file-pit.svelte';
	import { Label } from '$lib/components/ui/label';

	interface Props {
		studentFiles: FileList | null;
	}

	let { studentFiles = $bindable(null) }: Props = $props();
</script>

<div class="space-y-6">
	<div>
		<h2 class="mb-1 text-xl font-semibold">Upload Student Essays</h2>
		<p class="text-sm text-muted-foreground">Upload one or more student essay files to grade</p>
	</div>

	<div class="space-y-2">
		<Label for="student-files">Student Essays</Label>
		<FilePit bind:value={studentFiles} accept=".pdf,.txt" multiple />
	</div>
</div>
