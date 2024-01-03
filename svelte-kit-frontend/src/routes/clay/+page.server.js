import { API_URL } from '$lib/config';
import { stringify } from 'querystring';

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


export const actions = {
    default: async (event) => {
        console.log('Logging the server code...');
        console.log(event);
    },
}