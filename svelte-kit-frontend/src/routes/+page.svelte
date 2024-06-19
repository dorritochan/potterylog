<script>
    export let data;
    import { API_URL } from '$lib/config';
    import defaultImage from '$lib/images/default_mug.jpg';
    import ButtonTransparent from '$lib/components/ButtonTransparent.svelte';
    import Title from '$lib/components/Title.svelte';
    import { goto } from '$app/navigation';
    
    console.log(data.pots);

    let pots = data.pots;

    // Helper function for the sort function, for the paths of type clay_type.id
    function getNestedValue(obj, path) {
        return path.split('.').reduce((o, p) => o ? o[p] : null, obj);
    }

    // Holds table sort state.  Initialized to reflect table sorted by id column ascending.
	let sortBy = {col: "id", descending: true};

    $: sort = (column) => {
        if (sortBy.col == column) {
            sortBy.descending = !sortBy.descending;
        } else {
            sortBy.col = column;
            sortBy.descending = true;
        }

        let sortModifier = (sortBy.descending) ? 1 : -1;

        let sort = (a, b) => {
            let aValue = getNestedValue(a, column);
            let bValue = getNestedValue(b, column);

            if (aValue < bValue) return -1 * sortModifier;
            if (aValue > bValue) return 1 * sortModifier;
            return 0;
        };

        pots = pots.sort(sort);

        update_sort_icons(column, sortBy.descending);
    }

    // Take care of the sorting icons
    let iconClassId = "fa-solid fa-sort-down";
    let iconClassThrowDate = "fa-solid fa-sort";
    let iconClassVesselType = "fa-solid fa-sort";
    let iconClassClayType = "fa-solid fa-sort";

    $: update_sort_icons = (column, descending) => {

        // Reset all icons to default
        iconClassId = "fa-solid fa-sort";
        iconClassThrowDate = "fa-solid fa-sort";
        iconClassVesselType = "fa-solid fa-sort";
        iconClassClayType = "fa-solid fa-sort";

        // Determine which column to change based on the column
        switch(column) {
            case 'id':
                iconClassId = descending ? "fa-solid fa-sort-up" : "fa-solid fa-sort-down";
                break;
            case 'throw_date':
                iconClassThrowDate = descending ? "fa-solid fa-sort-up" : "fa-solid fa-sort-down";
                break;
            case 'vessel_type':
                iconClassVesselType = descending ? "fa-solid fa-sort-up" : "fa-solid fa-sort-down";
                break;
            case 'clay_type.id':
                iconClassClayType = descending ? "fa-solid fa-sort-up" : "fa-solid fa-sort-down";
                break;
        }

    }

</script>

<svelte:head>
    <title>Pottery log: Home</title>
</svelte:head>

<Title title={'Pots'}/>

<ButtonTransparent on:click={() => goto('/pot')} buttonText={'&plus; Add a new pot'}/>


<table>
    <thead>
        <tr>
            <th on:click={sort("id")} class="sorting-column">
                ID
                <i class={iconClassId}></i>
            </th>
            <th>Image</th>
            <th on:click={sort("throw_date")} class="sorting-column">
                Throwing date
                <i class={iconClassThrowDate}></i>
            </th>
            <th on:click={sort("vessel_type")} class="sorting-column">
                Type
                <i class={iconClassVesselType}></i>
            </th>
            <th on:click={sort("clay_type.id")} class="sorting-column">
                Clay
                <i class={iconClassClayType}></i>
            </th>
            <th>Glazes</th>
        </tr>
    </thead>
    <tbody>
        {#each pots as pot}
            <tr>
                <td>{ pot.id }</td>
                <td>
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col p-0 image-container-index">
                                {#if pot.primary_image}
                                    <!-- Display the primary image -->
                                    <img src={`${API_URL}/static/photos/${pot.primary_image}`} alt="Pot" class="img-thumbnail img-fluid responsive-image">
                                {:else}
                                    <!-- Display a default image -->
                                    <img src={defaultImage} alt="DefaultCup" class="img-thumbnail img-fluid responsive-image">
                                {/if}
                            </div>  
                        </div>
                    </div>
                </td>
                <td>{ pot.throw_date }</td>
                <td>{ pot.vessel_type }</td>
                <td>
                    {#if pot.clay_type}
                    <a href={`/clay/${pot.clay_type.id}`} class="text-hover-effect">{ pot.clay_type.clay_name }</a>
                    {/if}
                </td>
                <td>
                    {#each pot.used_glazes as glaze}
                        <a href={`/glaze/${glaze.glaze.id}`} class="text-hover-effect">{ glaze.glaze.glaze_name }</a> <br>
                    {/each}
                </td>
            </tr>
        {/each}
    </tbody>
</table>
    

<style>
    .image-container-index{
        width: 120px;
        height: 120px;
        overflow: hidden;
    }
    .responsive-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }  


</style>
