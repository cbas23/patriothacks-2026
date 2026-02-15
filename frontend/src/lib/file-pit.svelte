<script lang="ts">
	import { cn } from '$lib/utils.js';

	interface Props {
		class?: string;
		accept?: string;
		multiple?: boolean;
		value?: FileList | null;
		onchange?: (files: FileList | null) => void;
	}

	let {
		class: className,
		accept = 'application/pdf,image/*,.doc,.docx,.txt',
		multiple = true,
		value = $bindable(null),
		onchange
	}: Props = $props();

	let isDragging = $state(false);
	let inputRef: HTMLInputElement | null = $state(null);

	function handleClick() {
		inputRef?.click();
	}

	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		isDragging = true;
	}

	function handleDragLeave(e: DragEvent) {
		e.preventDefault();
		isDragging = false;
	}

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		isDragging = false;
		const files = e.dataTransfer?.files ?? null;
		if (files && files.length > 0) {
			value = files;
			onchange?.(files);
		}
	}

	function handleInputChange(e: Event) {
		const target = e.target as HTMLInputElement;
		const files = target.files;
		value = files;
		onchange?.(files);
	}

	function formatFileSize(bytes: number): string {
		if (bytes < 1024) return bytes + ' B';
		if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
		return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
	}

	function removeFile(index: number, e: Event) {
		e.stopPropagation();
		if (!value || !multiple) {
			value = null;
			onchange?.(null);
			return;
		}
		const dt = new DataTransfer();
		for (let i = 0; i < value.length; i++) {
			if (i !== index) dt.items.add(value[i]);
		}
		const files = dt.files;
		value = files.length > 0 ? files : null;
		onchange?.(files.length > 0 ? files : null);
	}
</script>

<div
	class={cn(
		'cursor-pointer rounded-lg border-2 border-dashed p-6 text-center transition-all',
		'hover:border-primary/50 hover:bg-primary/5',
		isDragging && 'border-primary bg-primary/10',
		value && value.length > 0 && 'border-primary/30',
		className
	)}
	role="button"
	tabindex="0"
	onclick={handleClick}
	onkeydown={(e) => e.key === 'Enter' && handleClick()}
	ondragover={handleDragOver}
	ondragleave={handleDragLeave}
	ondrop={handleDrop}
>
	<input
		bind:this={inputRef}
		type="file"
		class="hidden"
		{accept}
		{multiple}
		onchange={handleInputChange}
	/>

	{#if !value || value.length === 0}
		<div class="flex flex-col items-center gap-2 text-muted-foreground">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="size-10"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				stroke-width="1.5"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"
				/>
			</svg>
			<p class="text-sm font-medium">
				{#if isDragging}
					Drop files here
				{:else}
					Click to upload or drag and drop
				{/if}
			</p>
			<p class="text-xs text-muted-foreground/70">PDF, Images, or Documents (DOC, DOCX, TXT)</p>
		</div>
	{:else}
		<div class="flex flex-col gap-2">
			{#each Array.from(value) as file, i (file.name + '-' + i)}
				<div
					class="flex items-center justify-between gap-3 rounded-md bg-muted/50 px-3 py-2 text-sm"
				>
					<span class="flex-1 truncate text-left">{file.name}</span>
					<span class="shrink-0 text-xs text-muted-foreground">
						{formatFileSize(file.size)}
					</span>
					<button
						type="button"
						class="shrink-0 text-muted-foreground transition-colors hover:text-destructive"
						aria-label="Remove file"
						onclick={(e) => removeFile(i, e)}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="size-4"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>
			{/each}
			<p class="mt-1 text-xs text-muted-foreground/70">Click or drag to replace</p>
		</div>
	{/if}
</div>
