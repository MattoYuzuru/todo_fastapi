<template>
  <div id="app">
    <header>
      <h1>To-Do App</h1>
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/login">Login</router-link> |
        <router-link to="/register">Register</router-link> |
        <router-link to="/pomodoro">Pomodoro</router-link>
      </nav>
    </header>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
nav {
  margin-bottom: 1rem;
}
nav a {
  margin-right: 10px;
  text-decoration: none;
  color: blue;
}
nav a.router-link-active {
  font-weight: bold;
}
</style>
