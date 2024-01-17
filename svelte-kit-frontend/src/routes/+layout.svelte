<script>

    import Footer from "./Footer.svelte";
    import Header from "./Header.svelte";

</script>

<Header />
<slot class="wrapper" />
<Footer />


<style>
    .wrapper{
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }
</style>