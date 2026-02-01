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

<!-- Messenger-style layout: mobile 85%, desktop 50% width, aligned left/right -->
<div class="flex w-full mb-4 {isOwnMessage ? 'justify-end' : 'justify-start'}">
	<div class="max-w-[85%] md:max-w-[50%] bg-card border rounded-lg shadow-sm hover:shadow-md transition-shadow {isOwnMessage ? 'bg-primary/10' : ''}">
		<div class="p-3 md:p-4">
			<!-- Header with avatar, author, timestamp -->
			<div class="flex items-center gap-2 md:gap-3 mb-2 md:mb-3">
				<div class="h-8 w-8 md:h-10 md:w-10 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-lg md:text-xl">
					{userAvatar}
				</div>
				<div class="flex-1 min-w-0">
					<div class="flex items-baseline gap-1.5 md:gap-2">
						<span class="font-semibold text-xs md:text-sm text-primary truncate">{message.author}</span>
						<span class="text-[10px] md:text-xs text-muted-foreground whitespace-nowrap">{new Date(message.created_at).toLocaleTimeString()}</span>
					</div>
				</div>
			</div>
			<!-- Message content -->
			<div class="pl-10 md:pl-[52px]">
				<p class="wrap-break-word whitespace-pre-wrap leading-relaxed text-foreground text-sm md:text-base">{message.content}</p>
			</div>
		</div>
	</div>
</div>
