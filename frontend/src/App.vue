<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
nav {
  margin-bottom: 1rem;
}

nav a, nav a.router-link-active {
  margin-right: 10px;
  text-decoration: none;
  color: blue;
}

nav a.router-link-active {
  font-weight: bold;
}
</style>