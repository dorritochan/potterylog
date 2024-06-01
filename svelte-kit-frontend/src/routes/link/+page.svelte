<script>
    import ButtonTransparent from "$lib/components/ButtonTransparent.svelte";
    import ModalFormLink from "$lib/components/ModalFormLink.svelte";
    import TableLink from "$lib/components/TableLink.svelte";

    // Stores
    import { showModal, editMode} from "$lib/stores/glaze.js";

    export let data;
    let linkList = data.linkList;
    console.log(linkList);

    function openModal(){
        $showModal = true;
    }

    function handleOnClickEdit(linkId) {
        $editMode = true;
        openModal();
        
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
    <ButtonTransparent handleOnClick={openModal} buttonText={'&plus; Add a new link'}/>
</div>

<TableLink {handleOnClickEdit} {linkList}/>

<ModalFormLink />