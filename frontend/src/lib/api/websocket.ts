import { WS_URL } from '$lib/config';
import type { WebSocketMessage } from '$lib/types/chat';

export type WebSocketHandler = (message: WebSocketMessage) => void;

export function createWebSocketConnection(
	roomId: number,
	onMessage: WebSocketHandler
): { close: () => void } {
	const ws = new WebSocket(`${WS_URL}/api/ws/room/${roomId}`);

	ws.onopen = () => {
		console.log(`WebSocket connected to room ${roomId}`);
	};

	ws.onmessage = (event) => {
		try {
			console.log('[WebSocket] Raw message received:', event.data);
			const data = JSON.parse(event.data) as WebSocketMessage;
			console.log('[WebSocket] Parsed message:', data);
			onMessage(data);
		} catch (error) {
			console.error('Failed to parse WebSocket message:', error);
		}
	};

	ws.onerror = (error) => {
		console.error('WebSocket error:', error);
	};

	ws.onclose = () => {
		console.log(`WebSocket disconnected from room ${roomId}`);
	};

	return {
		close: () => ws.close()
	};
}
