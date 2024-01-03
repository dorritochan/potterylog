<script>
    import { API_URL } from '$lib/config';
    import Modal from '../Modal.svelte';
    import { onDestroy, onMount } from 'svelte';

	export let data;
    
    let showModal = false;

    let clayBrandList = [];
    let filteredBrands = [];
    let highlightedIndex = -1; // Index of the currently highlighted element in the list
    let brand = '';
    
    onMount(async () => {
        const response = await fetch(`${API_URL}/api/clay_brands`);
        if (response.ok) {
            clayBrandList = await response.json();
        }
    });
    

    let brandInput;
    function handleClickOutsideBrandInput(event) {
        if (!brandInput.contains(event.target)) {
            closeBrandList();
        }
    }

    function updateFilteredBrands() {
        filteredBrands = clayBrandList.filter(brandFromList => brandFromList.toLowerCase().includes(brand.toLowerCase()));
    }

    function selectBrand(brandItem) {
        brand = brandItem;
        closeBrandList();
    }

    function closeBrandList() {
        filteredBrands = [];
        highlightedIndex = -1;
    }

    function handleKeydown(event) {
        switch(event.key) {
            case 'ArrowDown':
                highlightedIndex = (highlightedIndex + 1) % filteredBrands.length;
                break;
            case 'ArrowUp':
                highlightedIndex = (highlightedIndex - 1 + filteredBrands.length) % filteredBrands.length;
                break;
            case 'Enter':
                if (highlightedIndex >= 0) {
                    selectBrand(filteredBrands[highlightedIndex]);
                }
                break;
            case 'Tab':
                closeBrandList();
                break;
        }
    }

    let name_id = '';
    let color = '';
    let temp_min = '';
    let temp_max = '';
    let grog_percent = '';
    let grog_size_max = '';
    let url = '';
    let errors = { brand: [], name_id: [], color: [], temp_min: [], temp_max: [], grog_percent: [], grog_size_max: [], url: [] };

    async function handleSubmit() {
        const response = await fetch(`${API_URL}/api/add_clay`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                brand, name_id,color, temp_min, temp_max, grog_percent, grog_size_max, url 
            })
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result.message);
        } else {
            console.log(response.errors);

            // Client-side errors (e.g., 400 Bad Request)
            if (response.status >= 400 && response.status < 500) {
                console.error("Client error:", response.status);
                const errorData = await response.json();
                // Show error message to the user
                console.error(errorData.errors);
                // Server-side errors (e.g., 500 Internal Server Error)
            } else if (response.status >= 500) {
                // Show generic error message to the user
                console.error("Server error:", response.status);
            }
        }
    }

</script>

<svelte:head>
    <title>List of clays</title>
</svelte:head>


<h1 class="m-3">List of clays</h1>

<div class="m-3">
    <button on:click={() => showModal = true} id="add-new-clay" type="button" class="btn btn-primary">&plus; Add a new clay</button>
</div>

<Modal bind:showModal modalTitle="Add a new clay" submitText="Add clay" on:submit={handleSubmit} on:click={handleClickOutsideBrandInput}>

    <form on:submit|preventDefault method='POST'>
        <div class="form-group" bind:this={brandInput}>
            <label for="brand" class="p-1">Brand</label>
            <input type="input" class="form-control input-search" bind:value={brand} on:input={updateFilteredBrands} on:click={updateFilteredBrands} on:focus={updateFilteredBrands} on:keydown={handleKeydown} autocomplete="off" id="brand" placeholder="e.g. Sibelco"/>
            {#if filteredBrands.length > 0}
                <ul class="input-search-list list-group">
                    {#each filteredBrands as brandItem, index (brandItem)}
                        <li class="list-group-item {index === highlightedIndex ? 'selected' : ''}" on:click={() => selectBrand(brandItem)}>{brandItem}</li>
                    {/each}
                </ul>
            {/if}
            {#each errors.brand as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
        <div class="form-group">
            <label for="name_id" class="p-1">Name or ID</label>
            <input type="text" class="form-control" bind:value={name_id} on:keydown={handleKeydown} autocomplete="off" id="name_id" placeholder="e.g. WM 2502 B"/>
            {#each errors.name_id as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
        <div class="form-group">
            <label for="color" class="p-1">Color</label>
            <input type="text" class="form-control" bind:value={color} autocomplete="off" id="color" placeholder="e.g. Yellow with spots"/>
            {#each errors.color as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
        <div class="form-group">
            <label for="temp_min" class="p-1">Min. temp.</label>
            <input type="number" class="form-control" bind:value={temp_min} autocomplete="off" id="temp_min" placeholder="°C"/>
            {#each errors.temp_min as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
        <div class="form-group">
            <label for="temp_max" class="p-1">Max. temp.</label>
            <input type="number" class="form-control" bind:value={temp_max} autocomplete="off" id="temp_max" placeholder="°C"/>
            {#each errors.temp_max as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
        <div class="form-group">
            <label for="grog_percent" class="p-1">Grog percentage</label>
            <input type="number" class="form-control" bind:value={grog_percent} autocomplete="off" id="grog_percent" placeholder="%"/>
            {#each errors.grog_percent as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
        <div class="form-group">
            <label for="grog_size_max" class="p-1">Grog size</label>
            <input type="number" class="form-control" bind:value={grog_size_max} autocomplete="off" id="grog_size_max" placeholder="mm"/>
            {#each errors.grog_size_max as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
        <div class="form-group">
            <label for="url" class="p-1">URL</label>
            <input type="text" class="form-control" bind:value={url} autocomplete="off" id="url" placeholder="https://"/>
            {#each errors.url as error}
                <span style="color: red;">[{error}]</span>
            {/each}
        </div>
    </form>

</Modal>

<table class="table table-striped table-hover-color table-hover">
    <thead>
        <tr>
            <th>View pots</th>
            <th>Brand</th>
            <th>Name or ID</th>
            <th>Color</th>
            <th>Min. temp.</th>
            <th>Max. temp.</th>
            <th>Grog percentage</th>
            <th>Grog size</th>
            <th style="padding: 8px 13px;">URL</th>
        </tr>
    </thead>
    <tbody>
        {#each data.clays as clay}
        <tr>
            <td>
                <a href="clay/{ clay.id }" class="hover-border-link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-cup" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M.11 3.187A.5.5 0 0 1 .5 3h13a.5.5 0 0 1 .488.608l-.22.991a3.001 3.001 0 0 1-1.3 5.854l-.132.59A2.5 2.5 0 0 1 9.896 13H4.104a2.5 2.5 0 0 1-2.44-1.958L.012 3.608a.5.5 0 0 1 .098-.42Zm12.574 6.288a2 2 0 0 0 .866-3.899l-.866 3.9ZM1.124 4l1.516 6.825A1.5 1.5 0 0 0 4.104 12h5.792a1.5 1.5 0 0 0 1.464-1.175L12.877 4H1.123Z"/>
                    </svg>
                </a>
            </td>
            <td>{ clay.brand || '' }</td>
            <td>{ clay.name_id || '' }</td>
            <td>{ clay.color || '' }</td>
            <td>{ clay.temp_min !== null ? clay.temp_min + '°C' : ''}</td>
            <td>{ clay.temp_max !== null ? clay.temp_max + '°C' : '' }</td>
            <td>{ clay.grog_percent !== null ? clay.grog_percent + '%' : '' }</td>
            <td>{ clay.grog_size_max !== null ? clay.grog_size_max + 'mm' : '' }</td>
            <td>
                {#if clay.url }
                    <a class="hover-border-link" href="{ clay.url || '' }" target="_blank">
                        Website
                    </a>
                {/if}
            </td>
            <td>
                <button type="button" class="btn btn-outline-secondary" id="open-modal-edit-item-{ clay.id }" data-toggle="modal" data-target="#modal-add-edit-clay" data-reload-page="true" data-itemtype="clay">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                        <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                    </svg>
                </button>
            </td>
        </tr>
        {/each}
    </tbody>
</table>





<style>
    ::placeholder {
        opacity: 0.5;
    }
    .input-search {
        margin-bottom: 0;
        position: relative;
        z-index: 2;
    }
    .input-search-list {
        margin-top: 0;
        list-style-type: none;
        z-index: 1;
        position: absolute;
        width: 100%;
    }
    .list-group-item:hover, .list-group-item.selected {
        background-color: #d0d2d7;
    }
</style>