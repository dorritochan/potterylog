import { writable } from "svelte/store";

export const editMode = writable(false);
export const potData = writable({});
export const potId = writable(null);