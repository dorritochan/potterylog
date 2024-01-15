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


<Navbar color="light" light expand="md">
    <NavbarBrand href="/">
        <div class="m-2">
            <img src="/logo.png" alt="Logo" style="width: 2rem; height: 2rem;">
            <span>Pottery log</span><br>
            <span class="small-text">dorritochan pottery</span>
        </div>
    </NavbarBrand>

    <NavbarToggler on:click={() => (isOpen = !isOpen)} />

    <Collapse {isOpen} navbar expand="md" on:update={handleUpdate}>
        <Nav navbar>
            <NavItem>
                <NavLink href="/glaze">Glazes</NavLink>
            </NavItem>
            <NavItem>
                <NavLink href="/clay">Clays</NavLink>
            </NavItem>
            <!-- <NavItem>
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


<style>
    .small-text {
        font-size: 15px;
        color: rgb(176, 174, 174);
    }
</style>
