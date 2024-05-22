<script>
    import { fly } from "svelte/transition";
    export let name = '';
    export let placeholder = '';
    export let value = '';
    export let removeErrorMessage;
    export let errorKeys = [];
    export let updateFilteredItems;
    export let handleKeydown;
    export let state;
    export let filteredItems = [];
    export let highlightedIndex;
    export let selectItem;
    
    function handleInput() {
        updateFilteredItems();
        errorKeys.forEach(removeErrorMessage);
    }
    function handleClick() {
        updateFilteredItems();
    }
    function handleThisKeydown(event) {
        handleKeydown(event, state);
    }
</script>

<input type="search" class="form-control input-search" autocomplete="off" 
        name={name}
        placeholder={placeholder}
        bind:value
        on:input={() => handleInput()}
        on:focus={() => handleClick()} 
        on:keydown={(event) => handleThisKeydown(event)}
/>
{#if filteredItems.length > 0}
    <ul class="list-group" transition:fly={{  y: 200, duration: 1000 }}>
        {#each filteredItems as item, index (item)}
            <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
            <li  class="list-group-item {index === highlightedIndex ? 'selected' : ''}" on:click={() => selectItem(item)}>{item}</li>
        {/each}
    </ul>
{/if}

<style>
    ::placeholder {
        opacity: 0.5;
    }
    .input-search {
        position: relative;
        z-index: 2;
        box-sizing: border-box;
    }
    .list-group {
        list-style-type: none;
        z-index: 3;
        position: absolute;
        width: 100%;
        box-sizing: border-box; 
        margin: 0;
        padding: 0;
        box-shadow: 1px 6px 10px -10px #666;
    }
    .list-group-item:hover, .list-group-item.selected {
        background-color: #d0d2d7;
    }
</style>
