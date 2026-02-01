import { WS_URL } from '$lib/config';
import type { WebSocketMessage } from '$lib/types/chat';

export type WebSocketHandler = (message: WebSocketMessage) => void;

export function createWebSocketConnection(
	roomId: number,
	onMessage: WebSocketHandler
): { close: () => void } {
	const ws = new WebSocket(`${WS_URL}/api/ws/room/${roomId}`);

	ws.onmessage = (event) => {
		try {
			const data = JSON.parse(event.data) as WebSocketMessage;
			onMessage(data);
		} catch (error) {
			console.error('Failed to parse WebSocket message:', error);
		}
	};

	ws.onerror = (error) => {
		console.error('WebSocket error:', error);
	};

	return {
		close: () => ws.close()
	};
}
