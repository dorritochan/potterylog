import { API_URL } from '$lib/config';

export async function load({ fetch, params }) {

    let clay_id = params.id;

    // Fetch the clay in json format
    const res = await fetch(`${API_URL}/api/clay/${clay_id}`);
    
    if (res.ok) {
        const clay = await res.json();
        return { clay };
    } else {
        // Handle error
        return { clay: '' }; // or return an error message
    }
}