<script lang="ts">
	import { Check } from '@lucide/svelte';

	interface Step {
		title: string;
		description?: string;
	}

	interface Props {
		steps: Step[];
		currentStep: number;
	}

	let { steps, currentStep }: Props = $props();
</script>

<div class="mb-8 flex items-center justify-center gap-1 md:gap-2">
	{#each steps as step, i (i)}
		<div class="relative flex flex-col items-center">
			<div
				class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-2 text-sm font-semibold transition-colors
				{i < currentStep
					? 'border-primary bg-primary text-primary-foreground'
					: i === currentStep
						? 'border-primary bg-primary text-primary-foreground'
						: 'border-muted-foreground text-muted-foreground'}"
			>
				{#if i < currentStep}
					<Check class="size-5" />
				{:else}
					{i + 1}
				{/if}
			</div>
			<span class="absolute top-12 text-xs font-medium md:text-sm">{step.title}</span>
		</div>
		{#if i < steps.length - 1}
			<div class="relative top-px mx-1 h-0.5 w-24 shrink-0 bg-muted-foreground/30 md:w-24"></div>
		{/if}
	{/each}
</div>
