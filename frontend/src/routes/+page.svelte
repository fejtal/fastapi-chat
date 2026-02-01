<script lang="ts">
	import { browser } from '$app/environment';
	import { MessageForm, MessageList, ModelSelector, RoomTabs, UserPicker } from '$lib/components';
	import { getMessages, createMessage, clearRoomMessages } from '$lib/api/messages';
	import { getRooms, createRoom } from '$lib/api/rooms';
	import { createWebSocketConnection } from '$lib/api/websocket';
	import { chatStore } from '$lib/stores/chat.svelte';
	import type { WebSocketMessage } from '$lib/types/chat';

	let wsConnection: { close: () => void } | null = null;
	let mounted = $state(false);
	let hasLoaded = $state(false);

	// Load rooms on mount
	async function loadRooms() {
		try {
			const rooms = await getRooms();
			chatStore.setRooms(rooms);
			if (rooms.length > 0) {
				chatStore.setActiveRoom(rooms[0].id);
			}
		} catch (e) {
			console.error('Failed to load rooms:', e);
			chatStore.setLoadingRooms(false);
		}
	}

	// Load messages for active room
	async function loadMessages(roomId: number, page: number = 1) {
		chatStore.setLoadingMessages(true);
		try {
			const data = await getMessages(roomId, page, 10);
			if (page === 1) {
				chatStore.setMessages(roomId, data.messages, data.has_more, page);
			} else {
				chatStore.appendOlderMessages(roomId, data.messages, data.has_more, page);
			}
		} catch (e) {
			console.error('Failed to load messages:', e);
			chatStore.setLoadingMessages(false);
		}
	}

	// Load more older messages
	function loadMoreMessages() {
		if (chatStore.activeRoomId && chatStore.hasMoreMessages && !chatStore.loadingMessages) {
			loadMessages(chatStore.activeRoomId, chatStore.currentPage + 1);
		}
	}

	// Handle WebSocket messages
	function handleWsMessage(wsMessage: WebSocketMessage) {
		if (wsMessage.type === 'new_message') {
			chatStore.addMessage(wsMessage.message.room_id, wsMessage.message);
			
			// Stop loading only if this is an AI model response (not a caveman user)
			const cavemanNames = ['Grok', 'Ooga', 'Booga', 'Ugga', 'Mugga'];
			const isUserMessage = cavemanNames.includes(wsMessage.message.author);
			const isAiResponse = !isUserMessage; // AI responses have model names like "gemma3:4b"
			
			if (isAiResponse && chatStore.aiGenerating) {
				chatStore.setAiGenerating(false);
			}
		}
	}

	// Connect WebSocket when room changes (only after mount)
	$effect(() => {
		if (!mounted) return;
		
		const roomId = chatStore.activeRoomId;
		if (!roomId) return;

		// Close existing connection
		if (wsConnection) {
			wsConnection.close();
			wsConnection = null;
		}

		// Connect to new room
		wsConnection = createWebSocketConnection(roomId, handleWsMessage);
		
		// Load messages for new room
		loadMessages(roomId);

		// Cleanup function - close WebSocket when effect re-runs or component unmounts
		return () => {
			wsConnection?.close();
			wsConnection = null;
		};
	});

	// Initial load - only run in browser
	$effect(() => {
		if (!browser) return;
		if (hasLoaded) return;
		hasLoaded = true;
		mounted = true;
		loadRooms();
	});

	// Check if current room is AI room
	const isAiRoom = $derived(
		chatStore.activeRoom?.name.includes('AI Cave') || 
		chatStore.activeRoom?.name.includes('🤖') || 
		false
	);

	// Handle message submit
	async function handleSubmit(content: string, author: string) {
		if (!chatStore.activeRoomId) return;
		// If in AI room, include selected model
		const model = isAiRoom ? (chatStore.selectedModel || undefined) : undefined;
		
		// Set AI generating state if model is selected
		if (isAiRoom && model) {
			chatStore.setAiGenerating(true);
		}
		
		await createMessage(chatStore.activeRoomId, content, author, model);
		// Message will arrive via WebSocket, no need to manually add
	}

	// Handle create room
	async function handleCreateRoom() {
		const name = prompt('Enter cave name:');
		if (!name?.trim()) return;

		try {
			const room = await createRoom(name.trim());
			chatStore.addRoom(room);
			chatStore.setActiveRoom(room.id);
		} catch (e) {
			console.error('Failed to create room:', e);
			alert('Failed to create cave. Maybe name already exists?');
		}
	}

	// Handle clear chat
	async function handleClearChat() {
		if (!chatStore.activeRoomId) return;
		
		const confirmed = confirm('OOK! Delete ALL messages in cave? No undo! 🗑️');
		if (!confirmed) return;

		try {
			const result = await clearRoomMessages(chatStore.activeRoomId);
			// Clear messages from store
			chatStore.setMessages(chatStore.activeRoomId, [], false, 1);
			alert(result.message);
		} catch (e) {
			console.error('Failed to clear chat:', e);
			alert('Monkey failed to clear cave! Try again! 😢');
		}
	}
</script>

<svelte:head>
	<title>Cave Chat 🍌</title>
</svelte:head>

<main class="h-screen flex flex-col bg-muted/40">
	<!-- Header -->
	<header class="bg-card border-b px-6 py-4">
		<div class="max-w-4xl mx-auto flex items-center justify-between gap-4">
			<h1 class="text-2xl font-bold">🍌 Cave Chat</h1>
			<div class="flex items-center gap-3">
				{#if chatStore.activeRoomId}
					<button
						onclick={handleClearChat}
						class="px-3 py-1.5 text-sm bg-red-500/10 hover:bg-red-500/20 text-red-600 dark:text-red-400 rounded-lg border border-red-500/20 transition-colors"
						title="Clear all messages in this cave"
					>
						🗑️ Clear Cave
					</button>
				{/if}
				<UserPicker />
			</div>
		</div>
	</header>

	<!-- Room Tabs -->
	<div class="max-w-4xl mx-auto w-full">
		<RoomTabs onCreateRoom={handleCreateRoom} />
		{#if isAiRoom}
			<div class="px-4 py-3 bg-card border-b">
				<ModelSelector />
			</div>
		{/if}
	</div>

	<!-- Chat Area -->
	<div class="flex-1 max-w-4xl mx-auto w-full flex flex-col overflow-hidden">
		{#if chatStore.loadingRooms}
			<div class="flex-1 flex items-center justify-center">
				<p class="text-muted-foreground">OOK! Searching for caves... 🍌🦍</p>
			</div>
		{:else if !chatStore.activeRoom}
			<div class="flex-1 flex items-center justify-center">
				<p class="text-muted-foreground">No cave! Monkey need cave! Make new cave! 🏔️</p>
			</div>
		{:else}
			{@const msgs = chatStore.activeMessages}
			<MessageList
				messages={msgs}
				loading={chatStore.loadingMessages}
				hasMore={chatStore.hasMoreMessages}
				onLoadMore={loadMoreMessages}
			/>
			{#if isAiRoom && !chatStore.selectedModel}
				<div class="px-4 py-2 bg-yellow-500/10 border-t border-yellow-500/20 text-yellow-700 dark:text-yellow-400 text-sm text-center">
					⚠️ Pick monkey brain first! AI need brain to talk! 🧠
				</div>
			{/if}
			<MessageForm onSubmit={handleSubmit} />
		{/if}
	</div>
</main>
