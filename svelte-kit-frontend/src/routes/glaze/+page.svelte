<script>
    // Components
    import TableGlaze from '$lib/components/TableGlaze.svelte';
    import ButtonTransparent from '$lib/components/ButtonTransparent.svelte';
    import ModalFormGlaze from '$lib/components/ModalFormGlaze.svelte';

    import { onMount } from 'svelte';

    // Stores
    import { showModal, editMode, glazeId, glazeList } from '$lib/stores/glaze.js';
    
    // The glaze list from the DB
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

</script>

<svelte:head>
    <title>List of glazes</title>
</svelte:head>



<div name="title" class="m-3 page-title">
    <h1>
        List of glazes
    </h1>
</div>

<div name="addButton" class="m-3 centered">
    <ButtonTransparent handleOnClick={openModal} buttonText={'&plus; Add a new glaze'}/>
</div>

<TableGlaze glazeList={$glazeList} handleOnClickEdit={openModal} on:edit={handleEditClick} showPotColumn={true}/>

<ModalFormGlaze />

