<script>
    import { Button } from "sveltestrap";
    import { createEventDispatcher } from "svelte";
    import { showModal, editMode } from "$lib/stores/glaze";

    export let show;
    $: $showModal = show;

    const dispatch = createEventDispatcher();

    export let modalTitle = 'Modal title';
    export let submitText = 'Submit text';

    export let edit;
    $: $editMode = edit;
    
    export let deleteBtnLabel;
    export let handleDelete;

    export let dialog; // HTMLDialogElement

    $: if ($showModal && dialog) {
        dialog.showModal();
    }
    $: if (!$showModal && dialog) {
        dialog.close();
    }
        

    function onSubmitButtonClick(){
        dispatch('submit');
    }

    function onResetButtonClick(){
        dispatch('resetValues');
    }

</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog 
    bind:this={dialog}
    on:close={() => show = false}
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="modal-dialog scroll-container" role="document" on:click|stopPropagation>
            <div class="modal-content">
                <!-- svelte-ignore a11y-autofocus -->
                <div class="modal-header" autofocus>
                    <h3 class="modal-title pl-3 pt-3 ml-3">
                        { modalTitle }
                    </h3>
                    <button on:click={() => dialog.close()} type="button" class="btn btn-outline-secondary">
                        <span aria-hidden="true">&minus;</span>
                    </button>
                </div>
                <br>
                <div class="modal-body">
                    <slot />
                </div>
                <br>
                <div class="container">
                    <div class="row justify-content-between">
                        <Button class="standard-btn primary col-12 col-md-4 p-2 p-md-2" type="submit" on:click={onSubmitButtonClick} color='primary'>
                            { submitText }
                        </Button>
                        <Button class="standard-btn col-12 col-md-4 p-2 p-md-2" type="secondary" outline on:click={onResetButtonClick} >
                            Reset values
                        </Button>
                    </div>
                    {#if editMode}
                    <div class="row justify-content-end mt-3 mb-3">
                        <Button class="standard-btn col-12 col-md-4 p-2 p-md-2" outline color="danger" on:click={handleDelete}>
                            {deleteBtnLabel}
                        </Button>
                    </div>
                    {/if}
                    <div class="row justify-content-end mt-3 mb-3">
                        <Button class="standard-btn secondary col-12 col-md-4 p-2 p-md-2" type="secondary" on:click={() => dialog.close()}>
                            Cancel
                        </Button>
                    </div>
                </div>
            </div>
        </div>
</dialog>



<style>
    dialog {
        width: 90%;
		max-width: 54em;
		border-radius: 0.6em;
		border: none;
        margin: auto; /* Center the modal */
        box-sizing: border-box; /* Include padding and border in the element's total width and height */
        display: none;
        background-color: rgba(255, 255, 255, 0.743);
        -webkit-backdrop-filter: blur(5px);
        backdrop-filter: blur(5px);
	}
    dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(2px);
	}
	dialog > div {
		padding: 1em;
        width: 50em;
        display: flex;
	}
	dialog[open] {
		animation: fly-in 0.5s;
        display: flex;
	}
	@keyframes fly-in {
		from {
			transform: translateY(10%);
            opacity: 0;
		}
		to {
			transform: translateY(0%);
            opacity: 1;
		}
	}
    @keyframes fly-out {
        from {
            transform: translateY(0%);
            opacity: 1;
        }
        to {
            transform: translateY(10%);
            opacity: 0;
        }
    }
	dialog[open]::backdrop {
		animation: fade 1s ease-out;
	} 
    @keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 3;
		}
	}
    /* Custom scrollbar styles */
    dialog::-webkit-scrollbar {
        width: 12px;
    }

    dialog::-webkit-scrollbar-thumb {
        background: #d4d4d4;
        border-radius: 10px;
        border: 2px solid white;
    }

    dialog::-webkit-scrollbar-thumb:hover {
        background: #7caef880;
    }
    :global(.standard-btn.primary) {
        box-shadow: 0px 6px 10px -5px #0d6efd;
    }
    :global(.standard-btn.secondary) {
        box-shadow: 0px 6px 10px -5px #666;
    }
</style>