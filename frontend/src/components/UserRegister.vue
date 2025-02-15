<template>
  <div class="register-container">
    <div class="register-card">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" class="form-control" required/>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" class="form-control" required/>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" class="form-control" required/>
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://localhost:8000/create', {
          username: this.username,
          email: this.email,
          password: this.password
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data);
        this.$router.push('/login');
      } catch (error) {
        this.errorMessage = "Registration failed. Please check your details.";
      }
    }
  }
};
</script>

<style scoped>

* {
    font-family: Andale Mono, monospace;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f4;
}

.register-card {
  width: 100%;
  max-width: 400px;
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 18px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
  transition: border-color 0.2s ease-in-out;
}

input:focus {
  border-color: #28a745;
  outline: none;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: background-color 0.2s ease-in-out;
}

.btn-primary:hover {
  background-color: #218838;
}

.error {
  color: #d32f2f;
  margin-top: 12px;
  font-size: 14px;
  font-weight: 500;
}
</style>

