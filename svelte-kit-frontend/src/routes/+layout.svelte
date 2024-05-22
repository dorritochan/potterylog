<script>

    import Footer from "$lib/components/layout/Footer.svelte";
    import Header from "$lib/components/layout/Header.svelte";

</script>

<div class="wrapper-outer">
    <Header />
    <div class="wrapper-inner">
        <slot/>
    </div>
    <Footer />
</div>


<style>
    .wrapper-outer{
        position:relative; /* needed for footer positioning*/
        
        height:auto !important; /* real browsers */
        height:100%; /* IE6: treaded as min-height*/

        min-height:100%; /* real browsers */
    }
    .wrapper-inner{
        padding:1em 1em 5em; /* bottom padding for footer */
    }
</style>