    import { API_URL } from '$lib/config';
    
    // Fetch the list of brands on click on brand input
    export async function _fetchBrandList() {
        const response = await fetch(`${API_URL}/api/glaze_brands`);
        if (response.ok) {
            const brandList = await response.json();
            return brandList;
        }
    }
    
    // Fetching the list of glazes after deleting, adding, updating
    export async function _fetchGlazeList() {

        const response = await fetch(`${API_URL}/api/glazes`);

        if (!response.ok) {
            const errorBody = await response.json();
            console.log(`errorBody.message: ${errorBody.message}`);

            throw error(response.status, {
                message: errorBody.message
            })
        }

        const glazes = await response.json();
        return glazes;
    }

    // Delete a glaze from the database
    export async function _deleteGlaze(glazeId){
        const response = await fetch(`${API_URL}/api/delete_glaze/${glazeId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorMessage = await response.json()
            throw new Error(errorMessage.message);
        } 
    }

    export async function _fetchGlazeFromBrandName(brand, name){
        let encodedBrand = encodeURIComponent(brand);
        let encodedName = encodeURIComponent(name);

        const response = await fetch(`${API_URL}/api/glaze_from_name?brand=${encodedBrand}&name=${encodedName}`)

        if (!response.ok) {
            const errorMessage = await response.json()
            throw new Error(errorMessage.message);
        } else {
            const glaze = await response.json();
            return glaze;
        }
    }

    export async function _fetchGlazeFromBrandId(brand, brand_id){
        let encodedBrand = encodeURIComponent(brand);
        let encodedId = encodeURIComponent(brand_id);

        const response = await fetch(`${API_URL}/api/glaze_from_id?brand=${encodedBrand}&brand_id=${encodedId}`);

        if (!response.ok) {
            const errorMessage = await response.json()
            throw new Error(errorMessage.message);
        } else {
            const glaze = await response.json();
            return glaze;
        }
    }

    export async function _fetchBrandGlazeIds(brand){

        let encodedBrand = encodeURIComponent(brand);

        const response = await fetch(`${API_URL}/api/glaze_ids/${encodedBrand}`);

        if (!response.ok) {
            const errorMessage = await response.json()
            throw new Error(errorMessage.message);
        } else {
            const brandIdsList = await response.json();
            return brandIdsList;
        }
    }

    export async function _fetchBrandGlazeNames(brand){

        let encodedBrand = encodeURIComponent(brand);

        const response = await fetch(`${API_URL}/api/glaze_names/${encodedBrand}`);

        if (!response.ok) {
            const errorMessage = await response.json()
            throw new Error(errorMessage.message);
        } else {
            const brandNamesList = await response.json();
            return brandNamesList;
        }
    }

    export async function _fetchGlazeData(glazeId){

        const response = await fetch(`${API_URL}/api/glaze/${glazeId}`);

        if (response.ok) {
            let data = await response.json();
            return data;
        }
    }

    export async function _updateGlaze(glazeId, glazeData){
        try {
            const response = await fetch(`${API_URL}/api/update_glaze/${glazeId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(glazeData)
            });

            if (!response.ok) {
                const errorMessage = await response.json()
                throw new Error(`Error: ${errorMessage.message} (status: ${response.status})`);
            }

            return response;

        } catch (error) {
            console.error(`Failed to update glaze: ${error.message}`);
            throw error;
        }
    }

    export async function _addGlaze(glazeData) {
        try {
            const response = await fetch(`${API_URL}/api/add_glaze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(glazeData)
            });

            if (!response.ok) {
                const errorMessage = await response.json()
                throw new Error(`Error: ${errorMessage.message} (status: ${response.status})`);
            }

            return response;

        } catch (error) {
            console.error(`Failed to add glaze: ${error.message}`);
            throw error;
        }

        
    }