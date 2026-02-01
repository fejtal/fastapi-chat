<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { chatStore } from '$lib/stores/chat.svelte';
	import { Tabs, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import { Button } from '$lib/components/ui/button';

	let { onCreateRoom }: { onCreateRoom: () => void } = $props();

	// Use $state for bind:value - initialize from store
	let tabValue = $state(chatStore.activeRoomId?.toString() ?? '');
	let mounted = $state(false);
	
	onMount(() => {
		mounted = true;
	});
	
	// Sync tabValue with store's activeRoomId (one-way: store -> tab)
	$effect(() => {
		if (!mounted) return;
		const roomId = chatStore.activeRoomId;
		if (roomId !== null) {
			const newValue = roomId.toString();
			if (tabValue !== newValue) {
				tabValue = newValue;
			}
		}
	});

	// Sync store when tab changes (one-way: tab -> store)
	$effect(() => {
		if (!mounted) return;
		if (tabValue) {
			const roomId = parseInt(tabValue, 10);
			if (!isNaN(roomId) && chatStore.activeRoomId !== roomId) {
				chatStore.setActiveRoom(roomId);
			}
		}
	});
</script>

<div class="flex items-center gap-2 px-4 py-2 bg-card border-b">
	{#if mounted && browser && chatStore.rooms.length > 0}
		<Tabs bind:value={tabValue} class="flex-1">
			<TabsList class="h-9">
				{#each chatStore.rooms as room (room.id)}
					<TabsTrigger value={room.id.toString()} class="text-sm">
						{room.name}
					</TabsTrigger>
				{/each}
			</TabsList>
		</Tabs>
	{:else if chatStore.rooms.length > 0}
		<div class="flex gap-1 flex-1 overflow-x-auto">
			{#each chatStore.rooms as room (room.id)}
				<button
					onclick={() => chatStore.setActiveRoom(room.id)}
					class="px-4 py-2 rounded-md text-sm font-medium transition-colors whitespace-nowrap
						{chatStore.activeRoomId === room.id
							? 'bg-primary text-primary-foreground'
							: 'bg-muted text-muted-foreground hover:bg-muted/80'}"
				>
					{room.name}
				</button>
			{/each}
		</div>
	{:else}
		<div class="flex-1"></div>
	{/if}
	<Button variant="outline" size="sm" onclick={onCreateRoom}>
		+ New Cave
	</Button>
</div>
