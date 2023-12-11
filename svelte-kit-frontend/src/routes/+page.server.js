import { API_URL } from '$lib/config';

export async function load({ fetch }) {
    // Fetch the list of pots in json format
    const res = await fetch(`${API_URL}/api/pots`);
    
    if (res.ok) {
        const pots = await res.json();
        console.log(pots);
        return { pots };
    } else {
        // Handle error
        return { pots: [] }; // or return an error message
    }
}
