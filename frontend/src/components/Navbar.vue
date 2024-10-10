<template>
  <nav class="bg-gray-800 text-white p-4 fixed top-0 w-full z-50 shadow">
    <div class="container mx-auto flex items-center justify-between flex-wrap p-2">
      <!-- Logo et titre, cliquable pour revenir à la page d'accueil -->
      <div class="flex items-center flex-shrink-0 text-white mr-6 cursor-pointer">
        <img src="\src\assets\img\images.jpeg" alt="Logo Cinema Vue" class="h-8 w-8 mr-2">
        <span class="font-semibold text-xl tracking-tight">Cinéma Vue</span>
      </div>
      <!-- Bouton menu mobile -->
      <div class="block lg:hidden">
        <button @click="toggle" class="flex items-center px-3 py-2 border rounded text-teal-200 border-teal-400 hover:text-white hover:border-white">
          <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
        </button>
      </div>
      <!-- Liens de navigation et champ de recherche -->
      <div :class="{'hidden': !isOpen, 'block': isOpen}" class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
        <div class="text-sm lg:flex-grow">
          <a href="#accueil" class="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
            Accueil
          </a>
          <a href="#nouveautes" class="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4">
            Nouveautés
          </a>
          <a href="#genres" class="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white">
            Genres
          </a>
        </div>
        <div class="relative">
          <input class="border-2 border-gray-300 bg-white h-10 px-5 pr-16 rounded-l-lg text-sm focus:outline-none"
            type="search" name="search" placeholder="Rechercher des films...">
          <button type="submit" class="absolute right-0 top-0 mt-1 mr-1 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-r-lg">
            <svg class="h-4 w-4 fill-current" viewBox="0 0 24 24">
              <path d="M23.7 22.3l-7.1-7.1c1.4-1.7 2.2-3.9 2.2-6.2 0-5.5-4.5-10-10-10S-1.2 5.5-1.2 11s4.5 10 10 10c2.3 0 4.5-.8 6.2-2.2l7.1 7.1c.2.2.5.3.7.3s.5-.1.7-.3c.4-.4.4-1 0-1.4zM1.8 11c0-4.4 3.6-8 8-8s8 3.6 8 8-3.6 8-8 8-8-3.6-8-8z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      isOpen: false
    };
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen;
    }
  }
}
</script>

<style scoped>
/* Tu peux personnaliser davantage le style ici si nécessaire */
</style>
