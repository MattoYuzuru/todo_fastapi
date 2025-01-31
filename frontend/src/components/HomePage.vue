<template>
  <div>
    <h1>Welcome, {{ user?.username || 'Guest' }}</h1>

    <router-link v-if="isAuthenticated" to="/todos/create">
      <button>Add New Todo</button>
    </router-link>

    <TodoList v-if="isAuthenticated" :todos="todos" @todoUpdated="fetchTodos"/>
    <p v-else>Please log in to manage your to-do list.</p>
  </div>
</template>

<script>
import {mapActions} from 'vuex';
import TodoList from '@/components/TodoList.vue';

export default {
  components: {TodoList},
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    ...mapActions(['fetchTodos']),
  },
  mounted() {
    if (this.isAuthenticated) {
      this.fetchTodos();
    }
  },
};
</script>
