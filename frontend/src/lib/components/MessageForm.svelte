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

		const messageContent = content;
		content = ''; // Clear immediately!
		submitting = true;
		try {
			await onSubmit(messageContent, chatStore.selectedUser.name);
		} finally {
			submitting = false;
		}
	}
</script>

<form onsubmit={handleSubmit} class="flex gap-2 md:gap-3 items-center p-3 md:p-4 bg-card border-t">
	<div class="h-8 w-8 md:h-10 md:w-10 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-lg md:text-xl">
		{chatStore.selectedUser.avatar}
	</div>
	<Input
		type="text"
		placeholder="OOK OOK! Type your grunt here... 🦍"
		bind:value={content}
		required
		class="flex-1 text-sm md:text-base"
	/>
	<Button type="submit" disabled={submitting} class="text-xs md:text-sm whitespace-nowrap">
		{submitting ? '🍌' : '🦍'}
		<span class="hidden sm:inline ml-1">{submitting ? 'Throwing...' : 'GRUNT!'}</span>
	</Button>
</form>
