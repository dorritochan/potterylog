<script>
    import { API_URL } from "$lib/config";
    import defaultCup from '$lib/images/default_mug.jpg';

    export let data;
    let clay = data.clay;

    console.log(clay);
</script>

<svelte:head>
    <title>Clay { clay.clay_name }</title>
</svelte:head>

<h1 class="m-3">Clay { clay.clay_name }</h1>

<table class="table table-striped">
    <thead>
        <tr>
            <th>Brand</th>
            <th>Name or ID</th>
            <th>Color</th>
            <th>Min. temp.</th>
            <th>Max. temp.</th>
            <th>Grog %</th>
            <th>Grog size</th>
            <th style="padding: 8px 13px;">URL</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{ clay.brand || '' }</td>
            <td>{ clay.name_id || '' }</td>
            <td>{ clay.color || '' }</td>
            <td>{ clay.temp_min !== null ? clay.temp_min + '°C' : ''}</td>
            <td>{ clay.temp_max !== null ? clay.temp_max + '°C' : '' }</td>
            <td>{ clay.grog_percent !== null ? clay.grog_percent + '%' : '' }</td>
            <td>{ clay.grog_size_max !== null ? clay.grog_size_max + 'mm' : '' }</td>
            <td>
                {#if clay.url }
                    <a class="hover-border-link" href="{ clay.url }" target="_blank">
                        Website
                    </a>
                {/if}
            </td>
            <td>
                <button type="button" class="btn btn-outline-secondary" id="open-modal-edit-item-{ clay.id }" data-toggle="modal" data-target="#modal-add-edit-clay" data-reload-page="true" data-itemtype="clay">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                        <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                    </svg>
                </button>
            </td>
        </tr>
    </tbody>
</table>

<h3 class="m-3">Pots used with this clay</h3>
<div class="container-fluid">
    <div class="row">
        {#each clay.pots as pot}
            <a href={`/pot/${pot.id}`} class="col-md-2 link-image-label">
                <div class="image-container">
                    {#if pot.primary_image}
                        <img src={`${API_URL}/static/photos/${pot.primary_image}`} alt="Pot" class="img-thumbnail img-fluid">
                    {:else}
                        <img src={defaultCup} alt="Default Cup" class="img-thumbnail img-fluid">
                    {/if}
                </div>
                { pot.pot_name }
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