<script>
    import { createEventDispatcher } from "svelte";
    let dispatch = createEventDispatcher();

    export let data = [];
    export let handleOnClickEdit;
    function handleClickEdit(glazeIdEvent){
        handleOnClickEdit();
        dispatch('edit', glazeIdEvent);
    }
    export let showPotColumn;
</script>

<div class="table-container">
    <table>
        <thead>
            <tr>
                {#if showPotColumn}
                <th>View pots</th>
                {/if}
                <th>Brand</th>
                <th>ID</th>
                <th>Name</th>
                <th>Color</th>
                <th>Min °C</th>
                <th>Max °C</th>
                <th>Cone</th>
                <th style="padding: 8px 13px;">URL</th>
                <th>Edit</th>
            </tr>
        </thead>
        <tbody>
            {#each data as glaze}
            <tr>
                {#if showPotColumn}
                <td>
                    <a href="glaze/{ glaze.id }" class="hover-border-link">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-cup" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M.11 3.187A.5.5 0 0 1 .5 3h13a.5.5 0 0 1 .488.608l-.22.991a3.001 3.001 0 0 1-1.3 5.854l-.132.59A2.5 2.5 0 0 1 9.896 13H4.104a2.5 2.5 0 0 1-2.44-1.958L.012 3.608a.5.5 0 0 1 .098-.42Zm12.574 6.288a2 2 0 0 0 .866-3.899l-.866 3.9ZM1.124 4l1.516 6.825A1.5 1.5 0 0 0 4.104 12h5.792a1.5 1.5 0 0 0 1.464-1.175L12.877 4H1.123Z"/>
                        </svg>
                    </a>
                </td>
                {/if}
                <td>{ glaze.brand || '' }</td>
                <td>{ glaze.brand_id || '' }</td>
                <td>{ glaze.name || '' }</td>
                <td>{ glaze.color || '' }</td>
                <td>{ glaze.temp_min !== null ? glaze.temp_min + '°C' : ''}</td>
                <td>{ glaze.temp_max !== null ? glaze.temp_max + '°C' : '' }</td>
                <td>{ glaze.cone || '' }</td>
                <td>
                    {#if glaze.glaze_url }
                        <a class="hover-border-link" href="{ glaze.glaze_url || '' }" target="_blank">
                            <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 512 512" fill="currentColor">
                                <!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
                                <path d="M352 256c0 22.2-1.2 43.6-3.3 64H163.3c-2.2-20.4-3.3-41.8-3.3-64s1.2-43.6 3.3-64H348.7c2.2 20.4 3.3 41.8 3.3 64zm28.8-64H503.9c5.3 20.5 8.1 41.9 8.1 64s-2.8 43.5-8.1 64H380.8c2.1-20.6 3.2-42 3.2-64s-1.1-43.4-3.2-64zm112.6-32H376.7c-10-63.9-29.8-117.4-55.3-151.6c78.3 20.7 142 77.5 171.9 151.6zm-149.1 0H167.7c6.1-36.4 15.5-68.6 27-94.7c10.5-23.6 22.2-40.7 33.5-51.5C239.4 3.2 248.7 0 256 0s16.6 3.2 27.8 13.8c11.3 10.8 23 27.9 33.5 51.5c11.6 26 20.9 58.2 27 94.7zm-209 0H18.6C48.6 85.9 112.2 29.1 190.6 8.4C165.1 42.6 145.3 96.1 135.3 160zM8.1 192H131.2c-2.1 20.6-3.2 42-3.2 64s1.1 43.4 3.2 64H8.1C2.8 299.5 0 278.1 0 256s2.8-43.5 8.1-64zM194.7 446.6c-11.6-26-20.9-58.2-27-94.6H344.3c-6.1 36.4-15.5 68.6-27 94.6c-10.5 23.6-22.2 40.7-33.5 51.5C272.6 508.8 263.3 512 256 512s-16.6-3.2-27.8-13.8c-11.3-10.8-23-27.9-33.5-51.5zM135.3 352c10 63.9 29.8 117.4 55.3 151.6C112.2 482.9 48.6 426.1 18.6 352H135.3zm358.1 0c-30 74.1-93.6 130.9-171.9 151.6c25.5-34.2 45.2-87.7 55.3-151.6H493.4z"/>
                            </svg>
                        </a>
                    {/if}
                </td>
                <td>
                    <button class="hover-border-link" 
                        on:click={() => handleClickEdit(glaze.id)}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512" fill="currentColor">
                            <!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
                            <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 480.7c-2.5 8.4-.2 17.5 6.1 23.7s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.7 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 325.7 55.8 314.3 67.1l33.9 33.9 62.1 62.1 33.9 33.9 11.3-11.3 22.6-22.6 14.5-14.5c25-25 25-65.5 0-90.5L453.3 18.7c-25-25-65.5-25-90.5 0zm-47.4 168l-144 144c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6l144-144c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"/>
                        </svg>
                    </button>
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
</div>