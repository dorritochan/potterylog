<script>
    import { Button } from "sveltestrap";

    export let buttonText = '';

</script>

<Button class="standard-btn primary" type="submit" on:click>
    {@html buttonText}
</Button>


<style>
    :global(.standard-btn.primary) {
        background-color: var(--main-color);
        box-shadow: 0px 6px 10px -5px var(--main-color);
        border: none;
    }
</style>