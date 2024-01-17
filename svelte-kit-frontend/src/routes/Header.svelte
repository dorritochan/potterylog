<script lang="ts">
    import {
        Collapse,
        Navbar,
        NavbarToggler,
        NavbarBrand,
        Nav,
        NavItem,
        NavLink
    } from 'sveltestrap';

    let isOpen = false;

    function handleUpdate(event) {
        isOpen = event.detail.isOpen;
    }
</script>

<div class="navbar">
<Navbar light expand="md">
    <NavbarBrand href="/">
        <div class="m-2">
            <img src="/logo.svg" alt="Logo" class="logo">
            <span class="app-title">Pottery log</span><br>
            <span class="small-text">dorritochan pottery</span>
        </div>
    </NavbarBrand>

    <NavbarToggler on:click={() => (isOpen = !isOpen)} />

    <Collapse {isOpen} navbar expand="md" on:update={(event) => handleUpdate(event)}>
        <Nav navbar>
            <NavItem>
                <NavLink class="navitem" href="/glaze">Glazes</NavLink>
            </NavItem>
            <NavItem>
                <NavLink class="navitem" href="/clay">Clays</NavLink>
            </NavItem>
            <!--
            <NavItem>
                <Navlink href="/kilns">Kilns</Navlink>
            </NavItem>
            <NavItem>
                <Navlink href="/links">Links</Navlink>
            </NavItem>
            <NavItem>
                <Navlink href="/glazerecipes">Glaze recipes</Navlink>
            </NavItem>
            <NavItem>
                <Navlink href="/commissions">Commissions</Navlink>
            </NavItem>-->
        </Nav>
    </Collapse>
</Navbar>
</div>

<style>
    .logo{
        width: 2rem; 
        height: 2rem;
        filter: invert(100%) sepia(26%) saturate(4297%) hue-rotate(227deg) brightness(124%) contrast(111%);;
    }
    .app-title{
        color: #ffffff;
    }
    .navbar{
        background-color: transparent;
        display: block;
        -webkit-backdrop-filter: blur(5px);
        backdrop-filter: blur(5px);
    }
    .small-text {
        font-size: 15px;
        color: #ffffff;
    }
    :global(.navitem){
        color: white;
        text-shadow: 1px 1px 2px var(--main-color);
    }
    :global(.navitem):hover{
        color: var(--main-color);
    }
    :global(.navitem):focus{
        color: var(--main-color);
    }
    :global(.navitem):active{
        color: var(--main-color);
    }

</style>
