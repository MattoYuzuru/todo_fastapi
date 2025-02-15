<template>
  <div class="container">
    <nav class="nav-bar">
      <router-link to="/">Home</router-link>
      <router-link to="/todos/all">All Todos</router-link>
      <router-link to="/todos/create">Create Todo</router-link>
      <router-link v-if="!isAuthenticated" to="/login">Login</router-link>
      <router-link v-if="!isAuthenticated" to="/register">Register</router-link>
      <router-link v-if="isAuthenticated" to="/users/me">Account Settings</router-link>
    </nav>

    <div class="welcome-section">
      <h1>Welcome to Your Todo Manager</h1>
      <p v-if="isAuthenticated">Manage your tasks efficiently and track your progress!</p>
      <p v-else>Please log in to track your todos and see statistics.</p>
    </div>

    <div v-if="isAuthenticated" class="stats-section">
      <h2>Your Statistics</h2>
      <p>Current Streak: {{ user.current_streak }}</p>
      <p>Longest Streak: {{ user.longest_streak }}</p>
      <p>Pomodoro Sessions: {{ user.pomodoro_sessions }}</p>
      <p>Tasks Completed: {{ user.tasks_completed }}</p>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  computed: {
    ...mapGetters(["isAuthenticated", "getUser"]),
    user() {
      return this.getUser || {};
    }
  },
  methods: {
    ...mapActions(["fetchUser"])
  },
  async mounted() {
    await this.fetchUser();
  }
};
</script>


<style scoped>

* {
  font-family: Andale Mono, monospace;
}

.container {
  max-width: 800px;
  margin: 20px auto;
  padding: 24px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.nav-bar {
  display: flex;
  justify-content: space-around;
  padding: 12px;
  background: #007bff;
  border-radius: 6px;
}

.nav-bar a {
  text-decoration: none;
  color: white;
  font-weight: bold;
  transition: opacity 0.3s ease;
}

.nav-bar a:hover {
  opacity: 0.8;
}

.welcome-section {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-top: 20px;
}

.welcome-section h1 {
  font-size: 24px;
  color: #222;
}

.welcome-section p {
  font-size: 16px;
  color: #555;
}

.stats-section {
  padding: 20px;
  background: #ffffff;
  border-radius: 6px;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.stats-section h2 {
  font-size: 20px;
  color: #222;
  margin-bottom: 10px;
}

.stats-section p {
  font-size: 16px;
  color: #555;
  margin: 6px 0;
}
</style>
