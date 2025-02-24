<!-- App.vue -->
<template>
  <div>
    <!-- Conditionally show the Navbar if not "hideNavbar" -->
    <Navbar v-if="showNavbar" />
    <!-- The routed page -->
    <router-view />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'App',
  components: { Navbar },
  setup() {
    const route = useRoute();
    // If the route has meta.hideNavbar = true, we hide the navbar
    const showNavbar = computed(() => !route.meta.hideNavbar);

    return { showNavbar };
  }
}
</script>

<style>
/* Optional global styles */
</style>
