import { API_URL } from "$lib/config";

export async function load({ fetch, params }) {

    let pot_id = params.id;

    const res = await fetch(`${API_URL}/api/pot/${pot_id}`)

    if(res.ok){
        const pot = await res.json();
        return { pot }
    } else {
        return { pot: '' }
    }
}