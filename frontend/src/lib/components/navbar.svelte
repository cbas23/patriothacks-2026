<script lang="ts">
	import { page } from '$app/stores';
	import { resolve } from '$app/paths';

	function isActive(href: string): string {
		return $page.url.pathname === href ? 'text-foreground' : 'text-foreground/60';
	}
</script>

<nav class="border-b border-border bg-background">
	<div class="container mx-auto flex h-16 items-center justify-between gap-6 px-4">
		<span class="text-lg font-semibold">Swift Grader</span>
		<div class="flex gap-6">
			<a
				href={resolve('/')}
				class="text-sm font-medium transition-colors hover:text-foreground/80 {isActive(
					resolve('/')
				)}"
				data-sveltekit-preload-data="tap"
			>
				Home
			</a>
			<a
				href={resolve('/grader')}
				class="text-sm font-medium transition-colors hover:text-foreground/80 {isActive(
					resolve('/grader')
				)}"
				data-sveltekit-preload-data="tap"
			>
				Grading
			</a>
		</div>
	</div>
</nav>
