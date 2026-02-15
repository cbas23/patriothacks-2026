<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import * as Separator from '$lib/components/ui/separator';
</script>

<div class="min-h-screen bg-background text-foreground">
	<!-- Hero Section -->
	<div class="container mx-auto max-w-6xl px-4 py-16">
		<div class="mx-auto max-w-3xl text-center">
			<Badge variant="secondary" class="mb-4">
				<svg
					class="mr-1.5 size-3.5"
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
				>
					<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
				</svg>
				Powered by AI • Fast & Accurate
			</Badge>
			<h1 class="mb-6 text-4xl font-bold sm:text-5xl md:text-6xl">
				Grade Essays with
				<span class="text-primary">Confidence</span>
			</h1>
			<p class="mb-8 text-lg text-muted-foreground sm:text-xl">
				Save time and ensure consistency with our AI-powered essay grading tool. Simply upload your
				rubric and student submissions, and get detailed, fair feedback in seconds.
			</p>
			<div class="flex flex-col justify-center gap-4 sm:flex-row">
				<Button size="lg" href="/grader"
					>Get Started
					<svg
						class="ml-2 size-5"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M19 14l-7 7m0 0l-7-7m7 7V3"
						/>
					</svg>
				</Button>
				<Button variant="outline" size="lg">Learn More</Button>
			</div>
		</div>

		<Separator.Root class="my-16" />

		<!-- Features Grid -->
		<div class="grid grid-cols-1 gap-6 md:grid-cols-3">
			<Card.Root class="border-2 border-transparent shadow-lg transition-shadow hover:shadow-xl">
				<Card.Header>
					<div class="mb-2 flex size-12 items-center justify-center rounded-lg bg-chart-1/10">
						<svg
							class="size-6 text-chart-1"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M13 10V3L4 14h7v7l9-11h-7z"
							/>
						</svg>
					</div>
					<Card.Title>Lightning Fast</Card.Title>
				</Card.Header>
				<Card.Content>
					<p class="text-muted-foreground">
						Grade hundreds of essays in minutes, not hours. Let AI handle the heavy lifting.
					</p>
				</Card.Content>
			</Card.Root>

			<Card.Root class="border-2 border-transparent shadow-lg transition-shadow hover:shadow-xl">
				<Card.Header>
					<div class="mb-2 flex size-12 items-center justify-center rounded-lg bg-chart-2/10">
						<svg
							class="size-6 text-chart-2"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
							/>
						</svg>
					</div>
					<Card.Title>Fair & Consistent</Card.Title>
				</Card.Header>
				<Card.Content>
					<p class="text-muted-foreground">
						Every essay is evaluated against your rubric with the same standards, eliminating bias.
					</p>
				</Card.Content>
			</Card.Root>

			<Card.Root class="border-2 border-transparent shadow-lg transition-shadow hover:shadow-xl">
				<Card.Header>
					<div class="mb-2 flex size-12 items-center justify-center rounded-lg bg-chart-3/10">
						<svg
							class="size-6 text-chart-3"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
							/>
						</svg>
					</div>
					<Card.Title>Detailed Feedback</Card.Title>
				</Card.Header>
				<Card.Content>
					<p class="text-muted-foreground">
						Get comprehensive comments and scores for each criterion, helping students improve.
					</p>
				</Card.Content>
			</Card.Root>
		</div>

		<Separator.Root class="my-16" />

		<!-- How It Works -->
		<div class="mb-12">
			<h2 class="mb-12 text-center text-3xl font-bold">How It Works</h2>
			<div class="grid grid-cols-1 gap-8 md:grid-cols-3">
				<div class="flex flex-col items-center text-center">
					<div
						class="mb-4 flex size-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground"
					>
						1
					</div>
					<h3 class="mb-2 text-xl font-semibold">Upload Rubric</h3>
					<p class="text-muted-foreground">
						Upload your grading criteria so the AI knows exactly what to look for.
					</p>
				</div>

				<div class="flex flex-col items-center text-center">
					<div
						class="mb-4 flex size-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground"
					>
						2
					</div>
					<h3 class="mb-2 text-xl font-semibold">Add Essays</h3>
					<p class="text-muted-foreground">
						Upload all student essays at once. Supports multiple file formats.
					</p>
				</div>

				<div class="flex flex-col items-center text-center">
					<div
						class="mb-4 flex size-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground"
					>
						3
					</div>
					<h3 class="mb-2 text-xl font-semibold">Get Results</h3>
					<p class="text-muted-foreground">
						Receive detailed grades and feedback for each student instantly.
					</p>
				</div>
			</div>
		</div>

		<Separator.Root class="my-16" />

		<!-- Trust Section -->
		<Card.Root class="border-0 bg-primary p-8 text-center text-primary-foreground md:p-12">
			<Card.Header>
				<Card.Title class="text-3xl font-bold text-primary-foreground"
					>Trusted by Educators</Card.Title
				>
				<Card.Description class="text-lg text-primary-foreground/80">
					Join thousands of teachers who have saved countless hours while providing better feedback
					to their students.
				</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="flex flex-col justify-center gap-8 sm:flex-row sm:gap-12">
					<div>
						<div class="text-4xl font-bold">10K+</div>
						<div class="text-primary-foreground/70">Essays Graded</div>
					</div>
					<div>
						<div class="text-4xl font-bold">95%</div>
						<div class="text-primary-foreground/70">Accuracy Rate</div>
					</div>
					<div>
						<div class="text-4xl font-bold">500+</div>
						<div class="text-primary-foreground/70">Happy Educators</div>
					</div>
				</div>
			</Card.Content>
		</Card.Root>
	</div>

	<!-- Footer -->
	<footer class="border-t bg-card py-8">
		<div class="container mx-auto px-4 text-center text-muted-foreground">
			<p>Built for PatriotHacks 2026 • Empowering educators with AI</p>
		</div>
	</footer>
</div>
