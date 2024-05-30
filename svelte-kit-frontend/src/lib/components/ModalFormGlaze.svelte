<script>
    import Modal from '$lib/components/Modal.svelte';
    import InputSearch from '$lib/components/forms/InputSearch.svelte';
    import InputNumber from '$lib/components/forms/InputNumber.svelte';
    import ErrorMessageInput from '$lib/components/forms/ErrorMessageInput.svelte';
    import LabelInput from '$lib/components/forms/LabelInput.svelte';
    import InputWithSearch from '$lib/components/forms/InputWithSearch.svelte';
    import InputDisabled from '$lib/components/forms/InputDisabled.svelte';

    import { _fetchGlazeList, _deleteGlaze, _fetchBrandList, _fetchGlazeData,
        _fetchGlazeFromBrandName, _fetchGlazeFromBrandId, _addGlaze } from './routes/glazes/+page.js';
    import { _handleClickOutsideElement, _handleKeydown, _closeInputList } from '$lib/utils';

    import { showModal, editMode, glazeId, glazeList } from '$lib/stores/glaze.js';

    let dialog;
    let dbBrandList = [];

    onMount(async () => {
        dbBrandList = await _fetchBrandList();
        console.log(dbBrandList);
    });

    // State variables for form inputs
    $: formData = {
        schema: {
            error: '',
            errorGroup: '',
        },
        brand: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        brand_id: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        name: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        color: {
            value: '',
            error: '',
            errorGroup: '',
        },
        temp_min: {
            value: '',
            error: '',
            errorGroup: '',
        },
        temp_max: {
            value: '',
            error: '',
            errorGroup: '',
        },
        cone: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        glaze_url: {
            value: '',
            error: '',
            errorGroup: '',
        }
    };

    let _schema = '';


</script>


<Modal 
    bind:show={$showModal}
    bind:dialog 
    modalTitle="{$editMode ? 'Edit glaze' : 'Add a new glaze'}" 
    submitText="{$editMode ? 'Update glaze' : 'Add glaze'}" 
    on:submit={handleSubmit} 
    on:resetValues={resetValuesForm} 
    on:click={handleClickOutsideInput} 
    on:focus={handleClickOutsideInput}
    edit={$editMode}
    deleteBtnLabel={'Delete glaze'}
    handleDelete={handleDeleteGlaze}
>

    <form on:submit|preventDefault method='POST'>
        <div class="container" bind:this={formData.schema.errorGroup}>
            <div class="row">
                <ErrorMessageInput errors={formData.schema.error}/>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.brand.errorGroup}>
                    <LabelInput labelFor={formData.brand.value} label={'Brand'}/>
                    <div bind:this={formData.brand.element}>
                        {#if $editMode}
                        <InputDisabled name={'brand'} bind:value={formData.brand.value} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'brand'} placeholder={'e.g. Amaco'} bind:value={formData.brand.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredBrands} errorKeys={['brand', '_schema']}
                                state={brandState} filteredItems={filteredBrands} {highlightedIndex} selectItem={selectBrand} {handleKeydown}
                            />
                        {/if}
                    </div>
                    <ErrorMessageInput errors={formData.brand.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.brand_id.errorGroup}>
                    <LabelInput labelFor={formData.brand_id.value} label={'ID'}/>
                    <div bind:this={formData.brand_id.element}>
                        {#if $editMode}
                        <InputDisabled name={'brand_id'} bind:value={formData.brand_id.value} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'brand_id'} placeholder={'e.g. C-1'} bind:value={formData.brand_id.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredIds} errorKeys={['brand_id', '_schema']}
                                state={idState} filteredItems={filteredIds} {highlightedIndex} selectItem={selectId} {handleKeydown}
                            />
                        {/if}   
                    </div>
                    <ErrorMessageInput errors={formData.brand_id.error}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.name.errorGroup}>
                    <LabelInput labelFor={formData.name.value} label={'Name'}/>
                    <div bind:this={formData.name.element}>
                        {#if $editMode}
                        <InputDisabled name={'name'} bind:value={formData.name.value} className={'form-control'}/>
                        {:else}
                            <InputWithSearch name={'name'} placeholder={'e.g. Obsidian'} bind:value={formData.name.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredNames} errorKeys={['name', '_schema']}
                                state={nameState} filteredItems={filteredNames} {highlightedIndex} selectItem={selectName} {handleKeydown}
                            />
                        {/if}   
                    </div>
                    <ErrorMessageInput errors={formData.name.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.color.errorGroup}>
                    <LabelInput labelFor={formData.color.value} label={'Color'}/>
                    <InputSearch name={'color'} className={'form-control'} placeholder={'e.g. Yellow with spots'} bind:value={formData.color.value} errorKey={'color'} {removeErrorMessage}/>
                    <ErrorMessageInput errors={formData.color.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_min.errorGroup}>
                    <LabelInput labelFor={formData.temp_min.value} label={'Min. temp.'}/>
                    <InputNumber name={'temp_min'} className={'form-control'} placeholder={''} bind:value={formData.temp_min.value} errorKey={'temp_min'} {removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={errors.temp_min.error}/>
                </div>
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_max.errorGroup}>
                    <LabelInput labelFor={formData.temp_max.value} label={'Max. temp.'}/>
                    <InputNumber name={'temp_max'} className={'form-control'} placeholder={''} bind:value={formData.temp_max.value} errorKey={'temp_max'} {removeErrorMessage} addOn={'°C'}/>
                    <ErrorMessageInput errors={formData.temp_max.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.cone.errorGroup}>
                    <LabelInput labelFor={formData.cone.value} label={'Cone'}/>
                    <div bind:this={formData.cone.element}>
                    <InputWithSearch name={'cone'} placeholder={'e.g. 5/6'} bind:value={formData.cone.value} 
                                {removeErrorMessage} updateFilteredItems={updateFilteredCones} errorKeys={['cone']}
                                state={coneState} filteredItems={filteredCones} {highlightedIndex} selectItem={selectCone} {handleKeydown}
                            />
                    </div>
                    <ErrorMessageInput errors={formData.cone.error}/>
                </div>
            </div>
            <div class="row">
                <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.glaze_url.errorGroup}>
                    <LabelInput labelFor={formData.glaze_url.value} label={'URL'}/>
                    <InputSearch name={'glaze_url'} className={'form-control'} placeholder={'https://'} bind:value={formData.glaze_url.value} errorKey={'glaze_url'} {removeErrorMessage}/>
                    <ErrorMessageInput errors={formData.glaze_url.error}/>
                </div>
            </div>
        </div>
    </form>

</Modal>