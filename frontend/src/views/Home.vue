<template>
  <div>
    <h1>Welcome, {{ user?.username || 'Guest' }}</h1>
    <AddToDo @todoAdded="fetchTodos"/>
    <ToDoList :todos="todos" @todoUpdated="fetchTodos"/>
  </div>
</template>

<script>
import {mapActions, mapState} from 'vuex';
import AddToDo from '@/components/AddToDo.vue';
import ToDoList from '@/components/ToDoList.vue';

export default {
  components: {AddToDo, ToDoList},
  computed: {
    ...mapState(['user', 'todos']),
  },
  methods: {
    ...mapActions(['fetchTodos']),
  },
  mounted() {
    this.fetchTodos();
  },
};
</script>
