<template>
    <div v-for="film in films" :key="film.id" @click="goToFilmDetails(film.id)" class="cursor-pointer">

    </div>
  </template>
  
  <script>
  export default {

    methods: {
      goToFilmDetails(id) {
        this.$router.push({ name: 'FilmDetails', params: { id } });
      }
    }
  }
  </script>
  