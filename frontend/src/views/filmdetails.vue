<template>
    <section class="bg-gray-900 text-white p-6">
      <div class="container mx-auto">
        <h1 class="text-3xl font-bold mb-4">{{ film.title }}</h1>
        <img :src="film.image" alt="Affiche du film" class="w-full max-w-md mx-auto">
        <p class="mt-4">{{ film.description }}</p>
        <a :href="film.trailer" class="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">Regarder le Trailer</a>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    props: {
      id: Number
    },
    data() {
      return {
        film: null
      };
    },
    mounted() {
      // Simuler la récupération des données du film
      const films = [
        { id: 1, title: "Inception", image: "path_to_image/inception.jpg", description: "Un voleur, qui s'infiltre dans les rêves des autres.", trailer: "https://youtube.com/example_trailer1" },
        { id: 2, title: "Interstellar", image: "path_to_image/interstellar.jpg", description: "Un voyage à travers l'espace pour découvrir une nouvelle maison.", trailer: "https://youtube.com/example_trailer2" },
        { id: 3, title: "The Matrix", image: "path_to_image/matrix.jpg", description: "Un monde dystopique où la réalité n'est qu'une simulation.", trailer: "https://youtube.com/example_trailer3" }
      ];
      this.film = films.find(film => film.id === this.id);
    }
  }
  </script>
  