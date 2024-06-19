<script>
    import { Button } from "sveltestrap";
    export let buttonText = '';
</script>

<div name="addButton" class="m-3 centered">
    <Button class="standard-btn transparent" on:click>
        {@html buttonText}
    </Button>
</div>


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