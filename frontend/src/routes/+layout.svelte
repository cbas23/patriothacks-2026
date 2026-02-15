<script lang="ts">
	import './layout.css';
	import { ModeWatcher } from 'mode-watcher';
	import Navbar from '$lib/components/navbar.svelte';
	import { page } from '$app/stores';
	let { children } = $props();

	const isGradingPage = $derived($page.url.pathname.startsWith('/grader'));
</script>

<ModeWatcher defaultMode="light" />

<svelte:head>
	<script src="https://tweakcn.com/live-preview.min.js"></script>
</svelte:head>

<Navbar />

{#if isGradingPage}
	<div class="h-[calc(100vh-4rem)]">
		{@render children()}
	</div>
{:else}
	{@render children()}
{/if}
