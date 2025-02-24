<template>
    <div class="login-container">
      <!-- Left Side: Background Image -->
      <div class="login-image"></div>
  
      <!-- Right Side: Login Form -->
      <div class="login-form">
        <div class="text-center">
          <!-- Logos (Properly Aligned Side by Side) -->
          <div class="logos">
            <img src="@/assets/tesda.png" alt="Logo 1" class="logo">
          </div>
  
          <!-- School Name -->
          <h3 class="fw-bold school-name">JACOBO Z. GONZALES MEMORIAL SCHOOL OF ARTS AND TRADES</h3>
        </div>
  
        <!-- Login Form -->
        <form @submit.prevent="login">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" v-model="email" class="form-control" placeholder="Enter email" required>
          </div>
  
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" v-model="password" class="form-control" placeholder="Enter password" required>
          </div>
  
          <button type="submit" class="btn btn-dark w-100">Sign In</button>
  
          <div class="text-center mt-3">
            <a href="#" class="forgot-password">Forgot password?</a>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  
  export default {
    setup() {
      const email = ref("");
      const password = ref("");
  
      const login = () => {
        console.log("Logging in with:", { email: email.value, password: password.value });
        // Add API authentication here
      };
  
      return { email, password, login };
    }
  };
  </script>
  
  <style scoped>
  /* Main Layout */
  .login-container {
    display: flex;
    height: 100vh;
  }
  
  /* Left Side: Background Image */
  .login-image {
    flex: 1;
    background: url("@/assets/loginBg.png") no-repeat center center;
    background-size: cover;
  }
  
  /* Right Side: Login Form */
  .login-form {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 3rem;
    background-color: white;
  }
  
  /* Logos */
  .logos {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .logo {
    max-height: 70px;
    margin: 0 10px;
  }
  
  /* School Name */
  .school-name {
    font-size: 18px;
    text-transform: uppercase;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
  }
  
  /* Form Styling */
  .form-control {
    border-radius: 5px;
    padding: 12px;
    font-size: 16px;
  }
  
  /* Button */
  .btn-dark {
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
  }
  
  /* Forgot Password */
  .forgot-password {
    text-decoration: none;
    color: #007bff;
    font-size: 14px;
  }
  .forgot-password:hover {
    text-decoration: underline;
  }
  
  /* Mobile View */
  @media (max-width: 768px) {
    .login-container {
      flex-direction: column;
    }
    .login-image {
      height: 40vh;
    }
    .login-form {
      height: auto;
      padding: 2rem;
    }
  }
  </style>
  