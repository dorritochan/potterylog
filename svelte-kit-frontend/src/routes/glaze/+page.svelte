<script>
    import { API_URL } from '$lib/config';
    import Modal from '../Modal.svelte';
    import TableGlaze from '../TableGlaze.svelte';
    import InputSearch from '../InputSearch.svelte';
    import InputNumber from '../InputNumber.svelte';
    import ErrorMessageInput from '../ErrorMessageInput.svelte';
    import LabelInput from '../LabelInput.svelte';
    import InputWithSearch from '../InputWithSearch.svelte';
    import InputDisabled from '../InputDisabled.svelte';
    import { onMount } from 'svelte';
    import ButtonTransparent from '../ButtonTransparent.svelte';
    import { _fetchGlazeList, _deleteGlaze, _fetchBrandList, _selectBrand } from './+page';
    
    
    // The glaze data for the table
	export let data;
    console.log('data');
    console.log(data);
    console.log('data.glazes');
    console.log(data.glazes);
    
    onMount(async () => {
        dbBrandList = await _fetchBrandList(API_URL);
    });

    // A boolean variable: if true, the modal shows
    let showAddModal = false;
    let dialog;

    // State variables for form inputs
    let _schema = '';
    let brand = '';
    let brand_id = '';
    let name = '';
    let color = '';
    let temp_min = '';
    let temp_max = '';
    let cone = '';
    let glaze_url = '';

    // The list of error messages
    let errors = { _schema: [], brand: [], brand_id: [], name: [], color: [], temp_min: [], temp_max: [], cone: [], glaze_url: [] };

    // List of form groups needed for binding for showing the errors
    let schemaGroup;
    let brandGroup;
    let nameGroup;
    let idGroup;
    let colorGroup;
    let tempMinGroup;
    let tempMaxGroup;
    let coneGroup;
    let urlGroup;

    // Variables for binding with the respective inputs and managing
    // the clicks outside of them
    let brandInput;
    let nameInput;
    let idInput;
    let coneInput;

    // The whole list of brands from the DB
    let dbBrandList = [];
    // Filter the brands on input and save them in a list
    let filteredBrands = [];
    // Index of the currently highlighted element in the list: for brand and id inputs
    let highlightedIndex = -1;
    // The whole list of ids, based on the chosen brand
    let dbIdsList = [];
    // Filter the ids on input and save them in a list
    let filteredIds = [];
    // The whole list of names, based on the chosen brand
    let dbNamesList = [];
    // Filter the names on input and save them in a list
    let filteredNames = [];
    // The list of all the possible cone numbers
    let dbConesList = ['019', '018', '017', '016', '015', '014', '013', '012', '011',
            '010', '09', '08', '07', '06', '05', '04', '03', '02', '01',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
    // Filter the list of cones and save them a list
    let filteredCones = [];
    // Boolean: if true, the edit mode is turned on for the modal
    let editMode = false;
    // The glaze ID passed from the table needed for editing
    let glazeId;
    // Encoding of values for passing in glaze_url
    $: encodedBrand = encodeURIComponent(brand);
    $: encodedName = encodeURIComponent(name);
    $: encodedId = encodeURIComponent(brand_id);
    

    $: if (!showAddModal && dialog) {
        resetValuesForm();
        editMode = false;
    }

    // The states for handling keydowns
    $: brandState = {
        filteredItems: filteredBrands,
        highlightedIndex,
        selectItem: _selectBrand
    }

    $: nameState = {
        filteredItems: filteredNames,
        highlightedIndex,
        selectItem: selectName
    }

    $: idState = {
        filteredItems: filteredIds,
        highlightedIndex,
        selectItem: selectId
    }

    $: coneState = {
        filteredItems: filteredCones,
        highlightedIndex,
        selectItem: selectCone
    }

    function openModal(){
        showAddModal = true;
    }

    // Close the dropdowns on brand and name when the focus/click is not on the 
    // respective input
    function handleClickOutsideInput(event) {
        const isOutsideBrandInput = !brandInput.contains(event.target);
        const isOutsideIdInput = !idInput.contains(event.target);
        const isOutsideNameInput = !nameInput.contains(event.target);
        const isOutsideConeInput = !coneInput.contains(event.target);
        if (isOutsideBrandInput) {
            closeBrandList();
        }
        if (isOutsideIdInput) {
            closeIdsList();
        }
        if (isOutsideNameInput) {
            closeNamesList();
        }
        if (isOutsideConeInput) {
            closeConesList();
        }
    }
    
    function updateFilteredBrands() {
        filteredBrands = dbBrandList.filter(brandFromList => brandFromList.toLowerCase().includes(brand.toLowerCase()));
    }

    function updateFilteredIds() {
        if (brand != '') {
            filteredIds = dbIdsList.filter(idFromList => idFromList.toLowerCase().includes(brand_id.toLowerCase()));
        } else {
            filteredIds = [];
        }
    }

    function updateFilteredNames() {
        if (brand != '') {
            filteredNames = dbNamesList.filter(nameFromList => nameFromList.toLowerCase().includes(name.toLowerCase()));
        } else {
            filteredNames = [];
        }
    }

    function updateFilteredCones() {
        filteredCones = dbConesList.filter(coneFromList => coneFromList.toLowerCase().includes(cone.toLowerCase()));
    }

    function closeBrandList() {
        filteredBrands = [];
        highlightedIndex = -1;
    }

    function closeNamesList() {
        filteredNames = [];
        highlightedIndex = -1;
    }

    function closeIdsList() {
        filteredIds = [];
        highlightedIndex = -1;
    }

    function closeConesList() {
        filteredCones = [];
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
                } else if (state == idState) {
                    closeIdsList();
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
            brand_id = '';
            name = '';
        }
        color = '';
        temp_min = '';
        temp_max = '';
        cone = '';
        glaze_url = '';
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
            case 'brand_id':
                target = idGroup;
                break;
            case 'name':
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
            case 'cone':
                target = coneGroup;
                break;
            case 'glaze_url':
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

    async function selectName(nameItem) {
        name = nameItem;
        closeNamesList();
        // closeIdsList();

        encodedBrand = encodeURIComponent(brand);
        encodedName = encodeURIComponent(name);

        const response = await fetch(`${API_URL}/api/glaze_from_name?brand=${encodedBrand}&name=${encodedName}`);

        if (response.ok) {
            let data = await response.json();
            brand_id = data.brand_id;
            color = data.color;
            temp_min = data.temp_min;
            temp_max = data.temp_max;
            cone = data.cone;
            glaze_url = data.glaze_url;
        }
    }

    async function selectId(idItem) {
        brand_id = idItem;
        closeIdsList();

        encodedBrand = encodeURIComponent(brand);
        encodedId = encodeURIComponent(brand_id);

        const response = await fetch(`${API_URL}/api/glaze_from_id?brand=${encodedBrand}&brand_id=${encodedId}`);

        if (response.ok) {
            let data = await response.json();
            name = data.name;
            color = data.color;
            temp_min = data.temp_min;
            temp_max = data.temp_max;
            cone = data.cone;
            glaze_url = data.glaze_url;
        }
    }

    function selectCone(coneItem) {
        cone = coneItem;
        closeConesList();
    }

    async function handleSubmit() {
        let response;
        if (!editMode){
            response = await fetch(`${API_URL}/api/add_glaze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    brand, brand_id, name, color, temp_min, temp_max, cone, glaze_url
                })
            });
        } else {
            response = await fetch(`${API_URL}/api/update_glaze/${glazeId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    brand, brand_id, name, color, temp_min, temp_max, cone, glaze_url
                })
            });
        }

        if (response.ok) {
            const result = await response.json();
            console.log(result.message);
            resetValuesForm();
            showAddModal = false;
            
            data.glazes = await _fetchGlazeList(API_URL);

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

    async function handleEditClick(glazeIdEvent) {

        editMode = true;
        glazeId = glazeIdEvent.detail;
        console.log("Edit button clicked for glaze ID:", glazeId);

        const response = await fetch(`${API_URL}/api/glaze/${glazeId}`);

        if (response.ok) {
            let data = await response.json();
            brand = data.brand;
            brand_id = data.brand_id;
            name = data.name;
            color = data.color;
            temp_min = data.temp_min;
            temp_max = data.temp_max;
            cone = data.cone;
            glaze_url = data.glaze_url;
        }
    }

    function selectItem(item, event) {
        switch(event.target.name){
            case 'brand':
                _selectBrand(API_URL, item, brand, closeBrandList, dbIdsList, dbNamesList);
                break;

        }
    }

</script>

<svelte:head>
    <title>List of glazes</title>
</svelte:head>


<div class="m-3 page-title">
    <h1>
        List of glazes
    </h1>
</div>

<div class="m-3 centered">
    <ButtonTransparent handleOnClick={openModal} buttonText={'&plus; Add a new glaze'}/>
</div>

<Modal 
    bind:showAddModal 
    bind:dialog 
    modalTitle="{editMode ? 'Edit glaze' : 'Add a new glaze'}" 
    submitText="{editMode ? 'Update glaze' : 'Add glaze'}" 
    on:submit={handleSubmit} 
    on:resetValues={resetValuesForm} 
    on:click={handleClickOutsideInput} 
    on:focus={handleClickOutsideInput}
    {editMode}
    deleteBtnLabel={'Delete glaze'}
    handleDelete={()=>_deleteGlaze(API_URL, glazeId, _schema, data, showAddModal, dbBrandList)}
>

    <form on:submit|preventDefault method='POST'>
        <div class="container" bind:this={schemaGroup}>
            <div class="row">
                <ErrorMessageInput errors={errors._schema}/>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={brandGroup}>
                    <LabelInput labelFor={brand} label={'Brand'}/>
                    <div bind:this={brandInput}>
                        {#if editMode}
                        <InputDisabled name={'brand'} bind:value={brand} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'brand'} placeholder={'e.g. Amaco'} bind:value={brand} 
                                removeErrorMessage={removeErrorMessage} updateFilteredItems={updateFilteredBrands} errorKeys={['brand', '_schema']}
                                state={brandState} filteredItems={filteredBrands} highlightedIndex={highlightedIndex} selectItem={_selectBrand} handleKeydown={handleKeydown}
                            />
                        {/if}
                    </div>
                    <ErrorMessageInput errors={errors.brand}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={idGroup}>
                    <LabelInput labelFor={brand_id} label={'ID'}/>
                    <div bind:this={idInput}>
                        {#if editMode}
                        <InputDisabled name={'brand_id'} bind:value={brand_id} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'brand_id'} placeholder={'e.g. C-1'} bind:value={brand_id} 
                                removeErrorMessage={removeErrorMessage} updateFilteredItems={updateFilteredIds} errorKeys={['brand_id', '_schema']}
                                state={idState} filteredItems={filteredIds} highlightedIndex={highlightedIndex} selectItem={selectId} handleKeydown={handleKeydown}
                            />
                        {/if}   
                    </div>
                    <ErrorMessageInput errors={errors.brand_id}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={nameGroup}>
                    <LabelInput labelFor={name} label={'Name'}/>
                    <div bind:this={nameInput}>
                        {#if editMode}
                        <InputDisabled name={'name'} bind:value={name} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'name'} placeholder={'e.g. Obsidian'} bind:value={name} 
                                removeErrorMessage={removeErrorMessage} updateFilteredItems={updateFilteredNames} errorKeys={['name', '_schema']}
                                state={nameState} filteredItems={filteredNames} highlightedIndex={highlightedIndex} selectItem={selectName} handleKeydown={handleKeydown}
                            />
                        {/if}   
                    </div>
                    <ErrorMessageInput errors={errors.name}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={colorGroup}>
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
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={coneGroup}>
                    <LabelInput labelFor={name} label={'Cone'}/>
                    <div bind:this={coneInput}>
                    <InputWithSearch name={'cone'} placeholder={'e.g. 5/6'} bind:value={cone} 
                                removeErrorMessage={removeErrorMessage} updateFilteredItems={updateFilteredCones} errorKeys={['cone']}
                                state={coneState} filteredItems={filteredCones} highlightedIndex={highlightedIndex} selectItem={selectCone} handleKeydown={handleKeydown}
                            />
                    </div>
                    <ErrorMessageInput errors={errors.cone}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={urlGroup}>
                    <LabelInput labelFor={glaze_url} label={'URL'}/>
                    <InputSearch name={'glaze_url'} className={'form-control'} placeholder={'https://'} bind:value={glaze_url} errorKey={'glaze_url'} removeErrorMessage={removeErrorMessage}/>
                    <ErrorMessageInput errors={errors.glaze_url}/>
                </div>
            </div>
        </div>
    </form>

</Modal>

<TableGlaze data={data.glazes} handleOnClickEdit={openModal} on:edit={handleEditClick} showPotColumn={true}/>



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
    .row{
        padding: 0;
    }
</style>