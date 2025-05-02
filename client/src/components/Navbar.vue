<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <!-- BRAND/LOGO -->
      <router-link class="navbar-brand d-flex align-items-center gap-2" to="/home">
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
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <router-link 
              class="nav-link text-white" 
              :class="{ 'active-route': $route.path === '/home' }" 
              to="/home"
            >
              Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link 
              class="nav-link text-white" 
              :class="{ 'active-route': $route.path === '/scan' }" 
              to="/scan"
            >
              Scan
            </router-link>
          </li>
          <li class="nav-item">
            <button
              class="nav-link btn btn-link text-white logout-btn"
              data-bs-toggle="modal"
              data-bs-target="#logoutModal"
            >
              <i class="bi bi-box-arrow-right"></i>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Smaller Logout Confirmation Modal -->
  <div class="modal fade" id="logoutModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
      <div class="modal-content rounded-4 p-3 border-0 shadow-sm">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <h6 class="fw-bold text-dark mb-0">Confirm Logout</h6>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body text-center px-2 py-1">
          <p class="text-secondary small mb-3">Are you sure you want to log out?</p>
          <div class="d-flex justify-content-center gap-2">
            <button class="btn btn-outline-secondary btn-sm px-3" data-bs-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-sm px-3" @click="logout" data-bs-dismiss="modal">
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
.logout-btn {
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
  padding: 5px 10px;
  border-radius: 5px;
}

.logout-btn:hover {
  background-color: var(--bs-danger) !important;
  color: white !important;
}

.navbar .container {
  padding-left: 20px;
  padding-right: 20px;
}

.nav-link {
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
  padding: 8px 12px;
  border-radius: 5px;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.active-route {
  font-weight: bold;
  border-bottom: 2px solid white;
}

.modal-content {
  font-family: 'Segoe UI', sans-serif;
}

.modal-body p {
  margin: 0;
  font-size: 14px;
}

.btn {
  font-weight: 500;
}
</style>
