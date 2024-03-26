// Function to update active link based on the current section.
function updateActiveLink(section) {
    // First, remove 'active' class from all links.
    document.querySelectorAll('#sidebarMenu .nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Then, add 'active' class to the link that matches the current section.
    const activeLink = document.querySelector(`#sidebarMenu .nav-link[href='#${section}']`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// Function to display the specified section and update the active link.
function showSection(sectionId) {
    // Hide all sections.
    document.querySelectorAll('.admin-section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the target section.
    const targetSection = document.querySelector(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
        // Extract the section name from the ID to update the active link.
        const sectionName = sectionId.replace('#', '');
        updateActiveLink(sectionName);
        // Save the active section to localStorage to remember it on page reload.
        localStorage.setItem('activeSection', sectionName);
    } else {
        console.error('Section does not exist:', sectionId);
    }
}

// Function to show the section based on URL, localStorage, or default.
function showSectionFromURLorStorage() {
    const urlParams = new URLSearchParams(window.location.search);
    const sectionFromURL = urlParams.get('section');
    const sectionFromStorage = localStorage.getItem('activeSection');
    const section = sectionFromURL || sectionFromStorage || 'cinemasSection';
    showSection(`#${section}`);
}

document.addEventListener('DOMContentLoaded', function() {
    showSectionFromURLorStorage();

    // Add click event listeners to sidebar links.
    document.querySelectorAll('#sidebarMenu .nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href');
            history.pushState(null, '', `?section=${sectionId.substring(1)}`);
            showSection(sectionId);
        });
    });

    // Handle back/forward browser navigation.
    window.addEventListener('popstate', showSectionFromURLorStorage);
});
