<script>
    // Svelte components
    import { onMount } from 'svelte';
    import Modal from '$lib/components/Modal.svelte';
    import InputSearch from '$lib/components/forms/InputSearch.svelte';
    import InputNumber from '$lib/components/forms/InputNumber.svelte';
    import ErrorMessageInput from '$lib/components/forms/ErrorMessageInput.svelte';
    import LabelInput from '$lib/components/forms/LabelInput.svelte';
    import InputWithSearch from '$lib/components/forms/InputWithSearch.svelte';
    import InputDisabled from '$lib/components/forms/InputDisabled.svelte';

    // API calls
    import { _fetchGlazeList, _deleteGlaze, _fetchBrandList, _fetchGlazeData,
        _fetchGlazeFromBrandName, _fetchGlazeFromBrandId,
        _fetchBrandGlazeIds, _fetchBrandGlazeNames, 
        _updateGlaze, _addGlaze} from '../../routes/glaze/+page.js';

    // Helper functions
    import { _handleClickOutsideElement, _handleKeydown, _closeInputList } from '$lib/utils';

    // Stores
    import { showModal, editMode, glazeId, glazeList } from '$lib/stores/glaze.js';

    // Props



    let dialog;
    $: if (!$showModal && dialog) {
        resetValuesForm();
        $editMode = false;
        $glazeId = '';
    }

    // State variables for form inputs
    $: formData = {
        schema: {
            error: '',
            errorGroup: '',
        },
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


    // Close the dropdowns when the focus/click is not on the 
    // respective input
    function handleClickOutsideInput(event) {
        const inputElements = [formData.brand.element, formData.brand_id.element, formData.name.element, formData.cone.element];
        const closeFunctions = [closeBrandList, closeIdList, closeNameList, closeConeList];
        _handleClickOutsideElement(event, inputElements, closeFunctions);
    }


    // Index of the currently highlighted element in the list: for brand and id inputs
    let highlightedIndex = -1;
    function handleKeydown(event, state) {
        highlightedIndex = _handleKeydown(event, state, highlightedIndex);
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


    // Reset the modal form values
    function resetValuesForm() {
        for (let key in formData) {
            if (!$editMode && (key === 'brand' || key === 'brand_id' || key === 'name')) {
                formData[key].value = '';
            }
            formData[key].value = '';
            formData[key].error = '';
        }
    }

    // Remove error message from the input field
    function removeErrorMessage(fieldKey) {
        formData[fieldKey].error = '';
    }

    // Focus on the first input field with an error
    function focusOnError(target) {

        if(dialog && target) {

            const modalRect = dialog.getBoundingClientRect();
            const targetRect = target.getBoundingClientRect();

            // Calculate relative position of the target element within the modal
            const relativeTop = targetRect.top - modalRect.top;

            // Scroll to the element
            dialog.scrollTop = dialog.scrollTop + relativeTop;

        }
    }


    // Fetching the whole list of brands from the DB
    let dbBrandList = [];
    onMount(async () => {
        dbBrandList = await _fetchBrandList();
        console.log(dbBrandList);
    });

    // Filter the brands on input and save them in a list
    // Drop-down list for the brand input is created when the user enters a brand name
    let filteredBrands = [];
    function updateFilteredBrands() {
        filteredBrands = dbBrandList.filter(brandFromList => brandFromList.toLowerCase().includes(formData.brand.value.toLowerCase()));
    }
    function closeBrandList() {
        [filteredBrands, highlightedIndex] = _closeInputList(filteredBrands, highlightedIndex);
    }
    async function selectBrand(brandItem) {
        formData.brand.value = brandItem;
        closeBrandList();

        dbIdsList = await _fetchBrandGlazeIds(brandItem);

        dbNamesList = await _fetchBrandGlazeNames(brandItem);

    }


    // The whole list of ids, based on the chosen brand
    let dbIdsList = [];
    // Filter the ids on input and save them in a list
    let filteredIds = [];
    function updateFilteredIds() {
        if (formData.brand.value != '') {
            filteredIds = dbIdsList.filter(idFromList => idFromList.toLowerCase().includes(formData.brand_id.value.toLowerCase()));
        } else {
            filteredIds = [];
        }
    }
    function closeIdList() {
        [filteredIds, highlightedIndex] = _closeInputList(filteredIds, highlightedIndex);
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


    // The whole list of names, based on the chosen brand
    let dbNamesList = [];
    // Filter the names on input and save them in a list
    let filteredNames = [];
    function updateFilteredNames() {
        if (formData.brand.value != '') {
            filteredNames = dbNamesList.filter(nameFromList => nameFromList.toLowerCase().includes(formData.name.value.toLowerCase()));
        } else {
            filteredNames = [];
        }
    }
    function closeNameList() {      
        [filteredNames, highlightedIndex] = _closeInputList(filteredNames, highlightedIndex);
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


    // The list of all the possible cone numbers
    let dbConesList = ['019', '018', '017', '016', '015', '014', '013', '012', '011',
            '010', '09', '08', '07', '06', '05', '04', '03', '02', '01',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
    // Filter the list of cones and save them a list
    let filteredCones = [];
    function updateFilteredCones() {
        filteredCones = dbConesList.filter(coneFromList => coneFromList.toLowerCase().includes(formData.cone.value.toLowerCase()));
    }
    function closeConeList() {
        [filteredCones, highlightedIndex] = _closeInputList(filteredCones, highlightedIndex);
    }
    function selectCone(coneItem) {
        formData.cone.value = coneItem;
        closeConeList();
    }


    // Edit mode: Fetching the glaze information and setting the form data in edit mode
    let glazeData = {};
    $: if ($editMode) {
        fetchGlazeData();
        for (let key in glazeData) {
            if (formData.hasOwnProperty(key)) {
                formData[key].value = glazeData[key];
            }
        }
    }
    async function fetchGlazeData(){
        glazeData = await _fetchGlazeData($glazeId);
    }


    async function handleSubmit() {
        
        let glazeFormData = {
            brand: formData.brand.value, brand_id: formData.brand_id.value, name: formData.name.value,
            color: formData.color.value, temp_min: formData.temp_min.value, temp_max: formData.temp_max.value,
            cone: formData.cone.value, glaze_url: formData.glaze_url.value
        };
        try {
            let response;

            if (!$editMode){
                response = await _addGlaze(glazeFormData);
            } else {
                response = await _updateGlaze($glazeId, glazeFormData);
            }
            const result = await response.json();
            console.log(result.message);

            resetValuesForm();
            $showModal = false;
            $glazeList = await _fetchGlazeList();

        } catch(error) {
            console.error(error.message);

            // Error logging
            if (error.message.includes('400')) {
                console.error('Client error occurred');
            } else if (error.message.includes('500')) {
                console.error('Server error occurred');
            }
            
            // Set the respective errors in the errors dict
            let errorMessages = error.message;

            let firstError = '';
            Object.keys(errorMessages).forEach(key => {
                    if(formData.hasOwnProperty(key)) {
                        formData[key].error = errorMessages[key];
                        if (firstError == '') {
                            firstError = formData[key].errorGroup;
                        };
                    }
                });
            console.log(firstError);
            focusOnError(firstError);
        }
    }


    // Handle the form submission on glaze deletion
    async function handleDeleteGlaze() {
        try{
            await _deleteGlaze($glazeId);
            glazeData = await _fetchGlazeList();
            $showModal = false;
            dbBrandList = await _fetchBrandList();
        } catch (error) {
            formData.schema.error = error.message;
            console.log(`Error: ${formData.schema.error}`);
        }
    }

</script>


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
        <div class="container" bind:this={formData.schema.errorGroup}>
            <div class="row">
                <ErrorMessageInput errors={formData.schema.error}/>
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
                    <ErrorMessageInput errors={formData.brand.error}/>
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
                    <ErrorMessageInput errors={formData.brand_id.error}/>
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
                    <ErrorMessageInput errors={formData.name.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.color.errorGroup}>
                    <LabelInput labelFor={formData.color.value} label={'Color'}/>
                    <InputSearch name={'color'} className={'form-control'} placeholder={'e.g. Yellow with spots'} bind:value={formData.color.value} errorKey={'color'} {removeErrorMessage}/>
                    <ErrorMessageInput errors={formData.color.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_min.errorGroup}>
                    <LabelInput labelFor={formData.temp_min.value} label={'Min. temp.'}/>
                    <InputNumber name={'temp_min'} className={'form-control'} placeholder={''} bind:value={formData.temp_min.value} errorKey={'temp_min'} {removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={formData.temp_min.error}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_max.errorGroup}>
                    <LabelInput labelFor={formData.temp_max.value} label={'Max. temp.'}/>
                    <InputNumber name={'temp_max'} className={'form-control'} placeholder={''} bind:value={formData.temp_max.value} errorKey={'temp_max'} {removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={formData.temp_max.error}/>
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
                    <ErrorMessageInput errors={formData.cone.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.glaze_url.errorGroup}>
                    <LabelInput labelFor={formData.glaze_url.value} label={'URL'}/>
                    <InputSearch name={'glaze_url'} className={'form-control'} placeholder={'https://'} bind:value={formData.glaze_url.value} errorKey={'glaze_url'} {removeErrorMessage}/>
                    <ErrorMessageInput errors={formData.glaze_url.error}/>
                </div>
            </div>
        </div>
    </form>

</Modal>

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