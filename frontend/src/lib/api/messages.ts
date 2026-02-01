import type { Message, PaginatedMessages } from '$lib/types/chat';
import { API_URL } from '$lib/config';

export async function getMessages(
	roomId: number,
	page: number = 1,
	pageSize: number = 10
): Promise<PaginatedMessages> {
	const response = await fetch(
		`${API_URL}/api/messages/room/${roomId}?page=${page}&page_size=${pageSize}`
	);
	if (!response.ok) throw new Error('Failed to fetch messages');
	return response.json();
}

export async function createMessage(
	roomId: number,
	content: string,
	author: string,
	model?: string
): Promise<Message> {
	const body: { room_id: number; content: string; author: string; model?: string } = {
		room_id: roomId,
		content,
		author
	};
	
	if (model) {
		body.model = model;
	}

	const response = await fetch(`${API_URL}/api/messages`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(body)
	});
	if (!response.ok) throw new Error('Failed to create message');
	return response.json();
}

export async function clearRoomMessages(roomId: number): Promise<{ deleted: number; message: string }> {
	const response = await fetch(`${API_URL}/api/messages/room/${roomId}`, {
		method: 'DELETE'
	});
	if (!response.ok) throw new Error('Failed to clear messages');
	return response.json();
}
