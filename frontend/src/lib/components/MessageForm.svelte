<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';

	let { onSubmit }: { onSubmit: (content: string, author: string) => Promise<void> } = $props();

	let content = $state('');
	let submitting = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		if (!content.trim() || submitting) return;

		submitting = true;
		try {
			await onSubmit(content, chatStore.selectedUser.name);
			content = '';
		} finally {
			submitting = false;
		}
	}
</script>

<form onsubmit={handleSubmit} class="flex gap-3 items-center p-4 bg-card border-t">
	<div class="h-10 w-10 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-xl">
		{chatStore.selectedUser.avatar}
	</div>
	<Input
		type="text"
		placeholder="OOK OOK! Type your grunt here... 🦍"
		bind:value={content}
		required
		class="flex-1"
	/>
	<Button type="submit" disabled={submitting}>
		{submitting ? 'Throwing banana... 🍌' : 'GRUNT! 🦍'}
	</Button>
</form>
