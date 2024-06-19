<script>
    import { API_URL } from "$lib/config";
    import defaultCup from "$lib/images/default_mug.jpg";
    import Subtitle from "./Subtitle.svelte";

    export let pots = [];
    export let itemType = '';
</script>



<Subtitle title={'Pots used with this ' + itemType} />

<div class="container-fluid">
    <div class="row">
        {#each pots as pot}
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