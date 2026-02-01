import type { Room, Message, CaveUser } from '$lib/types/chat';
import { CAVE_USERS } from '$lib/types/chat';

// Module-level $state variables (not exported - accessed via getters)
let rooms = $state<Room[]>([]);
let activeRoomId = $state<number | null>(null);
let messagesByRoom = $state<Record<number, Message[]>>({});
let loadingRooms = $state(true);
let loadingMessages = $state(false);
let hasMoreByRoom = $state<Record<number, boolean>>({});
let currentPageByRoom = $state<Record<number, number>>({});
let selectedUser = $state<CaveUser>(CAVE_USERS[0]);
let selectedModel = $state<string | null>(null);

// Derived values
const activeRoom = $derived(rooms.find((r) => r.id === activeRoomId));
const activeMessages = $derived(messagesByRoom[activeRoomId ?? -1] ?? []);
const hasMoreMessages = $derived(hasMoreByRoom[activeRoomId ?? -1] ?? true);
const currentPage = $derived(currentPageByRoom[activeRoomId ?? -1] ?? 1);

// Export store object with getters and setters
export const chatStore = {
	// Getters (reactive when accessed)
	get rooms() {
		return rooms;
	},
	get activeRoomId() {
		return activeRoomId;
	},
	get activeRoom() {
		return activeRoom;
	},
	get activeMessages() {
		return activeMessages;
	},
	get loadingRooms() {
		return loadingRooms;
	},
	get loadingMessages() {
		return loadingMessages;
	},
	get hasMoreMessages() {
		return hasMoreMessages;
	},
	get currentPage() {
		return currentPage;
	},
	get selectedUser() {
		return selectedUser;
	},
	get selectedModel() {
		return selectedModel;
	},

	// Setters
	setActiveRoom(roomId: number) {
		activeRoomId = roomId;
	},

	setRooms(newRooms: Room[]) {
		console.log('[DEBUG] setRooms called with:', newRooms.length, 'rooms');
		console.log('[DEBUG] loadingRooms BEFORE:', loadingRooms);
		rooms = newRooms;
		loadingRooms = false;
		console.log('[DEBUG] loadingRooms AFTER:', loadingRooms);
	},

	setLoadingRooms(loading: boolean) {
		loadingRooms = loading;
	},

	addRoom(room: Room) {
		rooms = [...rooms, room];
	},

	setMessages(roomId: number, messages: Message[], hasMore: boolean, page: number) {
		messagesByRoom[roomId] = messages;
		hasMoreByRoom[roomId] = hasMore;
		currentPageByRoom[roomId] = page;
		loadingMessages = false;
	},

	appendOlderMessages(roomId: number, messages: Message[], hasMore: boolean, page: number) {
		const existing = messagesByRoom[roomId] ?? [];
		messagesByRoom[roomId] = [...existing, ...messages];
		hasMoreByRoom[roomId] = hasMore;
		currentPageByRoom[roomId] = page;
		loadingMessages = false;
	},

	addMessage(roomId: number, message: Message) {
		console.log('[STORE] addMessage called - roomId:', roomId, 'message:', message);
		const existing = messagesByRoom[roomId] ?? [];
		console.log('[STORE] Existing messages count:', existing.length);
		messagesByRoom[roomId] = [message, ...existing];
		console.log('[STORE] New messages count:', messagesByRoom[roomId].length);
		console.log('[STORE] messagesByRoom after add:', messagesByRoom);
	},

	setLoadingMessages(loading: boolean) {
		loadingMessages = loading;
	},

	setSelectedUser(user: CaveUser) {
		selectedUser = user;
	},

	setSelectedModel(model: string | null) {
		selectedModel = model;
	}
};
