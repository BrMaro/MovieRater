// script.js

// Simulated data of top rated movies
const topRatedMovies = [
    { title: "The Shawshank Redemption", rating: 9.3 },
    { title: "The Godfather", rating: 9.2 },
    { title: "The Dark Knight", rating: 9.0 }
];

// Function to render movie cards
function renderMovies() {
    const moviesSection = document.getElementById('movies');
    moviesSection.innerHTML = '<h2>Top Rated Movies</h2>';
    topRatedMovies.forEach(movie => {
        const movieCard = document.createElement('div');
        movieCard.classList.add('movie-card');
        movieCard.innerHTML = `
            <h3>${movie.title}</h3>
            <p>Rating: ${movie.rating}</p>
        `;
        moviesSection.appendChild(movieCard);
    });
}

// Call the renderMovies function when the page loads
document.addEventListener('DOMContentLoaded', renderMovies);
