<script>
    export let name = '';
    export let className = '';
    export let placeholder = '';
    export let value;
    export let removeErrorMessage;
    export let errorKey = '';
    export let addOn = '';
</script>

<div class="input-group">
    <input autocomplete="off" type="number"
    name={name} 
    class={className}
    placeholder={placeholder}
    bind:value={value} 
    on:input={() => {removeErrorMessage(errorKey)}} 
    />
    <div class="input-group-append">
        <span class="input-group-text" id="basic-addon1">{addOn}</span>
    </div>
</div>

<style>
    ::placeholder {
        opacity: 0.5;
    }
</style>