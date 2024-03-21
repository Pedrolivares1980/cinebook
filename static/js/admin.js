document.addEventListener('DOMContentLoaded', function() {
    // Function to display the specified section and mark the corresponding navigation link as active.
    function showSectionFromURLorStorage() {
        // Attempt to get the section from the URL. If not present, use localStorage or default to 'cinemasSection'.
        const urlParams = new URLSearchParams(window.location.search);
        const sectionFromURL = urlParams.get('section');
        const sectionFromStorage = localStorage.getItem('activeSection');
        const section = sectionFromURL || sectionFromStorage || 'cinemasSection';
        showSection(`#${section}`);
        
        // Mark the corresponding navigation link as active.
        document.querySelectorAll('#sidebarMenu .nav-link').forEach(link => {
            if (link.getAttribute('href') === `#${section}`) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Function to hide all sections and show the target section.
    function showSection(sectionId) {
        document.querySelectorAll('.admin-section').forEach(section => {
            section.style.display = 'none';
        });
        const targetSection = document.querySelector(sectionId);
        if (targetSection) {
            targetSection.style.display = 'block';
            // Save the active section to localStorage to remember it on page reload.
            localStorage.setItem('activeSection', sectionId.substring(1));
        } else {
            console.error('Section does not exist:', sectionId);
        }
    }

    // Initially show the section from the URL or localStorage.
    showSectionFromURLorStorage();

    // Add event listeners to sidebar links to show sections and update URL without reloading the page.
    document.querySelectorAll('#sidebarMenu .nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href');
            history.pushState(null, '', `?section=${sectionId.substring(1)}`); // Update URL without reloading
            showSection(sectionId);
        });
    });

    // Listen to popstate event to handle back/forward browser navigation.
    window.addEventListener('popstate', showSectionFromURLorStorage);
});
