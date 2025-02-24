<template>
  <div class="login-container">
    <!-- Left Side: Background Image -->
    <div class="login-image"></div>

    <!-- Right Side: Login Form -->
    <div class="login-form">
      <div class="form-content">
        <h3 class="school-name">JZGMSAT INVENTORY MANAGEMENT SYSTEM</h3>

        <!-- Login Form -->
        <form @submit.prevent="login">
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input id="email" type="email" v-model="email" class="form-control" placeholder="Enter email" required>
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input id="password" type="password" v-model="password" class="form-control" placeholder="Enter password" required>
          </div>

          <button type="submit" class="btn btn-dark w-100">Sign In</button>

          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

          <div class="text-center mt-3">
            <a href="#" class="forgot-password">Forgot password?</a>
          </div>
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
  setup() {
    const email = ref("");
    const password = ref("");
    const errorMessage = ref("");
    const router = useRouter();

    onMounted(() => {
      document.body.style.overflow = "hidden"; // Prevents scrolling issues
    });

    const login = async () => {
      console.log("Logging in with:", { email: email.value, password: password.value });

      try {
        const response = await axios.post("http://127.0.0.1:8000/api/login/", {
          email: email.value,
          password: password.value,
        });

        if (response.data.token) {
          localStorage.setItem("userToken", response.data.token);
          router.push("/home"); // Redirect to home page after login
        } else {
          errorMessage.value = "Invalid login credentials";
        }
      } catch (error) {
        console.error("Login failed:", error.response?.data || error);
        errorMessage.value = "Login failed. Please check your credentials.";
      }
    };

    return { email, password, errorMessage, login };
  }
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
  width: 40%; /* Prevent image from taking too much space */
  height: 100vh;
  background: url('@/assets/loginBg.png') no-repeat center center;
  background-size: cover;
}


.login-form {
  width: 60%; /* Form takes the remaining space */
  display: flex;
  justify-content: center; /* Ensures centering */
  align-items: center;
  background-color: white;
  padding: 4rem;
}


.form-content {
  width: 100%;
  max-width: 500px; /* Ensures a well-sized form */
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

/* ✅ FORGOT PASSWORD LINK */
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
