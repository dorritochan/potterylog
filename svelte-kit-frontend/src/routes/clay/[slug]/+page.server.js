import { API_URL } from '$lib/config';
import { error } from '@sveltejs/kit';

export async function load({ fetch, params }) {

    let clay_id = params.slug;

    // Fetch the clay in json format
    const response = await fetch(`${API_URL}/api/clay/${clay_id}`);
    
    if (!response.ok) {
        const errorBody = await response.json();
        console.log(`errorBody.message: ${errorBody.message}`);

        if (response.status == 404) {
            throw error(404, {
                message: errorBody.message
            });
        } else {
            console.log('An error occurred:', response.statusText);
            throw error(response.status, {
                message: response.statusText
            });
        }
    }

    const clay = await response.json();
    return { clay };
}