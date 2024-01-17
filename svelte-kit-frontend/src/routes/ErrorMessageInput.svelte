<script>
    export let errors;
    import { fade, fly } from 'svelte/transition';
</script>

<div class="error-message">
    <small>
        {#each errors as error}
            <p in:fly={{ y: 200, duration: 800 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
        {/each}
    </small>
</div>

<style>
    small {
        font-style: bold;
        color: var(--main-btn-color);
        min-height: 15px;
        margin: 0;
        padding-left: 3px;
    }
    .error-message small {
        display: block;
    }
</style>