<script>
    import { API_URL } from '$lib/config';

    import TableGlaze from '$lib/components/TableGlaze.svelte';
    import ButtonTransparent from '$lib/components/ButtonTransparent.svelte';
    // import ModalFormGlaze from '$lib/components/ModalFormGlaze.svelte';

    import { onMount } from 'svelte';

    import { showModal, editMode, glazeId, glazeList } from '$lib/stores/glaze.js';
    

    export let data;
    $glazeList = data.glazeList;

    // Show the modal
    function openModal(){
        $showModal = true;
    }

    // Handle the edit button click on a glaze row
    async function handleEditClick(glazeIdEvent) {

        $editMode = true;
        $glazeId = glazeIdEvent.detail;
        console.log("Edit button clicked for glaze ID:", $glazeId);

    }
    



    // let _schema = '';
    // // let brand = '';
    // // let brand_id = '';
    // // let name = '';
    // // let color = '';
    // // let temp_min = '';
    // // let temp_max = '';
    // // let cone = '';
    // // let glaze_url = '';

    // let glazeData = {};
    // // $: if ($editMode) {
    // //     fetchGlazeData();
    // //     // ({brand, brand_id, name, color, temp_min, temp_max, cone, glaze_url} = $glazeData);
    // //     for (let key in glazeData) {
    // //         if (formData.hasOwnProperty(key)) {
    // //             formData[key].value = glazeData[key];
    // //         }
    // //     }
    // // }
    // // async function fetchGlazeData(){
    // //     glazeData = await _fetchGlazeData($glazeId);
    // // }

    // // The list of error messages
    // // let errors = { _schema: [], brand: [], brand_id: [], name: [], color: [], temp_min: [], temp_max: [], cone: [], glaze_url: [] };

    // // List of form groups needed for binding for showing the errors
    // let schemaGroup;
    // // let brandGroup;
    // // let nameGroup;
    // // let idGroup;
    // // let colorGroup;
    // // let tempMinGroup;
    // // let tempMaxGroup;
    // // let coneGroup;
    // // let urlGroup;

    // // Variables for binding with the respective inputs and managing
    // // the clicks outside of them
    // // let brandInput;
    // // let nameInput;
    // // let idInput;
    // // let coneInput;

    // // The whole list of brands from the DB
    // let dbBrandList = [];
    // // Filter the brands on input and save them in a list
    // let filteredBrands = [];
    // // Index of the currently highlighted element in the list: for brand and id inputs
    // let highlightedIndex = -1;
    // // The whole list of ids, based on the chosen brand
    // let dbIdsList = [];
    // // Filter the ids on input and save them in a list
    // let filteredIds = [];
    // // The whole list of names, based on the chosen brand
    // let dbNamesList = [];
    // // Filter the names on input and save them in a list
    // let filteredNames = [];
    // // The list of all the possible cone numbers
    // let dbConesList = ['019', '018', '017', '016', '015', '014', '013', '012', '011',
    //         '010', '09', '08', '07', '06', '05', '04', '03', '02', '01',
    //         '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
    // // Filter the list of cones and save them a list
    // let filteredCones = [];
    

    // // $: if (!$showModal && dialog) {
    // //     resetValuesForm();
    // //     $editMode = false;
    // // }

    // // The states for handling keydowns
    // $: brandState = {
    //     filteredItems: filteredBrands,
    //     highlightedIndex,
    //     selectItem: selectBrand,
    //     closeList: closeBrandList
    // }

    // $: nameState = {
    //     filteredItems: filteredNames,
    //     highlightedIndex,
    //     selectItem: selectName,
    //     closeList: closeIdList
    // }

    // $: idState = {
    //     filteredItems: filteredIds,
    //     highlightedIndex,
    //     selectItem: selectId,
    //     closeList: closeNameList
    // }

    // $: coneState = {
    //     filteredItems: filteredCones,
    //     highlightedIndex,
    //     selectItem: selectCone,
    //     closeList: closeConeList
    // }


    // // Close the dropdowns on brand and name when the focus/click is not on the 
    // // respective input
    // function handleClickOutsideInput(event) {
    //     const inputElements = [formData.brand.element, formData.brand_id.element, formData.name.element, formData.cone.element];
    //     const closeFunctions = [closeBrandList, closeIdList, closeNameList, closeConeList];
    //     _handleClickOutsideElement(event, inputElements, closeFunctions);
    // }

    // function handleKeydown(event, state) {
    //     highlightedIndex = _handleKeydown(event, state, highlightedIndex);
    // }
    
    // function updateFilteredBrands() {
    //     filteredBrands = dbBrandList.filter(brandFromList => brandFromList.toLowerCase().includes(formData.brand.value.toLowerCase()));
    // }

    // function updateFilteredIds() {
    //     if (formData.brand.value != '') {
    //         filteredIds = dbIdsList.filter(idFromList => idFromList.toLowerCase().includes(formData.brand_id.value.toLowerCase()));
    //     } else {
    //         filteredIds = [];
    //     }
    // }

    // function updateFilteredNames() {
    //     if (formData.brand.value != '') {
    //         filteredNames = dbNamesList.filter(nameFromList => nameFromList.toLowerCase().includes(formData.name.value.toLowerCase()));
    //     } else {
    //         filteredNames = [];
    //     }
    // }

    // function updateFilteredCones() {
    //     filteredCones = dbConesList.filter(coneFromList => coneFromList.toLowerCase().includes(formData.cone.value.toLowerCase()));
    // }

    // function closeBrandList() {
    //     [filteredBrands, highlightedIndex] = _closeInputList(filteredBrands, highlightedIndex)
    // }

    // function closeNameList() {      
    //     [filteredNames, highlightedIndex] = _closeInputList(filteredNames, highlightedIndex);
    // }

    // function closeIdList() {
    //     [filteredIds, highlightedIndex] = _closeInputList(filteredIds, highlightedIndex);
    // }

    // function closeConeList() {
    //     [filteredCones, highlightedIndex] = _closeInputList(filteredCones, highlightedIndex);
    // }

    // function removeErrorMessage(fieldKey) {
    //     errors[fieldKey] = [];
    // }

    // function resetValuesForm() {
    //     _schema = '';
    //     for (let key in formData) {
    //         if (!$editMode && (key === 'brand' || key === 'brand_id' || key === 'name')) {
    //             formData[key].value = '';
    //         }
    //         formData[key].value = '';
    //     }
    //     Object.keys(errors).forEach(key => {
    //         removeErrorMessage(key);
    //     });
    //     errors = { ...errors };
    // }
    
    // function focusOnError(firstError) {
    //     const errorTargetMap = {
    //         '_schema': schemaGroup,
    //         'brand': formData.brand.errorGroup,
    //         'brand_id': formData.brand_id.errorGroup,
    //         'name': formData.name.errorGroup,
    //         'color': formData.color.errorGroup,
    //         'temp_min': formData.temp_min.errorGroup,
    //         'temp_max': formData.temp_max.errorGroup,
    //         'cone': formData.cone.errorGroup,
    //         'glaze_url': formData.glaze_url.errorGroup
    //     };

    //     let target = errorTargetMap[firstError];

    //     if(dialog && target) {

    //         const modalRect = dialog.getBoundingClientRect();
    //         const targetRect = target.getBoundingClientRect();

    //         // Calculate relative position of the target element within the modal
    //         const relativeTop = targetRect.top - modalRect.top;

    //         // Scroll to the element
    //         dialog.scrollTop = dialog.scrollTop + relativeTop;

    //     }
    // }

    // async function selectName(nameItem) {
    //     formData.name.value = nameItem;
    //     closeNameList();

    //     glazeData = await _fetchGlazeFromBrandName(formData.brand.value, formData.name.value);
    //     for (let key in glazeData) {
    //         if (formData.hasOwnProperty(key)) {
    //             formData[key].value = glazeData[key];
    //         }
    //     }

    // }

    // async function selectId(idItem) {
    //     formData.brand_id.value = idItem;
    //     closeIdList();

    //     glazeData = await _fetchGlazeFromBrandId(formData.brand.value, formData.brand_id.value);
    //     for (let key in glazeData) {
    //         if (formData.hasOwnProperty(key)) {
    //             formData[key].value = glazeData[key];
    //         }
    //     }
    // }

    // function selectCone(coneItem) {
    //     formData.cone.value = coneItem;
    //     closeConeList();
    // }

    // async function handleSubmit() {
    //     let response;
    //     if (!$editMode){
    //         response = await fetch(`${API_URL}/api/add_glaze`, {
    //             method: 'POST',
    //             headers: { 'Content-Type': 'application/json' },
    //             body: JSON.stringify({ 
    //                 brand, brand_id, name, color, temp_min, temp_max, cone, glaze_url
    //             })
    //         });
    //     } else {
    //         response = await fetch(`${API_URL}/api/update_glaze/${$glazeId}`, {
    //             method: 'PUT',
    //             headers: { 'Content-Type': 'application/json' },
    //             body: JSON.stringify({
    //                 brand, brand_id, name, color, temp_min, temp_max, cone, glaze_url
    //             })
    //         });
    //     }

    //     if (response.ok) {
    //         const result = await response.json();
    //         console.log(result.message);
    //         resetValuesForm();
    //         $showModal = false;
            
    //         $glazeList = await _fetchGlazeList();

    //     } else {
    //         console.log(response.errors);
    //         const errorData = await response.json();

    //         // Client-side errors (e.g., 400 Bad Request)
    //         if (response.status >= 400 && response.status < 500) {
    //             console.error("Client error:", response.status);
    //             // Show error message to the user
    //             console.error(errorData.message);
                
    //             // Server-side errors (e.g., 500 Internal Server Error)
    //         } else if (response.status >= 500) {
    //             // Show generic error message to the user
    //             console.error("Server error:", response.status);
    //         }
            
    //         // Set the respective errors in the errors dict
    //         let errorsMessage = errorData.message;

    //         let firstError = '';
    //         Object.keys(errors).forEach(key => {
    //                 if(errorsMessage[key]) {
    //                     errors[key] = errorsMessage[key];
    //                     if (firstError == '') {
    //                         firstError = key;
    //                     };
    //                 }
    //             });
    //         console.log(firstError);
    //         focusOnError(firstError);
    //     }
    // }

    // async function selectBrand(brandItem) {
    //     brand = brandItem;
    //     closeBrandList();

    //     let encodedBrand = encodeURIComponent(brand);

    //     const response_ids = await fetch(`${API_URL}/api/glaze_ids/${encodedBrand}`);
    //     if (response_ids.ok) {
    //         dbIdsList = await response_ids.json();
    //     }

    //     const response_names = await fetch(`${API_URL}/api/glaze_names/${encodedBrand}`);
    //     if (response_names.ok) {
    //         dbNamesList = await response_names.json();
    //     }
    // }

    // async function handleDeleteGlaze() {
    //     try{
    //         await _deleteGlaze($glazeId);
    //         $glazeData = await _fetchGlazeList();
    //         $showModal = false;
    //         dbBrandList = await _fetchBrandList();
    //     } catch (error) {
    //         _schema = error.message;
    //         console.log(`Error: ${_schema}`);
    //     }
    // }


</script>

<svelte:head>
    <title>List of glazes</title>
</svelte:head>


<slot name="title"/>

<slot name="addButton" />

<slot/>


<div name="title" class="m-3 page-title">
    <h1>
        List of glazes
    </h1>
</div>

<div name="addButton" class="m-3 centered">
    <ButtonTransparent handleOnClick={openModal} buttonText={'&plus; Add a new glaze'}/>
</div>

<TableGlaze glazeList={$glazeList} handleOnClickEdit={openModal} on:edit={handleEditClick} showPotColumn={true}/>

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

