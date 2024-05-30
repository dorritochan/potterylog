<script>
    import { API_URL } from "$lib/config";
    import defaultCup from '$lib/images/default_mug.jpg';
    import TableGlaze from '$lib/components/TableGlaze.svelte'

    export let data;
    let { glaze } = data;

    const title = `Glaze ${glaze.glaze_name}`;

    function openModal() {

    }

    function handleEditClick() {

    }
</script>

<svelte:head>
    <title>{ title }</title>
</svelte:head>

<h1 class="m-3 page-title">{ title }</h1>

<TableGlaze glazeList={[glaze]} handleOnClickEdit={openModal} on:edit={handleEditClick} showPotColumn={false}/>

<h3 class="m-3 page-title">Pots used with this glaze</h3>
<div class="container-fluid">
    <div class="row">
        {#each glaze.glazed_pots as pot}
            <a href={`/pot/${pot.pot.id}`} class="col-md-2 link-image-label">
                <div>
                    {#if pot.pot.primary_image}
                        <img src={`${API_URL}/static/photos/${pot.pot.primary_image}`} alt="Pot" class="img-thumbnail img-fluid">
                    {:else}
                        <img src={defaultCup} alt="Default Cup" class="img-thumbnail img-fluid">
                    {/if}
                </div>
                { pot.pot.pot_name }
            </a>
        {/each}
    </div>
</div>

<style>
    .img-thumbnail{
        width: 14rem; 
        height: 8rem; 
        object-fit: cover;
    }
</style>