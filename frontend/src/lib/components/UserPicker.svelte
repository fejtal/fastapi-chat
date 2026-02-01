<script lang="ts">
	import { chatStore } from '$lib/stores/chat.svelte';
	import { CAVE_USERS } from '$lib/types/chat';
	import { Badge } from '$lib/components/ui/badge';
</script>

<div class="flex items-center gap-3">
	<span class="text-sm text-muted-foreground">Speak as:</span>
	<div class="flex gap-1">
		{#each CAVE_USERS as user (user.id)}
			<button
				onclick={() => chatStore.setSelectedUser(user)}
				class="h-9 w-9 rounded-full bg-muted flex items-center justify-center text-lg transition-all
					{chatStore.selectedUser.id === user.id ? 'scale-110 ring-2 ring-primary' : 'opacity-60 hover:opacity-100'}"
				title={user.name}
			>
				{user.avatar}
			</button>
		{/each}
	</div>
	<Badge variant="secondary">{chatStore.selectedUser.name}</Badge>
</div>
