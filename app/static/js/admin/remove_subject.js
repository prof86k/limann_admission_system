export function deleteItem(deleteItems, itemIds, url) {
    for (const key in deleteItems) {
        if (Object.hasOwnProperty.call(deleteItems, key)) {
            const element = deleteItems[key];
            element.addEventListener('click', function() {
                let result = confirm('Erase Record?');
                if (result == true) {
                    element.href = url + itemIds[key].value;
                }
            })
        }
    }
}