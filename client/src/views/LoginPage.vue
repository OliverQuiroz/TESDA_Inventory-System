<template>
    <div class="login-container">
      <!-- Left Side: Proper Full-Height Background Image -->
      <div class="login-image"></div>
  
      <!-- Right Side: Centered Login Form -->
      <div class="login-form">
        <div class="form-content">
          <div class="text-center">
            <!-- Logos: Properly Sized & Positioned -->
            <div class="logos">
              <img src="@/assets/jzgmsatLogo.png" alt="School Logo" class="logo">
            </div>
  
            <!-- School Name -->
            <h3 class="school-name">JACOBO Z. GONZALES MEMORIAL SCHOOL OF ARTS AND TRADES</h3>
          </div>
  
          <!-- Login Form -->
          <form @submit.prevent="login">
            <div class="input-group">
              <label class="form-label">Email</label>
              <input type="email" v-model="email" class="form-control" placeholder="Enter email" required>
            </div>
  
            <div class="input-group">
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
    width: 100vw;
  }
  
  /* Left Side: FIXED 50% WIDTH IMAGE */
  .login-image {
    width: 50%; /* Ensures full half-page coverage */
    height: 100vh;
    background: url("@/assets/loginBg.png") no-repeat center center;
    background-size: cover;
  }
  
  /* Right Side: Centered Login Form */
  .login-form {
    width: 50%; /* Ensures the form takes exactly half of the screen */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: white;
    padding: 4rem 3rem; /* Adjusted padding */
  }
  
  /* Form Content */
  .form-content {
    width: 100%;
    max-width: 400px; /* FINAL WIDTH FIX */
    text-align: center;
  }
  
  /* Logos */
  .logos {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .logo {
    max-height: 65px; /* Fixed size for better alignment */
  }
  
  /* School Name */
  .school-name {
    font-size: 18px;
    text-transform: uppercase;
    font-weight: bold;
    text-align: center;
    margin-bottom: 25px;
  }
  
  /* Form Inputs */
  .input-group {
    width: 100%;
    margin-bottom: 18px;
  }
  
  .form-label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
    font-size: 14px;
    text-align: left;
  }
  
  .form-control {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #ced4da;
    border-radius: 5px;
    transition: all 0.3s ease-in-out;
  }
  
  .form-control:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.2);
  }
  
  /* Button */
  .btn-dark {
    padding: 14px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 5px;
    background-color: #343a40;
    transition: 0.3s;
  }
  
  .btn-dark:hover {
    background-color: #23272b;
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
  @media (max-width: 992px) {
    .login-container {
      flex-direction: column;
    }
    .login-image {
      width: 100%;
      height: 40vh;
    }
    .login-form {
      width: 100%;
      padding: 2rem;
    }
    .form-content {
      max-width: 380px;
    }
  }
  </style>
  