<script lang="ts">
	import { Pane as ResizablePane } from 'paneforge';
	import type { ComponentProps } from 'svelte';
	import cn from 'clsx';

	type PaneProps = ComponentProps<typeof ResizablePane>;

	let { class: className, ...restProps }: PaneProps = $props();
</script>

<ResizablePane class={cn('flex flex-col', className)} {...restProps} />
