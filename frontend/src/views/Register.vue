<template>
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="register">
      <div>
        <label for="username">Username</label>
        <input type="text" id="username" v-model="formData.username" required/>
      </div>
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="formData.email" required/>
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="formData.password" required/>
      </div>
      <button type="submit">Register</button>
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
        email: '',
        password: '',
      },
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('/users/', this.formData);
        alert('Registration successful!');
        this.$router.push('/login');
      } catch (error) {
        alert(error.response?.data?.detail || 'Registration failed.');
      }
    },
  },
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
}
</style>
