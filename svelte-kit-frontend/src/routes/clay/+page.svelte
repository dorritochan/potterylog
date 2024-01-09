<script>
    import { API_URL } from '$lib/config';
    import Modal from '../Modal.svelte';
    import { onDestroy, onMount } from 'svelte';

	export let data;
    
    let showModal = false;

    let brand = '';
    let clayBrandList = [];
    let filteredBrands = [];
    let highlightedIndex = -1; // Index of the currently highlighted element in the list
    let name_id = '';
    let clayNamesList = [];
    let filteredClayNames = [];
    let color = '';
    let temp_min = '';
    let temp_max = '';
    let grog_percent = '';
    let grog_size_max = '';
    let url = '';
    let encodedBrand = encodeURIComponent(brand);
    let encodedName = encodeURIComponent(name_id);
    
    onMount(async () => {
        const response = await fetch(`${API_URL}/api/clay_brands`);
        if (response.ok) {
            clayBrandList = await response.json();
        }
    });
    

    let brandInput;
    let nameInput;
    // Close the dropdowns on brand and name when the focus/click is not on the 
    // respective input
    function handleClickOutsideInput(event) {
        if (!brandInput.contains(event.target)) {
            if (!nameInput.contains(event.target)) {
                closeBrandList();
                closeNamesList();
            } else {
                closeBrandList();
            }
        } else {
            closeNamesList();
        }
    }

    function updateFilteredBrands() {
        filteredBrands = clayBrandList.filter(brandFromList => brandFromList.toLowerCase().includes(brand.toLowerCase()));
    }

    async function selectBrand(brandItem) {
        brand = brandItem;
        closeBrandList();

        encodedBrand = encodeURIComponent(brand);

        const response = await fetch(`${API_URL}/api/clay_names/${encodedBrand}`);
        if (response.ok) {
            clayNamesList = await response.json();
        }
    }

    function closeBrandList() {
        filteredBrands = [];
        highlightedIndex = -1;
    }

    function updateFilteredNames() {
        if (brand != '') {
            filteredClayNames = clayNamesList.filter(nameFromList => nameFromList.toLowerCase().includes(name_id.toLowerCase()));
        } else {
            filteredClayNames = [];
        }
    }
    
    async function selectClayName(nameItem) {
        name_id = nameItem;
        closeNamesList();

        encodedBrand = encodeURIComponent(brand);
        encodedName = encodeURIComponent(name_id);

        const response = await fetch(`${API_URL}/api/clay?brand=${encodedBrand}&name_id=${encodedName}`);

        if (response.ok) {
            let data = await response.json();
            color = data.color;
            temp_min = data.temp_min;
            temp_max = data.temp_max;
            grog_percent = data.grog_percent;
            grog_size_max = data.grog_size_max;
            url = data.url;
        }
    }

    function closeNamesList() {
        filteredClayNames = [];
        highlightedIndex = -1;
    }

    let brandState = {
        filteredItems: filteredBrands,
        highlightedIndex: -1,
        selectItem: selectBrand
    }

    let nameState = {
        filteredItems: filteredClayNames,
        highlightedIndex: -1,
        selectItem: selectClayName
    }

    // function handleKeydown(event, state) {
    //     switch(event.key) {
    //         case 'ArrowDown':
    //             console.log('we went down');
    //             console.log(state.highlightedIndex);
    //             console.log(state.filteredItems);
    //             console.log(state.filteredItems.length);
    //             state.highlightedIndex = (state.highlightedIndex + 1) % state.filteredItems.length;
    //             console.log(state.highlightedIndex);
    //             break;
    //         case 'ArrowUp':
    //             state.highlightedIndex = (state.highlightedIndex - 1 + state.filteredItems.length) % state.filteredItems.length;
    //             break;
    //         case 'Enter':
    //             if (state.highlightedIndex >= 0) {
    //                 state.selectItem(state.filteredItems[state.highlightedIndex]);
    //             }
    //             break;
    //         case 'Tab':
    //             closeBrandList();
    //             break;
    //     }
    // }

    
    let errors = { brand: [], name_id: [], color: [], temp_min: [], temp_max: [], grog_percent: [], grog_size_max: [], url: [] };

    function removeErrorMessage(fieldKey) {
        errors[fieldKey] = [];
    }

    function resetValuesForm() {
        brand = '';
        name_id = '';
        color = '';
        temp_min = '';
        temp_max = '';
        grog_percent = '';
        grog_size_max = '';
        url = '';
        Object.keys(errors).forEach(key => {
            removeErrorMessage(key);
        });
        errors = { ...errors };
    }

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
            const errorData = await response.json();

            // Client-side errors (e.g., 400 Bad Request)
            if (response.status >= 400 && response.status < 500) {
                console.error("Client error:", response.status);
                // Show error message to the user
                console.error(errorData.message);
                
                // Server-side errors (e.g., 500 Internal Server Error)
            } else if (response.status >= 500) {
                // Show generic error message to the user
                console.error("Server error:", response.status);
            }
            
            // Set the respective errors in the errors dict
            let errorsMessage = errorData.message;

            let firstError = '';
            Object.keys(errors).forEach(key => {
                    if(errorsMessage[key]) {
                        errors[key] = errorsMessage[key];
                        if (firstError == '') {
                            firstError = key;
                        };
                    }
                });
            console.log(firstError);
            if (firstError == 'brand') {
                brandInput.focus();
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

<Modal bind:showModal modalTitle="Add a new clay" submitText="Add clay" on:submit={handleSubmit} on:resetValues={resetValuesForm} on:click={handleClickOutsideInput} on:focus={handleClickOutsideInput}>

    <form on:submit|preventDefault method='POST'>
        <div class="form-group">
            <div class="label-container">
                <label for="brand" class="p-1">Brand</label>
                <div class="invisible-container"></div>
            </div>
            <input type="search" name="brand" class="form-control input-search" autocomplete="off" id="brand" placeholder="e.g. Sibelco"
                bind:this={brandInput} 
                bind:value={brand} 
                on:input={updateFilteredBrands} 
                on:input={removeErrorMessage('brand')} 
                on:click={updateFilteredBrands} 
                on:focus={updateFilteredBrands} 
                />
            {#if filteredBrands.length > 0}
                <ul class="input-search-list list-group">
                    {#each filteredBrands as brandItem, index (brandItem)}
                        <li class="list-group-item {index === highlightedIndex ? 'selected' : ''}" on:click={() => selectBrand(brandItem)}>{brandItem}</li>
                    {/each}
                </ul>
            {/if}
            <div class="error-message">
                <small>
                    {#each errors.brand as error}
                    {error}
                    {/each}
                </small>
            </div>
        </div>
        <div class="form-group">
            <div class="label-container">
                <label for="name_id" class="p-1">Name or ID</label>
                <div class="invisible-container"></div>
            </div>
            <input type="search" name="name_id" class="form-control" autocomplete="off" id="name_id" placeholder="e.g. WM 2502 B"
            bind:this={nameInput}
            bind:value={name_id}
            on:input={removeErrorMessage('name_id')}
            on:input={updateFilteredNames}
            on:focus={updateFilteredNames}/>
            {#if filteredClayNames.length > 0}
                <ul class="input-search-list list-group">
                    {#each filteredClayNames as nameItem, index (nameItem)}
                        <li class="list-group-item {index === highlightedIndex ? 'selected' : ''}" on:click={() => selectClayName(nameItem)}>{nameItem}</li>
                    {/each}
                </ul>
            {/if}
            <div class="error-message">
                <small>
                    {#each errors.name_id as error}
                    {error}
                    {/each}
                </small>
            </div>
        </div>
        <div class="form-group">
            <div class="label-container">
                <label for="color" class="p-1">Color</label>
                <div class="invisible-container"></div>
            </div>
            <input type="search" name="color" class="form-control" bind:value={color} on:input={removeErrorMessage('color')} autocomplete="off" id="color" placeholder="e.g. Yellow with spots"/>
            <div class="error-message">
                <small>
                    {#each errors.color as error}
                    {error}
                    {/each}
                </small>
            </div>
        </div>
        <div class="d-flex justify-content-between">
            <div class="form-group col-5">
                <div class="label-container">
                    <label for="temp_min" class="p-1">Min. temp.</label>
                    <div class="invisible-container"></div>
                </div>
                <div class="input-group">
                    <input type="number" name="temp_min" class="form-control" autocomplete="off"
                        bind:value={temp_min} 
                        on:input={removeErrorMessage('temp_min')} />
                    <div class="input-group-append">
                        <span class="input-group-text" id="basic-addon1">°C</span>
                    </div>
                </div>
                <div class="error-message">
                    <small>
                        {#each errors.temp_min as error}
                        {error}
                        {/each}
                    </small>
                </div>
            </div>
            <div class="form-group col-5">
                <div class="label-container">
                    <label for="temp_max" class="p-1">Max. temp.</label>
                    <div class="invisible-container"></div>
                </div>
                <div class="input-group">
                    <input type="number" name="temp_max" class="form-control" autocomplete="off"
                    bind:value={temp_max} 
                    on:input={removeErrorMessage('temp_max')}/>
                    <div class="input-group-append">
                        <span class="input-group-text" id="basic-addon1">°C</span>
                    </div>
                </div>
                <div class="error-message">
                    <small>
                        {#each errors.temp_max as error}
                        {error}
                        {/each}
                    </small>
                </div>
            </div>
        </div>
        <div class="d-flex justify-content-between">
            <div class="form-group col-5">
                <div class="label-container">
                    <label for="grog_percent" class="p-1">Grog percentage</label>
                    <div class="invisible-container"></div>
                </div>
                <div class="input-group">
                    <input type="number" name="grog_percent" class="form-control" autocomplete="off" 
                    bind:value={grog_percent} 
                    on:input={removeErrorMessage('grog_percent')} />
                    <div class="input-group-append">
                        <span class="input-group-text" id="basic-addon1">%</span>
                    </div>
                </div>
                <div class="error-message">
                    <small>
                        {#each errors.grog_percent as error}
                        {error}
                        {/each}
                    </small>
                </div>
            </div>
            <div class="form-group col-5">
                <div class="label-container">
                    <label for="grog_size_max" class="p-1">Grog size</label>
                    <div class="invisible-container"></div>
                </div>
                <div class="input-group">
                    <input type="number" name="grog_size_max" class="form-control" autocomplete="off"
                    bind:value={grog_size_max} 
                    on:input={removeErrorMessage('grog_size_max')} />
                    <div class="input-group-append">
                        <span class="input-group-text" id="basic-addon1">mm</span>
                    </div>
                </div>

                <div class="error-message">
                    <small>
                        {#each errors.grog_size_max as error}
                        {error}
                        {/each}
                    </small>
                </div>
            </div>
        </div>
        <div class="form-group">
            <div class="label-container">
                <label for="url" class="p-1">URL</label>
                <div class="invisible-container"></div>
            </div>
            <input type="search" name="url" class="form-control" bind:value={url} on:input={removeErrorMessage('url')} autocomplete="off" id="url" placeholder="https://"/>
            <div class="error-message">
                <small>
                    {#each errors.url as error}
                    {error}
                    {/each}
                </small>
            </div>
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
        z-index: 3;
    }
    .input-search-list {
        margin-top: 0;
        list-style-type: none;
        z-index: 2;
        position: absolute;
        width: 100%;
        box-sizing: border-box; 
        margin: 0;
        padding: 0;
    }
    .list-group-item:hover, .list-group-item.selected {
        background-color: #d0d2d7;
    }
    input {
        margin-bottom: 0;
    }

    small {
        font-style: italic;
        color: red;
        min-height: 15px;
        margin: 0;
        padding-left: 3px;
    }
    .error-message small {
        display: block;
    }
    .form-group {
        position: relative;
    }
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