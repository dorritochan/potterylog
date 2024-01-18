<script>
    export let name = '';
    export let className = '';
    export let value;
</script>

<input autocomplete="off" type="search" disabled
    name={name} 
    class={className}
    bind:value={value} 
/>