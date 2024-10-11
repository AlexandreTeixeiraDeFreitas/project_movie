<template>
  <section class="bg-gray-900 text-white p-6 min-h-screen mt-20">
    <div class="container mx-auto">
      <h1 class="text-4xl font-bold mb-6">Liste des Films</h1>

      <!-- Section de filtres -->
      <div class="bg-gray-800 p-4 mb-6 rounded">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Recherche par titre -->
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Rechercher par titre"
            class="p-2 rounded bg-gray-700 text-white"
          />

          <!-- Filtre par genre -->
          <select v-model="selectedGenre" class="p-2 rounded bg-gray-700 text-white">
            <option value="">Tous les genres</option>
            <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
          </select>

          <!-- Filtre par tag -->
          <select v-model="selectedTag" class="p-2 rounded bg-gray-700 text-white">
            <option value="">Tous les tags</option>
            <option v-for="tag in tags" :key="tag" :value="tag">{{ tag }}</option>
          </select>
        </div>
        <button @click="applyFilters" class="mt-4 p-2 bg-blue-600 rounded hover:bg-blue-700">Appliquer les filtres</button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div
          v-for="film in films"
          :key="film.movieId"
          class="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer hover:shadow-2xl transition-all"
          @click="() => goToFilmDetails(film.movieId)"
        >
          <img :src="film.imageUrl" alt="Affiche du film" class="w-full h-64 object-cover">
          <div class="p-4">
            <h2 class="text-xl font-bold mb-2">{{ film.title }}</h2>
            <p class="text-sm text-gray-400">Genres: {{ film.genres.join(', ') }}</p>
            <p class="text-sm text-yellow-400">Note Moyenne: {{ film.averageRating }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>


<script>
export default {
  data() {
    return {
      films: [],
      genres: [],
      tags: [],
      searchTerm: '',
      selectedGenre: '',
      selectedTag: ''
    };
  },
  methods: {
    async fetchFilms() {
  try {
    let url = `http://localhost:5000/films`;
    const params = [];

    if (this.selectedGenre) {
      params.push(`genres=${encodeURIComponent(this.selectedGenre)}`);
    }
    if (this.selectedTag) {
      params.push(`tag=${encodeURIComponent(this.selectedTag)}`);
    }
    if (this.searchTerm) {
      params.push(`search_term=${encodeURIComponent(this.searchTerm)}`);
    }
    
    if (params.length) {
      url += `?${params.join('&')}`;
    }

    const response = await fetch(url);
    const data = await response.json();
    console.log('Données des films reçues:', data); // Pour vérifier les données renvoyées par l'API
    if (response.ok) {
      this.films = data.map(film => ({
        movieId: film.movieId,
        title: film.title,
        genres: film.GenresArray || [],
        averageRating: film.AverageRating || 'N/A',
        imageUrl: film.movieId ? `http://localhost:5000/poster/${film.movieId}` : 'URL_IMAGE_PAR_DÉFAUT'
      }));
      console.log(this.films);
    } else {
      console.error('Erreur lors de la récupération des films:', data.message);
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des films:', error);
  }
},
    async fetchGenres() {
      try {
        const response = await fetch(`http://localhost:5000/genres`);
        const data = await response.json();
        console.log('Genres reçus:', data); // Log pour voir les genres reçus
        if (response.ok) {
          this.genres = data;
        } else {
          console.error('Erreur lors de la récupération des genres:', data.message);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des genres:', error);
      }
    },
    async fetchTags() {
      try {
        const response = await fetch(`http://localhost:5000/tags`);
        const data = await response.json();
        if (response.ok) {
          this.tags = data;
        } else {
          console.error('Erreur lors de la récupération des tags:', data.message);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des tags:', error);
      }
    },
    applyFilters() {
      this.fetchFilms(); // Rafraîchir les films en fonction des filtres appliqués
    },
    goToFilmDetails(id) {
      console.log('Redirection vers le film ID:', id);
      this.$router.push({ name: 'filmdetails', params: { id } });
    }
  },
  mounted() {
    this.fetchFilms(); // Récupère les films lorsque le composant est monté
    this.fetchGenres(); // Récupère les genres distincts
    this.fetchTags(); // Récupère les tags distincts
  }
};
</script>
