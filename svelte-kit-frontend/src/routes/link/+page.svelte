<script>
    import ButtonTransparent from "$lib/components/ButtonTransparent.svelte";
    import ModalFormLink from "$lib/components/ModalFormLink.svelte";
    import TableLink from "$lib/components/TableLink.svelte";

    // Stores
    import { showModal, editMode } from "$lib/stores/link.js";

    export let data;
    let linkList = data.linkList;
    console.log(linkList);

    function openModal(){
        $showModal = true;
    }

    let linkId;
    function handleClickEdit(linkId) {
        $editMode = true;
        linkId = linkId.detail;
        console.log("Edit button clicked for link ID:", linkId);
    }
</script>

<svelte:head>
    <title>Useful links</title>
</svelte:head>


<div name="title" class="m-3 page-title">
    <h1>
        Useful links
    </h1>
</div>

<div name="addButton" class="m-3 centered">
    <ButtonTransparent on:click={openModal} buttonText={'&plus; Add a new link'}/>
</div>

<TableLink on:edit={handleClickEdit} {openModal} {linkList}/>

<ModalFormLink />