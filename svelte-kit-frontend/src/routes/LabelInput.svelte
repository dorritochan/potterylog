<script>
    export let labelFor;
    export let label = '';
</script>

<div class="label-container">
    <label for={labelFor} class="p-1">{label}</label>
    <div class="invisible-container"></div>
</div>

<style>
    .label-container {
        position: relative;
    }
    .invisible-container {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: transparent; /* Making it invisible */
        z-index: 1; /* To ensure it's above the label */
    }  
</style>