    // Fetch the list of brands on click on brand input
    export async function _fetchBrandList(API_URL) {
        const response = await fetch(`${API_URL}/api/glaze_brands`);
        if (response.ok) {
            const brandList = await response.json();
            return brandList;
        }
    }
    
    // Fetching the list of glazes after deleting, adding, updating
    export async function _fetchGlazeList(API_URL) {

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

    export async function _deleteGlaze(API_URL, glazeId, _schema, data, showAddModal, dbBrandList){
        const response = await fetch(`${API_URL}/api/delete_glaze/${glazeId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorMessage = await response.json()
            _schema = errorMessage.message;
            console.log(`Error: ${_schema}`);
        } else {
            data.glazes = await _fetchGlazeList(API_URL);
            showAddModal = false;
            dbBrandList = await getBrandList();
        }
    }

    export async function _selectBrand(API_URL, brandItem, brand, closeBrandList, dbIdsList, dbNamesList) {
        brand = brandItem;
        closeBrandList();

        encodedBrand = encodeURIComponent(brand);

        const response_ids = await fetch(`${API_URL}/api/glaze_ids/${encodedBrand}`);
        if (response_ids.ok) {
            dbIdsList = await response_ids.json();
        }

        const response_names = await fetch(`${API_URL}/api/glaze_names/${encodedBrand}`);
        if (response_names.ok) {
            dbNamesList = await response_names.json();
        }
    }