<script lang="ts">
	import { PaneResizer as ResizableHandle } from 'paneforge';
	import type { ComponentProps } from 'svelte';
	import cn from 'clsx';

	type HandleProps = ComponentProps<typeof ResizableHandle>;

	let { class: className, ...restProps }: HandleProps = $props();
</script>

<ResizableHandle
	class={cn(
		'relative flex w-px items-center justify-center bg-border after:absolute after:h-5 after:w-[3px] after:rounded-full after:bg-border hover:bg-primary hover:after:bg-primary focus-visible:bg-primary focus-visible:outline-none focus-visible:after:bg-primary',
		className
	)}
	{...restProps}
>
	<div class="z-10 h-full w-1.5 bg-transparent"></div>
</ResizableHandle>
