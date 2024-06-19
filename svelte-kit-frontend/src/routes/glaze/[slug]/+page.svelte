<script>
    import TableGlaze from '$lib/components/TableGlaze.svelte';
    import ModalFormGlaze from '$lib/components/ModalFormGlaze.svelte';
    import Title from '$lib/components/Title.svelte';
    import PotsListThumb from '$lib/components/PotsListThumb.svelte';

    import { showModal, editMode, glazeId } from '$lib/stores/glaze.js';

    export let data;
    let { glaze } = data;

    let title = `Glaze ${glaze.glaze_name}`;

    function openModal() {
        $editMode = false;
        $showModal = true;
    }

    function handleEditClick(glazeIdEvent) {
        $editMode = true;
        $glazeId = glazeIdEvent.detail;
        $showModal = true;
        console.log("Edit button clicked for glaze ID:", $glazeId);
    }
</script>

<svelte:head>
    <title>{ title }</title>
</svelte:head>

<Title {title}/>

<TableGlaze glazeList={[glaze]} on:edit={handleEditClick} showPotColumn={false}/>

<PotsListThumb pots={glaze.glazed_pots} itemType={'glaze'}/>

<ModalFormGlaze />

