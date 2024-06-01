import { API_URL } from "$lib/config";
import { error } from '@sveltejs/kit';

export async function load({ fetch }) {
    const response = await fetch(`${API_URL}/api/links`);

    if (!response.ok) {
        const errorBody = await response.json();
        console.log(`errorBody.message: ${errorBody.message}`);

        throw error(response.status, {
            message: errorBody.message
        })
    }

    const links = await response.json();
    console.log('links:');
    console.log(links);
    return { linkList: links };
}