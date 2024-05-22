<script>
    import { API_URL } from '$lib/config';
    import Modal from '$lib/components/Modal.svelte';
    // import TableGlaze from '$lib/components/TableGlaze.svelte';
    import InputSearch from '$lib/components/forms/InputSearch.svelte';
    import InputNumber from '$lib/components/forms/InputNumber.svelte';
    import ErrorMessageInput from '$lib/components/forms/ErrorMessageInput.svelte';
    import LabelInput from '$lib/components/forms/LabelInput.svelte';
    import InputWithSearch from '$lib/components/forms/InputWithSearch.svelte';
    import InputDisabled from '$lib/components/forms/InputDisabled.svelte';
    // import ButtonTransparent from '$lib/components/ButtonTransparent.svelte';
    import { onMount } from 'svelte';
    import { _fetchGlazeList, _deleteGlaze, _fetchBrandList, _fetchGlazeData,
        _fetchGlazeFromBrandName, _fetchGlazeFromBrandId, _addGlaze } from './+page';
    import { _handleClickOutsideElement, _handleKeydown } from '$lib/utils';
    import { showModal, editMode, glazeId, glazeList } from '$lib/stores/glaze.js';
    import { _closeInputList } from '$lib/utils';
    
    onMount(async () => {
        dbBrandList = await _fetchBrandList();
    });

    let dialog;

    // State variables for form inputs
    $: formData = {
        brand: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        brand_id: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        name: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        color: {
            value: '',
            error: '',
            errorGroup: '',
        },
        temp_min: {
            value: '',
            error: '',
            errorGroup: '',
        },
        temp_max: {
            value: '',
            error: '',
            errorGroup: '',
        },
        cone: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        glaze_url: {
            value: '',
            error: '',
            errorGroup: '',
        }
    };

    let _schema = '';
    // let brand = '';
    // let brand_id = '';
    // let name = '';
    // let color = '';
    // let temp_min = '';
    // let temp_max = '';
    // let cone = '';
    // let glaze_url = '';

    let glazeData = {};
    $: if ($editMode) {
        fetchGlazeData();
        // ({brand, brand_id, name, color, temp_min, temp_max, cone, glaze_url} = $glazeData);
        for (let key in glazeData) {
            if (formData.hasOwnProperty(key)) {
                formData[key].value = glazeData[key];
            }
        }
    }
    async function fetchGlazeData(){
        glazeData = await _fetchGlazeData($glazeId);
    }

    // The list of error messages
    // let errors = { _schema: [], brand: [], brand_id: [], name: [], color: [], temp_min: [], temp_max: [], cone: [], glaze_url: [] };

    // List of form groups needed for binding for showing the errors
    let schemaGroup;
    // let brandGroup;
    // let nameGroup;
    // let idGroup;
    // let colorGroup;
    // let tempMinGroup;
    // let tempMaxGroup;
    // let coneGroup;
    // let urlGroup;

    // Variables for binding with the respective inputs and managing
    // the clicks outside of them
    // let brandInput;
    // let nameInput;
    // let idInput;
    // let coneInput;

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
    

    $: if (!$showModal && dialog) {
        resetValuesForm();
        $editMode = false;
    }

    // The states for handling keydowns
    $: brandState = {
        filteredItems: filteredBrands,
        highlightedIndex,
        selectItem: selectBrand,
        closeList: closeBrandList
    }

    $: nameState = {
        filteredItems: filteredNames,
        highlightedIndex,
        selectItem: selectName,
        closeList: closeIdList
    }

    $: idState = {
        filteredItems: filteredIds,
        highlightedIndex,
        selectItem: selectId,
        closeList: closeNameList
    }

    $: coneState = {
        filteredItems: filteredCones,
        highlightedIndex,
        selectItem: selectCone,
        closeList: closeConeList
    }


    // Close the dropdowns on brand and name when the focus/click is not on the 
    // respective input
    function handleClickOutsideInput(event) {
        const inputElements = [formData.brand.element, formData.brand_id.element, formData.name.element, formData.cone.element];
        const closeFunctions = [closeBrandList, closeIdList, closeNameList, closeConeList];
        _handleClickOutsideElement(event, inputElements, closeFunctions);
    }

    function handleKeydown(event, state) {
        highlightedIndex = _handleKeydown(event, state, highlightedIndex);
    }
    
    function updateFilteredBrands() {
        filteredBrands = dbBrandList.filter(brandFromList => brandFromList.toLowerCase().includes(formData.brand.value.toLowerCase()));
    }

    function updateFilteredIds() {
        if (formData.brand.value != '') {
            filteredIds = dbIdsList.filter(idFromList => idFromList.toLowerCase().includes(formData.brand_id.value.toLowerCase()));
        } else {
            filteredIds = [];
        }
    }

    function updateFilteredNames() {
        if (formData.brand.value != '') {
            filteredNames = dbNamesList.filter(nameFromList => nameFromList.toLowerCase().includes(formData.name.value.toLowerCase()));
        } else {
            filteredNames = [];
        }
    }

    function updateFilteredCones() {
        filteredCones = dbConesList.filter(coneFromList => coneFromList.toLowerCase().includes(formData.cone.value.toLowerCase()));
    }

    function closeBrandList() {
        [filteredBrands, highlightedIndex] = _closeInputList(filteredBrands, highlightedIndex)
    }

    function closeNameList() {      
        [filteredNames, highlightedIndex] = _closeInputList(filteredNames, highlightedIndex);
    }

    function closeIdList() {
        [filteredIds, highlightedIndex] = _closeInputList(filteredIds, highlightedIndex);
    }

    function closeConeList() {
        [filteredCones, highlightedIndex] = _closeInputList(filteredCones, highlightedIndex);
    }

    function removeErrorMessage(fieldKey) {
        errors[fieldKey] = [];
    }

    function resetValuesForm() {
        _schema = '';
        for (let key in formData) {
            if (!$editMode && (key === 'brand' || key === 'brand_id' || key === 'name')) {
                formData[key].value = '';
            }
            formData[key].value = '';
        }
        Object.keys(errors).forEach(key => {
            removeErrorMessage(key);
        });
        errors = { ...errors };
    }
    
    function focusOnError(firstError) {
        const errorTargetMap = {
            '_schema': schemaGroup,
            'brand': formData.brand.errorGroup,
            'brand_id': formData.brand_id.errorGroup,
            'name': formData.name.errorGroup,
            'color': formData.color.errorGroup,
            'temp_min': formData.temp_min.errorGroup,
            'temp_max': formData.temp_max.errorGroup,
            'cone': formData.cone.errorGroup,
            'glaze_url': formData.glaze_url.errorGroup
        };

        let target = errorTargetMap[firstError];

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
        formData.name.value = nameItem;
        closeNameList();

        glazeData = await _fetchGlazeFromBrandName(formData.brand.value, formData.name.value);
        for (let key in glazeData) {
            if (formData.hasOwnProperty(key)) {
                formData[key].value = glazeData[key];
            }
        }

    }

    async function selectId(idItem) {
        formData.brand_id.value = idItem;
        closeIdList();

        glazeData = await _fetchGlazeFromBrandId(formData.brand.value, formData.brand_id.value);
        for (let key in glazeData) {
            if (formData.hasOwnProperty(key)) {
                formData[key].value = glazeData[key];
            }
        }
    }

    function selectCone(coneItem) {
        formData.cone.value = coneItem;
        closeConeList();
    }

    async function handleSubmit() {
        let response;
        if (!$editMode){
            response = await fetch(`${API_URL}/api/add_glaze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    brand, brand_id, name, color, temp_min, temp_max, cone, glaze_url
                })
            });
        } else {
            response = await fetch(`${API_URL}/api/update_glaze/${$glazeId}`, {
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
            $showModal = false;
            
            $glazeList = await _fetchGlazeList();

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

    

    async function selectBrand(brandItem) {
        brand = brandItem;
        closeBrandList();

        let encodedBrand = encodeURIComponent(brand);

        const response_ids = await fetch(`${API_URL}/api/glaze_ids/${encodedBrand}`);
        if (response_ids.ok) {
            dbIdsList = await response_ids.json();
        }

        const response_names = await fetch(`${API_URL}/api/glaze_names/${encodedBrand}`);
        if (response_names.ok) {
            dbNamesList = await response_names.json();
        }
    }

    async function handleDeleteGlaze() {
        try{
            await _deleteGlaze($glazeId);
            $glazeData = await _fetchGlazeList();
            $showModal = false;
            dbBrandList = await _fetchBrandList();
        } catch (error) {
            _schema = error.message;
            console.log(`Error: ${_schema}`);
        }
    }


</script>

<svelte:head>
    <title>List of glazes</title>
</svelte:head>


<slot name="title"/>

<slot name="addButton" />


<Modal 
    bind:show={$showModal}
    bind:dialog 
    modalTitle="{$editMode ? 'Edit glaze' : 'Add a new glaze'}" 
    submitText="{$editMode ? 'Update glaze' : 'Add glaze'}" 
    on:submit={handleSubmit} 
    on:resetValues={resetValuesForm} 
    on:click={handleClickOutsideInput} 
    on:focus={handleClickOutsideInput}
    edit={$editMode}
    deleteBtnLabel={'Delete glaze'}
    handleDelete={handleDeleteGlaze}
>

    <form on:submit|preventDefault method='POST'>
        <div class="container" bind:this={schemaGroup}>
            <div class="row">
                <ErrorMessageInput errors={errors._schema}/>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.brand.errorGroup}>
                    <LabelInput labelFor={formData.brand.value} label={'Brand'}/>
                    <div bind:this={formData.brand.element}>
                        {#if $editMode}
                        <InputDisabled name={'brand'} bind:value={formData.brand.value} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'brand'} placeholder={'e.g. Amaco'} bind:value={formData.brand.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredBrands} errorKeys={['brand', '_schema']}
                                state={brandState} filteredItems={filteredBrands} {highlightedIndex} selectItem={selectBrand} {handleKeydown}
                            />
                        {/if}
                    </div>
                    <ErrorMessageInput errors={errors.brand}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.brand_id.errorGroup}>
                    <LabelInput labelFor={formData.brand_id.value} label={'ID'}/>
                    <div bind:this={formData.brand_id.element}>
                        {#if $editMode}
                        <InputDisabled name={'brand_id'} bind:value={formData.brand_id.value} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'brand_id'} placeholder={'e.g. C-1'} bind:value={formData.brand_id.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredIds} errorKeys={['brand_id', '_schema']}
                                state={idState} filteredItems={filteredIds} {highlightedIndex} selectItem={selectId} {handleKeydown}
                            />
                        {/if}   
                    </div>
                    <ErrorMessageInput errors={errors.brand_id}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.name.errorGroup}>
                    <LabelInput labelFor={formData.name.value} label={'Name'}/>
                    <div bind:this={formData.name.element}>
                        {#if $editMode}
                        <InputDisabled name={'name'} bind:value={formData.name.value} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'name'} placeholder={'e.g. Obsidian'} bind:value={formData.name.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredNames} errorKeys={['name', '_schema']}
                                state={nameState} filteredItems={filteredNames} {highlightedIndex} selectItem={selectName} {handleKeydown}
                            />
                        {/if}   
                    </div>
                    <ErrorMessageInput errors={errors.name}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.color.errorGroup}>
                    <LabelInput labelFor={formData.color.value} label={'Color'}/>
                    <InputSearch name={'color'} className={'form-control'} placeholder={'e.g. Yellow with spots'} bind:value={formData.color.value} errorKey={'color'} {removeErrorMessage}/>
                    <ErrorMessageInput errors={errors.color}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_min.errorGroup}>
                    <LabelInput labelFor={formData.temp_min.value} label={'Min. temp.'}/>
                    <InputNumber name={'temp_min'} className={'form-control'} placeholder={''} bind:value={formData.temp_min.value} errorKey={'temp_min'} {removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={errors.temp_min}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_max.errorGroup}>
                    <LabelInput labelFor={formData.temp_max.value} label={'Max. temp.'}/>
                    <InputNumber name={'temp_max'} className={'form-control'} placeholder={''} bind:value={formData.temp_max.value} errorKey={'temp_max'} {removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={errors.temp_max}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.cone.errorGroup}>
                    <LabelInput labelFor={formData.cone.value} label={'Cone'}/>
                    <div bind:this={formData.cone.element}>
                    <InputWithSearch name={'cone'} placeholder={'e.g. 5/6'} bind:value={formData.cone.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredCones} errorKeys={['cone']}
                                state={coneState} filteredItems={filteredCones} {highlightedIndex} selectItem={selectCone} {handleKeydown}
                            />
                    </div>
                    <ErrorMessageInput errors={errors.cone}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.glaze_url.errorGroup}>
                    <LabelInput labelFor={formData.glaze_url.value} label={'URL'}/>
                    <InputSearch name={'glaze_url'} className={'form-control'} placeholder={'https://'} bind:value={formData.glaze_url.value} errorKey={'glaze_url'} {removeErrorMessage}/>
                    <ErrorMessageInput errors={errors.glaze_url}/>
                </div>
            </div>
        </div>
    </form>

</Modal>

<slot/>


<style>

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