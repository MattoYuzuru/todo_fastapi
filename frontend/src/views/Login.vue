<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username</label>
        <input type="text" id="username" v-model="formData.username" required/>
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="formData.password" required/>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/users/login', new URLSearchParams({
          username: this.formData.username,
          password: this.formData.password,
        }));
        const token = response.data.access_token;
        localStorage.setItem('token', token);
        alert('Login successful!');
        this.$router.push('/');
      } catch (error) {
        alert(error.response?.data?.detail || 'Login failed.');
      }
    },
  },
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
}
</style>
