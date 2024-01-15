<script>
    import { API_URL } from '$lib/config';
    import Modal from '../Modal.svelte';
    import { onDestroy, onMount } from 'svelte';
    import { fade, fly } from 'svelte/transition';

	export let data;
    
    let showAddModal = false;
    let showEditModal = false;
    let editingClay = null;
    let dialog;

    let _schema = '';
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

    $: if(!showAddModal) {
        Object.keys(errors).forEach(key => {
            removeErrorMessage(key);
        });
    }
    
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

    $: brandState = {
        filteredItems: filteredBrands,
        highlightedIndex,
        selectItem: selectBrand
    }

    $: nameState = {
        filteredItems: filteredClayNames,
        highlightedIndex,
        selectItem: selectClayName
    }



    function handleKeydown(event, state) {
        switch(event.key) {
            case 'ArrowDown':
                highlightedIndex = (highlightedIndex + 1) % state.filteredItems.length;
                break;
            case 'ArrowUp':
                highlightedIndex = (highlightedIndex - 1 + state.filteredItems.length) % state.filteredItems.length;
                break;
            case 'Enter':
                if (state.highlightedIndex >= 0) {
                    state.selectItem(state.filteredItems[highlightedIndex]);
                }
                break;
            case 'Tab':
                if (state == brandState){
                    closeBrandList();
                } else if (state == nameState) {
                    closeNamesList();
                }
                break;
        }
    }

    
    let errors = { _schema: [], brand: [], name_id: [], color: [], temp_min: [], temp_max: [], grog_percent: [], grog_size_max: [], url: [] };

    function removeErrorMessage(fieldKey) {
        errors[fieldKey] = [];
    }

    function resetValuesForm() {
        _schema = '';
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
                brand, name_id, color, temp_min, temp_max, grog_percent, grog_size_max, url 
            })
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result.message);
            resetValuesForm();
            showAddModal = false;
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
            focusOnError(firstError);
        }
    }

    let schemaGroup;
    let brandGroup;
    let nameGroup;
    let colorGroup;
    let tempMinGroup;
    let tempMaxGroup;
    let grogPercentGroup;
    let grogSizeMaxGroup;
    let urlGroup;
    function focusOnError(firstError) {
        let target;
        switch(firstError) {
            case '_schema':
                target = schemaGroup;
                break;
            case 'brand':
                target = brandGroup;
                break;
            case 'name_id':
                target = nameGroup;
                break;
            case 'color':
                target = colorGroup;
                break;
            case 'temp_min':
                target = tempMinGroup;
                break;
            case 'temp_max':
                target = tempMaxGroup;
                break;
            case 'grog_percentage':
                target = grogPercentGroup;
                break;
            case 'grog_size_max':
                target = grogSizeMaxGroup;
                break;
            case 'url':
                target = urlGroup;
                break;
        }
        if(dialog && target) {

            const modalRect = dialog.getBoundingClientRect();
            const targetRect = target.getBoundingClientRect();

            // Calculate relative position of the target element within the modal
            const relativeTop = targetRect.top - modalRect.top;

            // Scroll to the element
            dialog.scrollTop = dialog.scrollTop + relativeTop;

        }
    }


</script>

<svelte:head>
    <title>List of clays</title>
</svelte:head>


<h1 class="m-3">List of clays</h1>

<div class="m-3">
    <button on:click={() => showAddModal = true} type="button" class="btn btn-primary">&plus; Add a new clay</button>
</div>

<Modal 
    bind:showAddModal 
    bind:dialog 
    modalTitle="{showEditModal ? 'Edit clay' : 'Add a new clay'}" 
    submitText="{showEditModal ? 'Update clay' : 'Add clay'}" 
    on:submit={handleSubmit} 
    on:resetValues={resetValuesForm} 
    on:click={handleClickOutsideInput} 
    on:focus={handleClickOutsideInput}
>

    <form on:submit|preventDefault method='POST'>
        <div class="container" bind:this={schemaGroup}>
            <div class="row">
                <div class="error-message">
                    <small>
                        {#each errors._schema as error}
                        <p in:fly={{ y: 200, duration: 2000 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                        {/each}
                    </small>
                </div>
                <div class="form-group" bind:this={brandGroup}>
                <div class="label-container">
                    <label for="brand" class="p-1">Brand</label>
                    <div class="invisible-container"></div>
                </div>
                <input type="search" name="brand" class="form-control input-search" autocomplete="off" id="brand" placeholder="e.g. Sibelco"
                    bind:this={brandInput} 
                    bind:value={brand} 
                    on:input={updateFilteredBrands} 
                    on:input={() => {removeErrorMessage('brand')}} 
                    on:input={() => {removeErrorMessage('_schema')}} 
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
            </div>
            <div class="row">
                <div class="form-group" bind:this={nameGroup}>
                <div class="label-container">
                    <label for="name_id" class="p-1">Name or ID</label>
                    <div class="invisible-container"></div>
                </div>
                <input type="search" name="name_id" class="form-control" autocomplete="off" id="name_id" placeholder="e.g. WM 2502 B"
                bind:this={nameInput}
                bind:value={name_id}
                on:input={() => {removeErrorMessage('name_id')}}
                on:input={() => {removeErrorMessage('_schema')}}
                on:input={updateFilteredNames}
                on:focus={updateFilteredNames}
                on:keydown={(event)=>handleKeydown(event, nameState)}/>
                {#if filteredClayNames.length > 0}
                    <ul class="input-search-list list-group" transition:fly={{  y: 200, duration: 1000 }}>
                        {#each filteredClayNames as nameItem, index (nameItem)}
                            <li class="list-group-item {index === highlightedIndex ? 'selected' : ''}" on:click={() => selectClayName(nameItem)}>{nameItem}</li>
                        {/each}
                    </ul>
                {/if}
                <div class="error-message">
                    <small>
                        {#each errors.name_id as error}
                        <p in:fly={{ y: 200, duration: 1000 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                        {/each}
                    </small>
                </div>
                </div>
            </div>
            <div class="row">
                <div class="form-group" bind:this={colorGroup}>
                <div class="label-container">
                    <label for="color" class="p-1">Color</label>
                    <div class="invisible-container"></div>
                </div>
                <input type="search" name="color" class="form-control" autocomplete="off" placeholder="e.g. Yellow with spots"
                    bind:value={color} 
                    on:input={() => {removeErrorMessage('color')}} />
                <div class="error-message">
                    <small>
                        {#each errors.color as error}
                        <p in:fly={{ y: 200, duration: 800 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                        {/each}
                    </small>
                </div>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={tempMinGroup}>
                    <div class="label-container">
                        <label for="temp_min" class="p-1">Min. temp.</label>
                        <div class="invisible-container"></div>
                    </div>
                    <div class="input-group">
                        <input type="number" name="temp_min" class="form-control" autocomplete="off"
                            bind:value={temp_min} 
                            on:input={() => {removeErrorMessage('temp_min')}} />
                        <div class="input-group-append">
                            <span class="input-group-text" id="basic-addon1">°C</span>
                        </div>
                    </div>
                    <div class="error-message">
                        <small>
                            {#each errors.temp_min as error}
                            <p in:fly={{ y: 200, duration: 700 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                            {/each}
                        </small>
                    </div>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={tempMaxGroup}>
                    <div class="label-container">
                        <label for="temp_max" class="p-1">Max. temp.</label>
                        <div class="invisible-container"></div>
                    </div>
                    <div class="input-group">
                        <input type="number" name="temp_max" class="form-control" autocomplete="off"
                        bind:value={temp_max} 
                        on:input={() => {removeErrorMessage('temp_max')}}/>
                        <div class="input-group-append">
                            <span class="input-group-text" id="basic-addon1">°C</span>
                        </div>
                    </div>
                    <div class="error-message">
                        <small>
                            {#each errors.temp_max as error}
                            <p in:fly={{ y: 200, duration: 700 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                            {/each}
                        </small>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={grogPercentGroup}>
                    <div class="label-container">
                        <label for="grog_percent" class="p-1">Grog percentage</label>
                        <div class="invisible-container"></div>
                    </div>
                    <div class="input-group">
                        <input type="number" name="grog_percent" class="form-control" autocomplete="off" 
                        bind:value={grog_percent} 
                        on:input={() => {removeErrorMessage('grog_percent')}} />
                        <div class="input-group-append">
                            <span class="input-group-text" id="basic-addon1">%</span>
                        </div>
                    </div>
                    <div class="error-message">
                        <small>
                            {#each errors.grog_percent as error}
                            <p in:fly={{ y: 200, duration: 600 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                            {/each}
                        </small>
                    </div>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={grogSizeMaxGroup}>
                    <div class="label-container">
                        <label for="grog_size_max" class="p-1">Grog size</label>
                        <div class="invisible-container"></div>
                    </div>
                    <div class="input-group">
                        <input type="number" name="grog_size_max" class="form-control" autocomplete="off"
                        bind:value={grog_size_max} 
                        on:input={() => {removeErrorMessage('grog_size_max')}} />
                        <div class="input-group-append">
                            <span class="input-group-text" id="basic-addon1">mm</span>
                        </div>
                    </div>

                    <div class="error-message">
                        <small>
                            {#each errors.grog_size_max as error}
                            <p in:fly={{ y: 200, duration: 600 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                            {/each}
                        </small>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="form-group" bind:this={urlGroup}>
                <div class="label-container">
                    <label for="url" class="p-1">URL</label>
                    <div class="invisible-container"></div>
                </div>
                <input type="search" name="url" class="form-control" autocomplete="off" placeholder="https://"
                bind:value={url} on:input={() => {removeErrorMessage('url')}} />
                <div class="error-message">
                    <small>
                        {#each errors.url as error}
                        <p in:fly={{ y: 200, duration: 500 }} out:fade={{ delay: 250, duration: 500}}>{error}</p>
                        {/each}
                    </small>
                </div>
                </div>
            </div>
        </div>
    </form>

</Modal>

<div class="table-container">
    <table class="table table-striped table-hover-color table-hover">
        <thead>
            <tr>
                <th>View pots</th>
                <th>Brand</th>
                <th>Name or ID</th>
                <th>Color</th>
                <th>Min °C</th>
                <th>Max °C</th>
                <th>Grog %</th>
                <th>Grog size</th>
                <th style="padding: 8px 13px;">URL</th>
                <th></th>
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
                    <button class="hover-border-link" 
                        on:click={() => {
                            showEditModal = true;
                            editingClay = clay;
                        }}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512" fill="currentColor">
                            <!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
                            <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 480.7c-2.5 8.4-.2 17.5 6.1 23.7s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.7 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 325.7 55.8 314.3 67.1l33.9 33.9 62.1 62.1 33.9 33.9 11.3-11.3 22.6-22.6 14.5-14.5c25-25 25-65.5 0-90.5L453.3 18.7c-25-25-65.5-25-90.5 0zm-47.4 168l-144 144c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6l144-144c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"/>
                        </svg>
                    </button>
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
</div>





<style>
    ::placeholder {
        opacity: 0.5;
    }
    .input-search {
        position: relative;
        z-index: 3;
        box-sizing: border-box;
    }
    .input-search-list {
        list-style-type: none;
        z-index: 2;
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
    input {
        margin-bottom: 0;
        box-shadow: 1px 6px 10px -10px #666;
    }

    small {
        font-style: bold;
        color: rgba(240, 11, 11, 0.978);
        min-height: 15px;
        margin: 0;
        padding-left: 3px;
    }
    .error-message small {
        display: block;
    }
    .form-group {
        position: relative;
        width: 100%;
        flex: 1 1 200px; /* Flex-grow, flex-shrink, flex-basis */
        margin: 0;
        padding: 0;
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
    .container{
        padding-left: 2;
        padding-right: 2;
    }
    .row{
        padding: 0;
    }
</style>