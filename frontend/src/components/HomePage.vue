<template>
  <div class="container">
    <nav class="nav-bar">
      <router-link to="/">Home</router-link>
      <router-link to="/todos/all">All Todos</router-link>
      <router-link to="/todos/create">Create Todo</router-link>
      <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
      <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
      <router-link v-if="isLoggedIn" to="/account">Account Settings</router-link>
    </nav>

    <div class="welcome-section">
      <h1>Welcome to Your Todo Manager</h1>
      <p v-if="isLoggedIn">Manage your tasks efficiently and track your progress!</p>
      <p v-else>Please log in to track your todos and see statistics.</p>
    </div>

    <div v-if="isLoggedIn" class="stats-section">
      <h2>Your Statistics</h2>
      <p>Current Streak: {{ userStats.current_streak }}</p>
      <p>Longest Streak: {{ userStats.longest_streak }}</p>
      <p>Pomodoro Sessions: {{ userStats.pomodoro_sessions }}</p>
      <p>Tasks Completed: {{ userStats.tasks_completed }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isLoggedIn: false,
      userStats: {},
    };
  },
  async mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      this.isLoggedIn = true;
      await this.fetchUserStats();
    }
  },
  methods: {
    async fetchUserStats() {
      try {
        const response = await axios.get('http://localhost:8000/users/me/', {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        this.userStats = response.data;
      } catch (error) {
        console.error('Error fetching user statistics:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid black;
  background-color: white;
}

.nav-bar {
  display: flex;
  justify-content: space-around;
  padding: 10px;
  border: 1px solid black;
  margin-bottom: 20px;
}

.nav-bar a {
  text-decoration: none;
  color: black;
}

.welcome-section, .stats-section {
  padding: 20px;
  border: 1px solid black;
  margin-top: 10px;
}
</style>
