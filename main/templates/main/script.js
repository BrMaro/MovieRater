document.addEventListener('DOMContentLoaded', () => {
    const moviesSection = document.querySelector('.movies');
    moviesSection.textContent += "Test";
    fetch('/api/movies/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(movies_list => {
            movies_list.forEach(movie => {
                const movieCard = document.createElement('div'); // Create the movieCard element inside the loop
                movieCard.classList.add('movie-card');

                movieCard.innerHTML = `
                    <img src="${movie.poster_url}" alt="${movie.title} Poster">
                    <div class="overlay">
                        <h3>${movie.title}</h3>
                        <p>${movie.overview.substring(0, 100)}...</p>
                    </div>
                `;

                moviesSection.appendChild(movieCard); // Append the movieCard to the moviesSection
            });
        })
        .catch(error => {
            console.error("Error fetching movies:", error);
            moviesSection.innerHTML = `<p>Error fetching movies: ${error.message}</p>`;
        });
});
