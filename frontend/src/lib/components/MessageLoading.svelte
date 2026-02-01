<script lang="ts">
	const jungleTexts = [
		'OOK! Thinking... 🦍',
		'Finding bananas... 🍌',
		'Climbing trees... 🌴',
		'Swinging vines... 🌿',
		'Eating coconuts... 🥥',
		'Scratching head... 🤔',
		'Gathering leaves... 🍃',
		'Munching fruit... 🥭',
		'Beating chest... 💪',
		'Hunting grubs... 🐛'
	];

	let currentText = $state(jungleTexts[0]);

	// Use $effect with cleanup instead of onMount/onDestroy
	$effect(() => {
		const intervalId = window.setInterval(() => {
			const randomIndex = Math.floor(Math.random() * jungleTexts.length);
			currentText = jungleTexts[randomIndex];
		}, 1000);

		// Cleanup function - automatically called when component unmounts
		return () => {
			clearInterval(intervalId);
		};
	});
</script>

<!-- Simple single-line loader -->
<div class="flex w-full mb-4 justify-start px-2 md:px-0">
	<div class="text-muted-foreground italic text-xs md:text-sm animate-pulse">
		{currentText}
	</div>
</div>
