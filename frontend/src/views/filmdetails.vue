<template>
  <section class="bg-gray-900 text-white p-6 mt-20">
    <div class="container mx-auto">
      <h1 class="text-4xl font-bold mb-4">{{ film.title }}</h1>
      <img :src="film.imageUrl" alt="Affiche du film" class="w-full max-w-md mx-auto rounded shadow-lg mb-6" v-if="film.imageUrl">
      <p class="text-lg mt-4 mb-6">Genres : <span class="text-yellow-400">{{ film.genres.join(', ') }}</span></p>
      <a v-if="film.trailerUrl" :href="film.trailerUrl" target="_blank" class="mt-4 inline-block bg-yellow-500 text-gray-900 px-4 py-2 rounded hover:bg-yellow-600 transition">Regarder le Trailer</a>

      <div class="mt-8" v-if="film.usersInfo && film.usersInfo.length > 0">
        <h2 class="text-3xl font-bold mb-4">Avis des utilisateurs</h2>
        <table class="table-auto w-full text-white mt-4 border-collapse border border-gray-700">
          <thead>
            <tr class="bg-gray-800">
              <th class="border border-gray-600 p-2 text-left">Utilisateur</th>
              <th class="border border-gray-600 p-2 text-left">Note</th>
              <th class="border border-gray-600 p-2 text-left">Tags</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(userInfo, index) in visibleReviews" :key="index" class="bg-gray-800 hover:bg-gray-700 transition-all">
              <td class="border border-gray-600 p-2">{{ userInfo.userId }}</td>
              <td class="border border-gray-600 p-2">
                <div class="flex items-center">
                  <span class="text-yellow-400">{{ userInfo.rating ? userInfo.rating.toFixed(1) : 'N/A' }}</span>
                  <div class="ml-2 flex">
                    <span v-for="star in 5" :key="star" class="text-yellow-400" :class="{'text-gray-500': star > Math.round(userInfo.rating || 0)}">
                      ★
                    </span>
                  </div>
                </div>
              </td>
              <td class="border border-gray-600 p-2">{{ userInfo.tags ? userInfo.tags.join(', ') : 'Aucun tag' }}</td>
            </tr>
          </tbody>
        </table>

        <div class="mt-4 text-center">
          <button v-if="showMoreButton" @click="showAllReviews" class="bg-yellow-500 text-gray-900 px-4 py-2 rounded hover:bg-yellow-600 transition">
            Voir plus
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      film: {
        title: '',
        imageUrl: '',
        genres: [],
        description: '',
        trailerUrl: '',
        usersInfo: []
      },
      showAll: false // Variable pour contrôler l'affichage des avis
    };
  },
  computed: {
    visibleReviews() {
      // Affiche les 3 premiers avis si 'showAll' est false, sinon affiche tous les avis
      return this.showAll ? this.film.usersInfo : this.film.usersInfo.slice(0, 3);
    },
    showMoreButton() {
      // Affiche le bouton "Voir plus" seulement si le nombre d'avis est supérieur à 3 et que 'showAll' est false
      return this.film.usersInfo.length > 3 && !this.showAll;
    }
  },
  methods: {
    showAllReviews() {
      this.showAll = true; // Change l'état pour afficher tous les avis
    }
  },
  async mounted() {
  try {
    const movieId = this.$route.params.id;
    const response = await fetch(`http://localhost:5000/filmdetails?movie_id=${movieId}`, {
      method: 'GET'
    });
    const data = await response.json();
    if (response.ok) {
      this.film = {
        title: data.title,
        imageUrl: `http://localhost:5000/poster/${movieId}`, // Mise à jour de l'URL de l'image pour utiliser l'API Flask
        genres: data.genres || [],
        description: `IMDB ID: ${data.imdbId}, TMDB ID: ${data.tmdbId}`,
        trailerUrl: `https://www.imdb.com/title/${data.imdbId}/`,
        usersInfo: data.usersInfo || []
      };
    } else {
      console.error('Erreur lors de la récupération des détails du film:', data.message);
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des détails du film:', error);
  }
}

};
</script>

<style scoped>
/* Améliorations inspirées du style Allociné */
table {
  border-spacing: 0;
}

th,
td {
  border: none;
}

th {
  background-color: #1f2937; /* Couleur sombre pour les en-têtes */
}

tr:hover {
  background-color: #2d3748; /* Couleur de survol plus claire */
}
</style>
