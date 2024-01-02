<script>
    import { Button } from "sveltestrap";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let showModal; // boolean
    export let modalTitle = 'Modal title';
    export let submitText = 'Submit text';

    let dialog; // HTMLDialogElement

    $: if (showModal && dialog) dialog.showModal();

    function onButtonClick(){
        dispatch('submit');
    }

</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
    bind:this={dialog}
    on:close={() => showModal = false}
    on:click|self={() => dialog.close()}
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
    <div on:click|stopPropagation class="">
        <div class="modal-dialog" role="document">
            <div class="modal-content p-2">
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
                <div class="modal-body">
                    <slot />
                </div>
                <br>
                <div class="modal-footer align-baseline">
                    <div class="w-100">
                        <Button type="submit" on:click={onButtonClick}>
                            { submitText }
                        </Button>
                        <button on:click={() => dialog.close()} class="btn btn-secondary">Cancel</button>
                    </div>
                    <slot name="delete_button" />
                </div>
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