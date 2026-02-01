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
let aiGenerating = $state(false);

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
	get aiGenerating() {
		return aiGenerating;
	},

	// Setters
	setActiveRoom(roomId: number) {
		activeRoomId = roomId;
	},

	setRooms(newRooms: Room[]) {
		rooms = newRooms;
		loadingRooms = false;
	},

	setLoadingRooms(loading: boolean) {
		loadingRooms = loading;
	},

	addRoom(room: Room) {
		rooms = [...rooms, room];
	},

	setMessages(roomId: number, messages: Message[], hasMore: boolean, page: number) {
		// Reassign to trigger reactivity
		messagesByRoom = { ...messagesByRoom, [roomId]: messages };
		hasMoreByRoom = { ...hasMoreByRoom, [roomId]: hasMore };
		currentPageByRoom = { ...currentPageByRoom, [roomId]: page };
		loadingMessages = false;
	},

	appendOlderMessages(roomId: number, messages: Message[], hasMore: boolean, page: number) {
		const existing = messagesByRoom[roomId] ?? [];
		// Reassign to trigger reactivity
		messagesByRoom = { ...messagesByRoom, [roomId]: [...existing, ...messages] };
		hasMoreByRoom = { ...hasMoreByRoom, [roomId]: hasMore };
		currentPageByRoom = { ...currentPageByRoom, [roomId]: page };
		loadingMessages = false;
	},

	addMessage(roomId: number, message: Message) {
		const existing = messagesByRoom[roomId] ?? [];
		// IMPORTANT: Reassign the entire object to trigger Svelte 5 reactivity!
		messagesByRoom = {
			...messagesByRoom,
			[roomId]: [message, ...existing]
		};
	},

	setLoadingMessages(loading: boolean) {
		loadingMessages = loading;
	},

	setSelectedUser(user: CaveUser) {
		selectedUser = user;
	},

	setSelectedModel(model: string | null) {
		selectedModel = model;
	},

	setAiGenerating(generating: boolean) {
		aiGenerating = generating;
	}
};
