<script>

    import Footer from "$lib/components/layout/Footer.svelte";
    import Header from "$lib/components/layout/Header.svelte";

</script>

<Header />

<div class="main">
    <slot/>
</div>

<Footer />


<style>
    .main{
        flex: 1;
    }
</style>