export type Room = {
	id: number;
	name: string;
	created_at: string;
};

export type Message = {
	id: number;
	content: string;
	author: string;
	room_id: number;
	created_at: string;
};

export type PaginatedMessages = {
	messages: Message[];
	total: number;
	page: number;
	page_size: number;
	has_more: boolean;
};

export type WebSocketMessage = {
	type: 'new_message';
	message: Message;
};

export type CaveUser = {
	id: string;
	name: string;
	avatar: string;
};

export const CAVE_USERS: CaveUser[] = [
	{ id: 'grok', name: 'Grok', avatar: '🦍' },
	{ id: 'ooga', name: 'Ooga', avatar: '🐒' },
	{ id: 'booga', name: 'Booga', avatar: '🦧' },
	{ id: 'ugga', name: 'Ugga', avatar: '🙈' },
	{ id: 'mugga', name: 'Mugga', avatar: '🙉' }
];
