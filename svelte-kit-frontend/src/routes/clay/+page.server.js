import { API_URL } from '$lib/config';
import { error } from '@sveltejs/kit';

export async function load({ fetch }) {

    const response = await fetch(`${API_URL}/api/clays`);
    if (!response.ok) {
        const errorBody = await response.json();
        console.log(`errorBody.message: ${errorBody.message}`);

        throw error(response.status, {
            message: errorBody.message
        })
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