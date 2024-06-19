<script>
    import Subtitle from "../Subtitle.svelte";
    import ErrorMessageInput from "./ErrorMessageInput.svelte";
    import LabelInput from "./LabelInput.svelte";
    import InputDisabled from "./InputDisabled.svelte";
    import InputWithSearch from "./InputDisabled.svelte";

    import { editMode, potData, potId } from "$lib/stores/pot.js";
    import InputSearch from "./InputSearch.svelte";

    // State variables for form inputs
    $: formData = {
        schema: {
            error: '',
            errorGroup: '',
        },
        author: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        vessel_type: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        },
        made_with_clay: {
            value: '',
            error: '',
            errorGroup: '',
            element: ''
        }
    };

    // Remove error message from the input field
    function removeErrorMessage(fieldKey) {
        formData[fieldKey].error = '';
    }
</script>

<form on:submit|preventDefault method='POST'>
    <div class="container" bind:this={formData.schema.errorGroup}>
        <div class="row">
            <ErrorMessageInput errors={formData.schema.error}/>
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.author.errorGroup}>
                <LabelInput labelFor={formData.author.value} label={'Author'}/>
                <div bind:this={formData.author.element}>
                    <InputSearch name={'author'} placeholder={'e.g. Dora'} className={'form-control'} value={formData.author.value} {removeErrorMessage} errorKey={'author'} />
                </div>
                <ErrorMessageInput errors={formData.author.error}/>
            </div>
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.vessel_type.errorGroup}>
                <LabelInput labelFor={formData.vessel_type.value} label={'Vessel type'}/>
                <div bind:this={formData.vessel_type.element}>
                    <InputSearch name={'vessel_type'} placeholder={'e.g. Mug, small'} className={'form-control'} value={formData.vessel_type.value} {removeErrorMessage} errorKey={'vessel_type'} />
                </div>
                <ErrorMessageInput errors={formData.vessel_type.error}/>
            </div>
        </div>
        <Subtitle  title={'Throwing'}/>
        <div class="row">
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.made_with_clay.errorGroup}>
                <LabelInput labelFor={formData.made_with_clay.value} label={'Clay'}/>
                <div bind:this={formData.made_with_clay.element}>
                    <InputSearch name={'made_with_clay'} placeholder={'e.g. Sibelco WMSB'} className={'form-control'} value={formData.made_with_clay.value} {removeErrorMessage} errorKey={'made_with_clay'} />
                </div>
                <ErrorMessageInput errors={formData.made_with_clay.error}/>
            </div>
        </div>
        <Subtitle  title={'Trimming'}/>
        <!-- <div class="row">
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.color.errorGroup}>
                
            </div>
        </div>-->
        <Subtitle  title={'Glazing'}/>
        <!--<div class="row">
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_min.errorGroup}>

            </div>
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.temp_max.errorGroup}>

            </div>
        </div>
        <div class="row">
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.cone.errorGroup}>

            </div>
        </div>
        <div class="row">
            <div class="form-group col-12 col-md-6 p-2 p-md-2" bind:this={formData.glaze_url.errorGroup}>

            </div>
        </div> -->
    </div>
</form>