<script>
    export let label = '';
    export let brandGroup;
    export let brandInput;
    export let brand = '';
    export let brandState;
    export let removeErrorMessage = () => {};
    export let updateFilteredBrands = () => {};
    export let handleKeydown = () => {};

    function handleInput() {
        updateFilteredBrands();
        removeErrorMessage('brand');
        removeErrorMessage('_schema');
    }


    
</script>

<div class="form-group" bind:this={brandGroup}>
    <div class="label-container">
        <label for="brand" class="p-1">{label}</label>
        <div class="invisible-container"></div>
    </div>
    <input type="search" name="brand" id="brand" class="form-control input-search" autocomplete="off" placeholder="e.g. Sibelco"
        bind:this={brandInput} 
        bind:value={brand} 
        on:input={handleInput}
        on:click={updateFilteredBrands} 
        on:focus={updateFilteredBrands} 
        on:keydown={(event) => handleKeydown(event, brandState)}
        />
    {#if filteredBrands.length > 0}
        <ul class="input-search-list list-group" transition:fly={{  y: 200, duration: 1000 }}>
            {#each filteredBrands as brandItem, index (brandItem)}
                <li  class="list-group-item {index === highlightedIndex ? 'selected' : ''}" on:click={() => selectBrand(brandItem)}>{brandItem}</li>
            {/each}
        </ul>
    {/if}
    <div class="error-message">
        <small>
            {#each errors.brand as error}
            <p in:fly={{ y: 200, duration: 2000 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
            {/each}
        </small>
    </div>
</div>

<style>

</style>