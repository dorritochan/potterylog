<script>
    import { Button } from "sveltestrap";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let showModal; // boolean
    export let modalTitle = 'Modal title';
    export let submitText = 'Submit text';

    let dialog; // HTMLDialogElement

    $: if (showModal && dialog) dialog.showModal();

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
    on:close={() => showModal = false}
    on:click|self={() => dialog.close()}
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="modal-dialog" role="document" on:click|stopPropagation>
            <div class="modal-content">
                <!-- svelte-ignore a11y-autofocus -->
                <div class="modal-header" autofocus>
                    <h5 class="modal-title">
                        { modalTitle }
                    </h5>
                    <button on:click={() => dialog.close()} type="button" class="btn close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <br>
                <div class="modal-body p-2">
                    <slot />
                </div>
                <br>
                <div>
                    <div class="d-flex justify-content-between">
                        <Button class="standard-btn" type="submit" on:click={onSubmitButtonClick} color='primary'>
                            { submitText }
                        </Button>
                    </div>
                    <div class="d-flex justify-content-between">
                        <Button class="standard-btn" type="secondary" outline on:click={onResetButtonClick} >
                            Reset values
                        </Button>
                        <Button class="standard-btn" type="secondary" on:click={() => dialog.close()}>
                            Cancel
                        </Button>
                    </div>
                    <slot name="delete_button" />
                </div>
            </div>
        </div>
</dialog>



<style>
    dialog {
		max-width: 52em;
		border-radius: 0.6em;
		border: none;
		padding: 0;
	}
    dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
	}
	dialog > div {
		padding: 1em;
        width: 50em;
	}
	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes zoom {
		from {
			transform: scale(0.1);
		}
		to {
			transform: scale(1);
		}
	}
    dialog.closing {
        animation: zoomout 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes zoomout {
		from {
			transform: scale(1);
		}
		to {
			transform: scale(0.1);
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
</style>