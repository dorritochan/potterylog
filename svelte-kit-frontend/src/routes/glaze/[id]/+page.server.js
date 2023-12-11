import { API_URL } from '$lib/config.js';

export async function load({ fetch, params }){

    let glaze_id = params.id;
    const response = await fetch(`${API_URL}/api/glaze/${glaze_id}`);

    if (response.ok) {
        const glaze = await response.json();
        return { glaze };
    } else {
        console.error('Failed to fetch');
        return { props: { error: 'Failed to fetch data' } };
    }
}