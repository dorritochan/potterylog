import { writable } from "svelte/store";

export const showModal = writable(false);
export const editMode = writable(false);
export const glazeData = writable({});
export const glazeId = writable(null);
export const glazeList = writable([]);