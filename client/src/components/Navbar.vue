<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <!-- BRAND/LOGO -->
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img src="@/assets/tesda.png" alt="Logo" class="me-2" height="70" />
        <span class="fw-bold">JZGMSAT</span>
      </router-link>

      <!-- TOGGLER (Mobile) -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- NAV LINKS -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/scan">Scan</router-link>
          </li>
          <!-- LOGOUT BUTTON triggers modal -->
          <li class="nav-item">
            <button
              class="nav-link btn btn-link text-white"
              data-bs-toggle="modal"
              data-bs-target="#logoutModal"
            >
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- LOGOUT CONFIRMATION MODAL -->
  <div
    class="modal fade"
    id="logoutModal"
    tabindex="-1"
    aria-labelledby="logoutModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="logoutModalLabel">Confirm Logout</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          Are you sure you want to log out?
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <!-- Actual logout call here -->
          <button
            type="button"
            class="btn btn-danger"
            @click="logout"
            data-bs-dismiss="modal"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "Navbar",
  methods: {
    async logout() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/logout/", {
          method: "POST",
          credentials: "include",
        });
        const data = await response.json();

        if (data.success) {
          localStorage.removeItem("isAuthenticated");
          // Once we push '/', we see the login page
          this.$router.push("/");
        } else {
          alert(data.message || "Logout failed");
        }
      } catch (error) {
        console.error("Logout error:", error);
        alert("Error during logout");
      }
    },
  },
};
</script>

<style scoped>
/* ✅ Ensures button is properly styled */
.modal-footer .btn-danger {
  background-color: #dc3545;
  border: none;
}

.modal-footer .btn-danger:hover {
  background-color: #c82333;
}
</style>
