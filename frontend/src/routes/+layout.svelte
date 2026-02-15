<script lang="ts">
	import './layout.css';
	import { ModeWatcher } from 'mode-watcher';
	import Navbar from '$lib/components/navbar.svelte';
	let { children } = $props();
</script>

<ModeWatcher defaultMode="dark" />

<Navbar />

<div class="h-[calc(100vh-4rem)] overflow-y-scroll">
	{@render children()}
</div>

<style>
	:global(body) {
		overflow: hidden;
	}
</style>
