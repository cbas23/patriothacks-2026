<script lang="ts">
	import { PaneGroup as ResizablePaneGroup } from 'paneforge';
	import type { ComponentProps } from 'svelte';
	import cn from 'clsx';

	type PaneGroupProps = ComponentProps<typeof ResizablePaneGroup>;

	let { class: className, ...restProps }: PaneGroupProps = $props();
</script>

<ResizablePaneGroup class={cn('flex h-full w-full', className)} {...restProps} />
