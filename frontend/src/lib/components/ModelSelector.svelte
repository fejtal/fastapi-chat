<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { getModels } from '$lib/api/ollama';
	import { Badge } from '$lib/components/ui/badge';

	let models = $state<string[]>([]);
	let loading = $state(false);
	let error = $state<string | null>(null);

	async function loadModels() {
		loading = true;
		error = null;
		try {
			models = await getModels();
			if (models.length === 0) {
				error = 'OOK! No monkey brains found! Wake up Ollama! 🦍';
			} else if (!chatStore.selectedModel && models.length > 0) {
				// Auto-select first model if none selected
				chatStore.setSelectedModel(models[0]);
			}
		} catch (e) {
			error = 'Failed to load models (Ollama monkey sleeping?)';
			console.error('Failed to load Ollama models:', e);
		} finally {
			loading = false;
		}
	}

	// Load models on mount (always try to load)
	$effect(() => {
		if (models.length === 0 && !loading && !error) {
			loadModels();
		}
	});
</script>

<div class="flex items-center gap-3">
		<span class="text-sm text-muted-foreground">Model:</span>
		{#if loading}
			<span class="text-sm text-muted-foreground">Finding monkey brains... 🧠</span>
		{:else if error}
			<span class="text-sm text-destructive">{error}</span>
		{:else if models.length > 0}
			{@const currentModel = chatStore.selectedModel}
			<select
				value={currentModel || ''}
				onchange={(e) => {
					const target = e.currentTarget;
					chatStore.setSelectedModel(target.value || null);
				}}
				class="h-9 rounded-md border border-input bg-background px-3 py-1 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
			>
				<option value="">Pick monkey brain... 🧠</option>
				{#each models as model}
					<option value={model}>{model}</option>
				{/each}
			</select>
			{#if chatStore.selectedModel}
				<Badge variant="secondary">{chatStore.selectedModel}</Badge>
			{/if}
		{:else}
			<span class="text-sm text-muted-foreground">No monkey brains in cave! 🏜️</span>
		{/if}
</div>
