<script>
    import { API_URL } from "$lib/config";
    import defaultCup from '$lib/images/default_mug.jpg';

    export let data;
    let glaze = data.glaze;

    // console.log(data);
    console.log(glaze.glazed_pots);

    const title = `Glaze ${glaze.glaze_name}`;
</script>

<svelte:head>
    <title>{ title }</title>
</svelte:head>

<h1 class="m-3">{ title }</h1>

<table class="table table-striped table-hover-color table-hover">
    <thead>
        <tr>
            <th>Brand</th>
            <th>ID</th>
            <th>Name</th>
            <th>Color</th>
            <th>Min. temp.</th>
            <th>Max. temp.</th>
            <th>Cone</th>
            <th style="padding: 8px 13px;">URL</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{ glaze.brand || '' }</td>
            <td>{ glaze.brand_id || '' }</td>
            <td>{ glaze.name || '' }</td>
            <td>{ glaze.color || '' }</td>
            <td>{ glaze.temp_min !== null ? glaze.temp_min + '°C' : '' }</td>
            <td>{ glaze.temp_max !== null ? glaze.temp_max + '°C' : '' }</td>
            <td>{ glaze.cone || '' }</td>
            <td>
                {#if glaze.glaze_url }
                    <a class="hover-border-link" href="{ glaze.glaze_url || '' }" target="_blank">
                        Website
                    </a>
                {/if}
            </td>
            <td>
                <button type="button" class="btn btn-outline-secondary" id="open-modal-edit-item-{ glaze.id }" data-toggle="modal" data-target="#modal-add-edit-glaze" data-reload-page="true" data-itemtype="glaze">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                        <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                    </svg>
                </button>
            </td>
        </tr>
    </tbody>
</table>

<h3 class="m-3">Pots used with this glaze</h3>
<div class="container-fluid">
    <div class="row">
        {#each glaze.glazed_pots as pot}
            <a href={`/pot/${pot.pot.id}`} class="col-md-2 link-image-label">
                <div class="image-container">
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