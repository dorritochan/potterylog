import { API_URL } from "$lib/config";
import { error } from '@sveltejs/kit';

export async function load({ fetch }) {
    const response = await fetch(`${API_URL}/api/glazes`);

    if (!response.ok) {
        const errorBody = await response.json();
        console.log(`errorBody.message: ${errorBody.message}`);

        throw error(response.status, {
            message: errorBody.message
        })
    }

    const glazes = await response.json();
    console.log('glazes:');
    console.log(glazes);
    return { glazeList: glazes };
}
