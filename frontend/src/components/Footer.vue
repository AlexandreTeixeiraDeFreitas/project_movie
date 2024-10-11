<template>
  <footer class="bg-gray-800 text-white py-8 mt-0">
    <div class="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
      <!-- Section Liens Rapides -->
      <div>
        <h2 class="font-bold text-lg mb-4">Liens Rapides</h2>
        <ul class="space-y-2">
          <li><a href="#accueil" class="hover:text-gray-400">Accueil</a></li>
          <li><a href="#nouveautes" class="hover:text-gray-400">Nouveautés</a></li>
          <li><a href="#genres" class="hover:text-gray-400">Genres</a></li>
          <li><a href="#contact" class="hover:text-gray-400">Contact</a></li>
        </ul>
      </div>

      <!-- Section Contact -->
      <div>
        <h2 class="font-bold text-lg mb-4">Contact</h2>
        <ul class="space-y-2">
          <li><span class="font-semibold">Email:</span> support@cinemavue.com</li>
          <li><span class="font-semibold">Téléphone:</span> +33 1 23 45 67 89</li>
          <li><span class="font-semibold">Adresse:</span> 123 Rue du Cinéma, Paris</li>
        </ul>
      </div>

      <!-- Section Réseaux Sociaux -->
      <div>
        <h2 class="font-bold text-lg mb-4">Suivez-nous</h2>
        <div class="flex space-x-4">
          <a href="#" class="text-gray-400 hover:text-white">
            <i class="fab fa-facebook-f"></i>
          </a>
          <a href="#" class="text-gray-400 hover:text-white">
            <i class="fab fa-twitter"></i>
          </a>
          <a href="#" class="text-gray-400 hover:text-white">
            <i class="fab fa-instagram"></i>
          </a>
          <a href="#" class="text-gray-400 hover:text-white">
            <i class="fab fa-linkedin-in"></i>
          </a>
        </div>
      </div>
    </div>

    <!-- Copyright -->
    <div class="mt-8 border-t border-gray-700 pt-4 text-center text-gray-500">
      &copy; 2024 Cinéma Vue. Tous droits réservés.
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
};
</script>

<style scoped>
/* Ajoute ici des styles personnalisés si nécessaire */
</style>
