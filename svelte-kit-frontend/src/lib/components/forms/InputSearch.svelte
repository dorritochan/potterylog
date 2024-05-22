<script>
    export let name = '';
    export let className = '';
    export let placeholder = '';
    export let value;
    export let removeErrorMessage;
    export let errorKey = '';
</script>

<input autocomplete="off" type="search"
    name={name} 
    class={className}
    placeholder={placeholder}
    bind:value={value} 
    on:input={() => {removeErrorMessage(errorKey)}} 
/>

<style>
    ::placeholder {
        opacity: 0.5;
    }
</style>