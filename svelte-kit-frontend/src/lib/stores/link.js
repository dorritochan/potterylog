import { writable } from "svelte/store";

export const showModal = writable(false);
export const editMode = writable(false);
export const linkData = writable({});
export const linkId = writable(null);
export const linkList = writable([]);