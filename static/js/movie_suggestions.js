document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");

    // Selecting DOM elements
    const movieInput = document.getElementById('movie-name');
    const suggestionsBox = document.getElementById('movie-suggestions');
    const form = document.getElementById('movie-form');
    const tmdbIdInput = document.getElementById('id_tmdb_id');

    // Ensuring all elements are correctly selected
    if (!movieInput || !suggestionsBox || !form || !tmdbIdInput) {
        console.error("One or more elements could not be found:", {movieInput, suggestionsBox, form, tmdbIdInput});
        return;
    }

    // Function to fetch movie suggestions
    async function fetchSuggestions(query) {
        console.log("Fetching suggestions for:", query);
        const url = `/movies/suggestions/?query=${query}`;
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch suggestions');
            const data = await response.json();
            console.log("Suggestions received:", data);
            return data;
        } catch (error) {
            console.error("Error fetching suggestions:", error);
            return { results: [] };
        }
    }

    // Displaying suggestions
    function displaySuggestions(suggestions) {
        console.log("Displaying suggestions");
        suggestionsBox.innerHTML = '';
        suggestions.forEach(movie => {
            const suggestionItem = document.createElement('div');
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.textContent = movie.title;
            suggestionItem.dataset.tmdbId = movie.id;
            suggestionItem.addEventListener('click', () => selectMovie(movie.id, movie.title));
            suggestionsBox.appendChild(suggestionItem);
        });
    }

    // Fetching and displaying movie details
    async function fetchMovieDetails(tmdbId) {
        console.log("Fetching movie details for TMDB ID:", tmdbId);
        const apiKey = 'a461382033e324b0ce66c1ed513d3d38'; // Replace with your actual TMDB API key
        const url = `https://api.themoviedb.org/3/movie/${tmdbId}?api_key=${apiKey}&append_to_response=credits,videos`;
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch movie details');
            const details = await response.json();
            console.log("Movie details received:", details);
            return details;
        } catch (error) {
            console.error("Error fetching movie details:", error);
            return null;
        }
    }

    // Filling the form with movie details
    function fillFormWithMovieDetails(movieDetails) {
        console.log('Filling form with movie details:', movieDetails);
        
        if (!movieDetails) {
            console.error("No movie details provided");
            return;
        }
        
        // Building the complete URL for the poster image using the base URL provided by TMDb
        const posterBaseUrl = 'https://image.tmdb.org/t/p/w500';
        const posterUrl = movieDetails.poster_path ? `${posterBaseUrl}${movieDetails.poster_path}` : '';
        

        document.getElementById('id_title').value = movieDetails.title || 'N/A';
        document.getElementById('id_tmdb_id').value = movieDetails.id || 'N/A';
        document.getElementById('id_overview').value = movieDetails.overview || 'N/A';
        document.getElementById('id_release_date').value = movieDetails.release_date || 'N/A';
        
        // Use the constructed poster URL for the poster_path field
        document.getElementById('id_poster_path').value = posterUrl;
        
        document.getElementById('id_original_language').value = movieDetails.original_language || 'N/A';
        

        document.getElementById('id_director').value = getDirector(movieDetails) || 'N/A';
        document.getElementById('id_cast').value = getCast(movieDetails) || 'N/A';
        document.getElementById('id_user_rating').value = movieDetails.vote_average || 'N/A';
        document.getElementById('id_trailer_link').value = getTrailerLink(movieDetails) || 'N/A';
    }
    

    // Utility functions to extract director, cast, and trailer link
    function getDirector(movieDetails) {
        const director = movieDetails.credits.crew.find(member => member.job === 'Director');
        return director ? director.name : '';
    }

    function getCast(movieDetails) {
        const castList = movieDetails.credits.cast.map(member => member.name).join(', ');
        return castList;
    }

    function getTrailerLink(movieDetails) {
        const trailer = movieDetails.videos.results.find(video => video.type === 'Trailer');
        return trailer ? `https://www.youtube.com/watch?v=${trailer.key}` : '';
    }

    // Listening for user input to fetch suggestions
    movieInput.addEventListener('input', async () => {
        const query = movieInput.value.trim();
        if (query.length >= 3) {
            const data = await fetchSuggestions(query);
            displaySuggestions(data.results);
        } else {
            suggestionsBox.innerHTML = '';
        }
    });

    // Handling movie selection
    async function selectMovie(tmdbId, title) {
        console.log("Movie selected:", title, "with TMDB ID:", tmdbId);
        movieInput.value = title; // Update the input with the movie title
        tmdbIdInput.value = tmdbId; // Store the TMDB ID in the hidden input
        suggestionsBox.innerHTML = ''; // Clear suggestions
        const movieDetails = await fetchMovieDetails(tmdbId);
        fillFormWithMovieDetails(movieDetails);
    }

    // Preventing form submission without a selected movie
    form.addEventListener('submit', function(event) {
        if (!tmdbIdInput.value) {
            event.preventDefault(); // Stop form submission
            alert('Please select a movie from the suggestions.');
        }
    });
});
