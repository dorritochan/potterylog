import { API_URL } from "$lib/config";

export async function load({ fetch }) {
    const response = await fetch(`${API_URL}/api/glazes`);

    if (!response.ok) {
        console.error('Failed to fetch');
        // Handle error appropriately
        return { props: { error: 'Failed to fetch data' } };
    }

    const glazes = await response.json();
    return { glazes };
}