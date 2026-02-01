import { API_URL } from '$lib/config';
import type { Room } from '$lib/types/chat';

export async function getRooms(): Promise<Room[]> {
	const res = await fetch(`${API_URL}/api/rooms`);
	if (!res.ok) throw new Error('Failed to fetch rooms');
	return res.json();
}

export async function createRoom(name: string): Promise<Room> {
	const res = await fetch(`${API_URL}/api/rooms`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name })
	});
	if (!res.ok) throw new Error('Failed to create room');
	return res.json();
}

export async function deleteRoom(roomId: number): Promise<void> {
	const res = await fetch(`${API_URL}/api/rooms/${roomId}`, {
		method: 'DELETE'
	});
	if (!res.ok) throw new Error('Failed to delete room');
}
