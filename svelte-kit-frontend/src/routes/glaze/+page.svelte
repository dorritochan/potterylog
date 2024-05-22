<script>
    import { API_URL } from '$lib/config';
    import TableGlaze from '$lib/components/TableGlaze.svelte';
    import ButtonTransparent from '$lib/components/ButtonTransparent.svelte';
    import { showModal, editMode, glazeId, glazeList } from '$lib/stores/glaze.js';

    export let data;
    $glazeList  = data.glazeList;

    function openModal(){
        $showModal = true;
    }

    async function handleEditClick(glazeIdEvent) {

        $editMode = true;
        $glazeId = glazeIdEvent.detail;
        console.log("Edit button clicked for glaze ID:", $glazeId);

    }
</script>

<div name="title" class="m-3 page-title">
    <h1>
        List of glazes
    </h1>
</div>

<div name="addButton" class="m-3 centered">
    <ButtonTransparent handleOnClick={openModal} buttonText={'&plus; Add a new glaze'}/>
</div>

<TableGlaze glazeList={$glazeList} handleOnClickEdit={openModal} on:edit={handleEditClick} showPotColumn={true}/>
