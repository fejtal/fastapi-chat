<script lang="ts">
	import type { Message } from '$lib/types/chat';
	import { CAVE_USERS } from '$lib/types/chat';

	let { message }: { message: Message } = $props();

	const userAvatar = $derived(
		CAVE_USERS.find((u) => u.name === message.author)?.avatar ?? '🐵'
	);
</script>

<!-- Simple card layout - no messenger-style alignment -->
<div class="w-full bg-card border rounded-lg shadow-sm hover:shadow-md transition-shadow mb-4">
	<div class="p-4">
		<!-- Header with avatar, author, timestamp -->
		<div class="flex items-center gap-3 mb-3">
			<div class="h-10 w-10 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-xl">
				{userAvatar}
			</div>
			<div class="flex-1">
				<div class="flex items-baseline gap-2">
					<span class="font-semibold text-sm text-primary">{message.author}</span>
					<span class="text-xs text-muted-foreground">{new Date(message.created_at).toLocaleTimeString()}</span>
				</div>
			</div>
		</div>
		<!-- Message content -->
		<div class="pl-[52px]">
			<p class="wrap-break-word whitespace-pre-wrap leading-relaxed text-foreground">{message.content}</p>
		</div>
	</div>
</div>
