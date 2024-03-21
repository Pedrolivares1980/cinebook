// filters.js
document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.getElementById('toggle-filters');
    const filterFormContainer = document.getElementById('filter-form-container');

    filterButton.addEventListener('click', function() {
        // Toggle the display of the filter form container
        const isDisplayed = filterFormContainer.style.display === 'block';
        filterFormContainer.style.display = isDisplayed ? 'none' : 'block';
    });
});
