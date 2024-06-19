<script>
    // Components
    import TableGlaze from '$lib/components/TableGlaze.svelte';
    import ButtonTransparent from '$lib/components/ButtonTransparent.svelte';
    import ModalFormGlaze from '$lib/components/ModalFormGlaze.svelte';
    import Title from '$lib/components/Title.svelte';

    // Stores
    import { showModal, editMode, glazeId, glazeList } from '$lib/stores/glaze.js';

    // Variables
    let title = 'List of glazes';
    
    // The glaze list from the DB
    export let data;
    $glazeList = data.glazeList;

    // Open the modal in the add mode
    function openModal(){
        $editMode = false;
        $showModal = true;
    }

    // Handle the edit button click on a glaze row
    async function handleEditClick(glazeIdEvent) {
        $editMode = true;
        $glazeId = glazeIdEvent.detail;
        $showModal = true;
        console.log("Edit button clicked for glaze ID:", $glazeId);
    }

</script>

<svelte:head>
    <title>{title}</title>
</svelte:head>


<Title {title}/>

<ButtonTransparent on:click={openModal} buttonText={'&plus; Add a new glaze'}/>

<TableGlaze glazeList={$glazeList} on:edit={handleEditClick} showPotColumn={true}/>

<ModalFormGlaze />

