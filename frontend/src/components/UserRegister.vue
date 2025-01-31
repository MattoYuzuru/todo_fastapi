<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" class="form-control" required/>
      </div>
      <div class="form-control">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" class="form-control" required/>
      </div>
      <div class="form-control">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" required/>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
      password: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://localhost:8000/users/create', {
          username: this.username,
          email: this.email,
          password: this.password
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data);
        this.$router.push('/users/login');
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
