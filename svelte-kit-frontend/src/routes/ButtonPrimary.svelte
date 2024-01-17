<script>
    import { Button } from "sveltestrap";
    export let buttonText = '';
</script>

<Button class="standard-btn primary" type="submit">
    {@html buttonText}
</Button>


<style>
    :global(.standard-btn.primary) {
        background-color: var(--main-color-pink);
        box-shadow: 0px 6px 10px -5px var(--main-color-pink);
        border: none;
    }
    :global(.standard-btn.primary):hover {
        background-color: var(--accent-color-yellow);
        box-shadow: 0px 6px 10px -5px var(--accent-color-yellow);
        color: var(--main-color-pink);
    }
</style>