export function _handleClickOutsideElement(event, elements, closeFunctions) {
    for (let i = 0; i < elements.length; i++) {
        const isOutsideElement = !elements[i].contains(event.target);
        if (isOutsideElement) {
            closeFunctions[i]();
        }
    }
}

export function _handleKeydown(event, state, highlightedIndex) {
    let updatedHighlightedIndex = highlightedIndex;

    switch(event.key) {
        case 'ArrowDown':
            updatedHighlightedIndex = (updatedHighlightedIndex + 1) % state.filteredItems.length;
            break;
        case 'ArrowUp':
            updatedHighlightedIndex = (updatedHighlightedIndex - 1 + state.filteredItems.length) % state.filteredItems.length;
            break;
        case 'Enter':
            if (state.highlightedIndex >= 0) {
                state.selectItem(state.filteredItems[updatedHighlightedIndex]);
            }
            break;
        case 'Tab':
            state.closeList();
            break;
    }

    return updatedHighlightedIndex;
}

export function _closeInputList(list, index) {
    list.length = 0;
    index = -1;
    return [list, index];
}