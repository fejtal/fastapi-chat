<script lang="ts">
	import type { Message } from '$lib/types/chat';
	import { CAVE_USERS } from '$lib/types/chat';
	import { chatStore } from '$lib/stores/chat.svelte';

	let { message }: { message: Message } = $props();

	const userAvatar = $derived(
		CAVE_USERS.find((u) => u.name === message.author)?.avatar ?? '🐵'
	);

	const isOwnMessage = $derived(message.author === chatStore.selectedUser.name);
</script>

<div class="flex gap-3 max-w-[80%] {isOwnMessage ? 'ml-auto flex-row-reverse' : 'mr-auto'}">
	<div class="h-10 w-10 shrink-0 rounded-full flex items-center justify-center text-xl {isOwnMessage ? 'bg-primary/20' : 'bg-muted'}">
		{userAvatar}
	</div>
	<div class="flex-1 rounded-xl shadow-sm {isOwnMessage ? 'bg-primary text-primary-foreground' : 'bg-card border'}">
		<div class="p-3">
			<div class="flex items-baseline gap-2 mb-1 {isOwnMessage ? 'flex-row-reverse' : ''}">
				<span class="font-semibold text-sm {isOwnMessage ? '' : 'text-primary'}">{message.author}</span>
				<span class="text-xs {isOwnMessage ? 'text-primary-foreground/70' : 'text-muted-foreground'}">{new Date(message.created_at).toLocaleTimeString()}</span>
			</div>
			<p class="break-words whitespace-pre-wrap leading-relaxed">{message.content}</p>
		</div>
	</div>
</div>
