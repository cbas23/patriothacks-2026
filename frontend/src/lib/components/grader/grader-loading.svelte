<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import * as Skeleton from '$lib/components/ui/skeleton';

	const studentSkeletons = [1, 2, 3, 4, 5];
	const criteriaSkeletons = [1, 2, 3, 4];
</script>

<Resizable.PaneGroup direction="horizontal" class="h-[calc(100vh-4rem)]">
	<Resizable.Pane defaultSize={20} minSize={15} maxSize={35}>
		<div class="flex h-full flex-col gap-2 overflow-y-auto border-r p-4">
			<h2 class="text-lg font-semibold">Students</h2>
			<!-- eslint-disable-next-line @typescript-eslint/no-unused-vars -->
			{#each studentSkeletons as _, i (i)}
				<div
					class="flex h-auto flex-col items-start justify-start gap-1 rounded-md border bg-background px-3 py-2"
				>
					<Skeleton.Root class="h-4 w-24 bg-muted" />
					<Skeleton.Root class="h-3 w-16 bg-muted" />
				</div>
			{/each}
		</div>
	</Resizable.Pane>

	<Resizable.Handle />

	<Resizable.Pane defaultSize={50} minSize={30}>
		<div class="flex h-full flex-col overflow-y-auto border-r p-4">
			<h2 class="mb-4 text-lg font-semibold">Submitted Items</h2>
			<Skeleton.Root class="h-64 w-full rounded-lg bg-muted" />
			<Skeleton.Root class="mt-4 h-64 w-full rounded-lg bg-muted" />
			<Skeleton.Root class="mt-4 h-64 w-full rounded-lg bg-muted" />
		</div>
	</Resizable.Pane>

	<Resizable.Handle />

	<Resizable.Pane defaultSize={30} minSize={20} maxSize={50}>
		<div class="flex h-full flex-col overflow-y-auto">
			<h2 class="m-4 mb-4 text-lg font-semibold">Grade Details</h2>
			<div class="flex flex-col gap-2 px-4">
				<!-- eslint-disable-next-line @typescript-eslint/no-unused-vars -->
				{#each criteriaSkeletons as _, i (i)}
					<div class="rounded-md border p-3">
						<div class="flex items-center gap-2">
							<Skeleton.Root class="size-5 rounded-sm bg-muted" />
							<Skeleton.Root class="h-4 flex-1 bg-muted" />
							<Skeleton.Root class="h-3 w-12 bg-muted" />
						</div>
					</div>
				{/each}
			</div>
		</div>
	</Resizable.Pane>
</Resizable.PaneGroup>
