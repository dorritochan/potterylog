<script>
    import { Button } from "sveltestrap";
    export let buttonText = '';
    export let handleOnClick;
</script>

<Button class="standard-btn transparent" on:click={handleOnClick}>
    {@html buttonText}
</Button>


<style>
    :global(.standard-btn.transparent) {
        background-color: transparent;
        -webkit-backdrop-filter: blur(10px);
        backdrop-filter: blur(10px);
        border: 1px var(--main-color) solid;
        color: white;
        text-shadow: 1px 1px 2px var(--main-color);
    }
    :global(.standard-btn.transparent):hover {
        background-color: var(--main-color);
    }
    :global(.standard-btn.transparent):focus {
        border: none;
    }
</style>