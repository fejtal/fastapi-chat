import { API_URL } from '$lib/config';

export async function getModels(): Promise<string[]> {
	const res = await fetch(`${API_URL}/api/ollama/models`);
	if (!res.ok) throw new Error('Failed to fetch Ollama models');
	const data = await res.json();
	return data.models || [];
}
