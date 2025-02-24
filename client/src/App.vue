<template>
  <div>
    <Navbar v-if="showNavbar" />
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import Navbar from "@/components/Navbar.vue";

export default {
  components: {
    Navbar,
  },
  setup() {
    const route = useRoute();

    // Define the pages where the navbar should be hidden
    const showNavbar = computed(() => route.path !== "/login");

    return { showNavbar };
  },
};
</script>
