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
        color: var(--text-color);;
    }
    :global(.standard-btn.transparent):hover {
        background-color: var(--main-color);
        color: white;
        font-weight: bold;
    }

</style>