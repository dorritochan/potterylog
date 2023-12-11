import { API_URL } from '$lib/config';

export async function load({ fetch }) {

    const response = await fetch(`${API_URL}/api/clays`);
    if (!response.ok) {
        console.error('Failed to fetch');
        // Handle error appropriately
        return { props: { error: 'Failed to fetch data' } };
    }

    const clays = await response.json();
    return { clays };
}