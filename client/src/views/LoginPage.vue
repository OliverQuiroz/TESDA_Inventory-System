<template>
  <div class="login-container">
    <!-- Left Side: Background Image -->
    <div class="login-image"></div>

    <!-- Right Side: Login Form -->
    <div class="login-form">
      <div class="form-content">
        <h3 class="school-name">JZGMSAT INVENTORY MANAGEMENT SYSTEM</h3>
        <form @submit.prevent="login">
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              type="text"
              v-model="username"
              class="form-control"
              placeholder="Enter username"
              required
            />
          </div>
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              type="password"
              v-model="password"
              class="form-control"
              placeholder="Enter password"
              required
            />
          </div>
          <button type="submit" class="btn btn-dark w-100">Sign In</button>
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  name: "LoginPage",
  setup() {
    const username = ref("");
    const password = ref("");
    const errorMessage = ref("");
    const router = useRouter();

    onMounted(() => {
      document.body.style.overflow = "hidden";
    });

    const login = async () => {
      console.log("Logging in with:", { username: username.value, password: password.value });
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/login/",
          {
            // Send the username value as "email" to match Django view expectations.
            email: username.value,
            password: password.value,
          },
          { withCredentials: true }
        );

        if (response.data.token) {
          localStorage.setItem("userToken", response.data.token);
          router.push("/home");
        } else if (response.data.success) {
          localStorage.setItem("isAuthenticated", "true");
          router.push("/home");
        } else {
          errorMessage.value = "Invalid login credentials";
        }
      } catch (error) {
        console.error("Login failed:", error.response?.data || error);
        errorMessage.value = "Login failed. Please check your credentials.";
      }
    };

    return { username, password, errorMessage, login };
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  align-items: center;
}
.login-image {
  width: 40%;
  height: 100vh;
  background: url('@/assets/loginBg.png') no-repeat center center;
  background-size: cover;
}
.login-form {
  width: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
  padding: 4rem;
}
.form-content {
  width: 100%;
  max-width: 500px;
  min-width: 400px;
  text-align: center;
}
.school-name {
  font-size: 24px;
  text-transform: uppercase;
  font-weight: bold;
  margin-bottom: 30px;
}
.form-group {
  width: 100%;
  margin-bottom: 20px;
  text-align: left;
}
.form-label {
  display: block;
  font-weight: bold;
  margin-bottom: 6px;
  font-size: 15px;
}
.form-control {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  transition: all 0.3s ease-in-out;
}
.form-control:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 6px rgba(0, 123, 255, 0.3);
}
.btn-dark {
  padding: 14px;
  font-size: 17px;
  font-weight: bold;
  border-radius: 5px;
  background-color: #343a40;
  transition: 0.3s;
}
.btn-dark:hover {
  background-color: #23272b;
}
.forgot-password {
  text-decoration: none;
  color: #007bff;
  font-size: 14px;
}
.forgot-password:hover {
  text-decoration: underline;
}
@media (max-width: 992px) {
  .login-container {
    flex-direction: column;
  }
  .login-image {
    width: 100%;
    height: 35vh;
  }
  .login-form {
    width: 100%;
    padding: 3rem;
  }
  .form-content {
    max-width: 400px;
  }
}
@media (max-width: 768px) {
  .login-form {
    padding: 2rem;
  }
  .form-content {
    max-width: 350px;
  }
}
</style>
