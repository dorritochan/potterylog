<script>
    import { API_URL } from '$lib/config';
    import { onMount } from 'svelte';
    import { error } from '@sveltejs/kit';

    import Modal from '$lib/components/Modal.svelte';
    import TableClay from '$lib/components/TableClay.svelte';
    import ButtonTransparent from '$lib/components/ButtonTransparent.svelte';
    import LabelInput from '$lib/components/forms/LabelInput.svelte';
    import InputSearch from '$lib/components/forms/InputSearch.svelte';
    import InputNumber from '$lib/components/forms/InputNumber.svelte';
    import InputWithSearch from '$lib/components/forms/InputWithSearch.svelte';
    import InputDisabled from '$lib/components/forms/InputDisabled.svelte';
    import ErrorMessageInput from '$lib/components/forms/ErrorMessageInput.svelte';
    
    
    // The clay data for the table
	export let data;
    
    onMount(async () => {
        dbBrandList = await getBrandList();
    });

    // A boolean variable: if true, the modal shows
    let showAddModal = false;
    let dialog;

    // State variables for form inputs
    let _schema = '';
    let brand = '';
    let name_id = '';
    let color = '';
    let temp_min = '';
    let temp_max = '';
    let grog_percent = '';
    let grog_size_max = '';
    let url = '';

    // The list of error messages
    let errors = { _schema: [], brand: [], name_id: [], color: [], temp_min: [], temp_max: [], grog_percent: [], grog_size_max: [], url: [] };

    // List of form groups needed for binding for showing the errors
    let schemaGroup;
    let brandGroup;
    let nameGroup;
    let colorGroup;
    let tempMinGroup;
    let tempMaxGroup;
    let grogPercentGroup;
    let grogSizeMaxGroup;
    let urlGroup;

    // Variables for binding with the respective inputs and managing
    // the clicks outside of them
    let brandInput;
    let nameInput;

    // The whole list of brands from the DB
    let dbBrandList = [];
    // Filter the brands on input and save them in a list
    let filteredBrands = [];
    // Index of the currently highlighted element in the list: for brand and name_id inputs
    let highlightedIndex = -1;
    // The whole list of names, based on the chosen brand
    let dbNamesList = [];
    // Filter the names on input and save them in a list
    let filteredNames = [];
    // Boolean: if true, the edit mode is turned on for the modal
    let editMode = false;
    // The clay ID passed from the table needed for editing
    let clayId;
    // Encoding of values for passing in URL
    $: encodedBrand = encodeURIComponent(brand);
    $: encodedName = encodeURIComponent(name_id);
    

    $: if (!showAddModal && dialog) {
        resetValuesForm();
        editMode = false;
    }

    // The states for handling keydowns
    $: brandState = {
        filteredItems: filteredBrands,
        highlightedIndex,
        selectItem: selectBrand
    }

    $: nameState = {
        filteredItems: filteredNames,
        highlightedIndex,
        selectItem: selectName
    }

    function openModal(){
        showAddModal = true;
    }

    // Close the dropdowns on brand and name when the focus/click is not on the 
    // respective input
    function handleClickOutsideInput(event) {
        const isOutsideBrandInput = !brandInput.contains(event.target);
        const isOutsideNameInput = !nameInput.contains(event.target);
        if (isOutsideBrandInput && isOutsideNameInput) {
            closeBrandList();
            closeNamesList();
        } else if (isOutsideBrandInput) {
            closeBrandList();
        } else if (isOutsideNameInput) {
            closeNamesList();
        }
    }
    
    function updateFilteredBrands() {
        filteredBrands = dbBrandList.filter(brandFromList => brandFromList.toLowerCase().includes(brand.toLowerCase()));
    }

    function updateFilteredNames() {
        if (brand != '') {
            filteredNames = dbNamesList.filter(nameFromList => nameFromList.toLowerCase().includes(name_id.toLowerCase()));
        } else {
            filteredNames = [];
        }
    }

    function closeBrandList() {
        filteredBrands = [];
        highlightedIndex = -1;
    }

    function closeNamesList() {
        filteredNames = [];
        highlightedIndex = -1;
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

    function removeErrorMessage(fieldKey) {
        errors[fieldKey] = [];
    }

    function resetValuesForm() {
        _schema = '';
        if (!editMode) {
            brand = '';
            name_id = '';
        }
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

    // Fetching the list of clays after deleting, adding, updating
    async function fetchClayList() {

        const response = await fetch(`${API_URL}/api/clays`);

        if (!response.ok) {
            const errorBody = await response.json();
            console.log(`errorBody.message: ${errorBody.message}`);

            throw error(response.status, {
                message: errorBody.message
            })
        }

        const clays = await response.json();
        return clays;
    }

    // Fetch the list of brands on click on brand input
    async function getBrandList() {
        const response = await fetch(`${API_URL}/api/clay_brands`);
        if (response.ok) {
            const brandList = await response.json();
            return brandList;
        }
    }

    async function selectBrand(brandItem) {
        brand = brandItem;
        closeBrandList();

        encodedBrand = encodeURIComponent(brand);

        const response = await fetch(`${API_URL}/api/clay_names/${encodedBrand}`);
        if (response.ok) {
            dbNamesList = await response.json();
        }
    }

    async function selectName(nameItem) {
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
    
    async function handleSubmit() {
        let response;
        if (!editMode){
            response = await fetch(`${API_URL}/api/add_clay`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    brand, name_id, color, temp_min, temp_max, grog_percent, grog_size_max, url 
                })
            });
        } else {
            response = await fetch(`${API_URL}/api/update_clay/${clayId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    brand, name_id, color, temp_min, temp_max, grog_percent, grog_size_max, url 
                })
            });
        }

        if (response.ok) {
            const result = await response.json();
            console.log(result.message);
            resetValuesForm();
            showAddModal = false;
            
            data.clays = await fetchClayList();

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

    async function handleEditClick(clayIdEvent) {

        editMode = true;
        clayId = clayIdEvent.detail;
        console.log("Edit button clicked for clay ID:", clayId);

        const response = await fetch(`${API_URL}/api/clay/${clayId}`);

        if (response.ok) {
            let data = await response.json();
            brand = data.brand;
            name_id = data.name_id;
            color = data.color;
            temp_min = data.temp_min;
            temp_max = data.temp_max;
            grog_percent = data.grog_percent;
            grog_size_max = data.grog_size_max;
            url = data.url;
        }
    }

    async function deleteClay(){
        const response = await fetch(`${API_URL}/api/delete_clay/${clayId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorMessage = await response.json()
            _schema = errorMessage.message;
            console.log(`Error: ${_schema}`);
        } else {
            data.clays = await fetchClayList();
            showAddModal = false;
            dbBrandList = await getBrandList();
        }
    }

</script>

<svelte:head>
    <title>List of clays</title>
</svelte:head>


<div class="m-3 page-title">
    <h1>
        List of clays
    </h1>
</div>

<div class="m-3 centered">
    <ButtonTransparent handleOnClick={openModal} buttonText={'&plus; Add a new clay'}/>
</div>

<Modal 
    bind:showAddModal 
    bind:dialog 
    modalTitle="{editMode ? 'Edit clay' : 'Add a new clay'}" 
    submitText="{editMode ? 'Update clay' : 'Add clay'}" 
    on:submit={handleSubmit} 
    on:resetValues={resetValuesForm} 
    on:click={handleClickOutsideInput} 
    on:focus={handleClickOutsideInput}
    {editMode}
    deleteBtnLabel={'Delete clay'}
    handleDelete={deleteClay}
>

    <form on:submit|preventDefault method='POST'>
        <div class="container" bind:this={schemaGroup}>
            <div class="row">
                <ErrorMessageInput errors={errors._schema}/>
                <div class="form-group" bind:this={brandGroup}>
                    <LabelInput labelFor={brand} label={'Brand'}/>
                    <div bind:this={brandInput}>
                        {#if editMode}
                        <InputDisabled name={'brand'} bind:value={brand} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'brand'} placeholder={'e.g. Sibelco'} bind:value={brand} 
                                removeErrorMessage={removeErrorMessage} updateFilteredItems={updateFilteredBrands} errorKeys={['brand', '_schema']}
                                state={brandState} filteredItems={filteredBrands} highlightedIndex={highlightedIndex} selectItem={selectBrand} handleKeydown={handleKeydown}
                            />
                        {/if}
                    </div>
                    <ErrorMessageInput errors={errors.brand}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group" bind:this={nameGroup}>
                    <LabelInput labelFor={name_id} label={'Name or ID'}/>
                    <div bind:this={nameInput}>
                        {#if editMode}
                        <InputDisabled name={'name_id'} bind:value={name_id} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'name_id'} placeholder={'e.g. WM 2502 B'} bind:value={name_id} 
                                removeErrorMessage={removeErrorMessage} updateFilteredItems={updateFilteredNames} errorKeys={['name_id', '_schema']}
                                state={nameState} filteredItems={filteredNames} highlightedIndex={highlightedIndex} selectItem={selectName} handleKeydown={handleKeydown}
                            />
                        {/if}   
                    </div>
                    <ErrorMessageInput errors={errors.name_id}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group" bind:this={colorGroup}>
                    <LabelInput labelFor={color} label={'Color'}/>
                    <InputSearch name={'color'} className={'form-control'} placeholder={'e.g. Yellow with spots'} bind:value={color} errorKey={'color'} removeErrorMessage={removeErrorMessage}/>
                    <ErrorMessageInput errors={errors.color}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={tempMinGroup}>
                    <LabelInput labelFor={temp_min} label={'Min. temp.'}/>
                    <InputNumber name={'temp_min'} className={'form-control'} placeholder={''} bind:value={temp_min} errorKey={'temp_min'} removeErrorMessage={removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={errors.temp_min}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={tempMaxGroup}>
                    <LabelInput labelFor={temp_max} label={'Max. temp.'}/>
                    <InputNumber name={'temp_max'} className={'form-control'} placeholder={''} bind:value={temp_max} errorKey={'temp_max'} removeErrorMessage={removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={errors.temp_max}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={grogPercentGroup}>
                    <LabelInput labelFor={grog_percent} label={'Grog percentage'}/>
                    <InputNumber name={'grog_percent'} className={'form-control'} placeholder={''} bind:value={grog_percent} errorKey={'grog_percent'} removeErrorMessage={removeErrorMessage} addOn={'%'}/>
                    <ErrorMessageInput errors={errors.grog_percent}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={grogSizeMaxGroup}>
                    <LabelInput labelFor={grog_size_max} label={'Grog size'}/>
                    <InputNumber name={'grog_size_max'} className={'form-control'} placeholder={''} bind:value={grog_size_max} errorKey={'grog_size_max'} removeErrorMessage={removeErrorMessage} addOn={'mm'}/>
                    <ErrorMessageInput errors={errors.grog_percent}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group" bind:this={urlGroup}>
                    <LabelInput labelFor={url} label={'URL'}/>
                    <InputSearch name={'url'} className={'form-control'} placeholder={'https://'} bind:value={url} errorKey={'url'} removeErrorMessage={removeErrorMessage}/>
                    <ErrorMessageInput errors={errors.url}/>
                </div>
            </div>
        </div>
    </form>

</Modal>

<TableClay data={data.clays} handleOnClickEdit={openModal} on:edit={handleEditClick}/>



<style>
    .centered{
        display: flex;
        justify-content: center;
    }
    .form-group {
        position: relative;
        width: 100%;
        flex: 1 1 200px; /* Flex-grow, flex-shrink, flex-basis */
        margin: 0;
        padding: 0;
    }

    .container{
        padding-left: 2;
        padding-right: 2;
    }
    .row{
        padding: 0;
    }
</style>