<template>
  <div>
    <h2>Your To-Dos</h2>
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        <span>{{ todo.title }}</span>
        <button @click="markCompleted(todo.id)">Complete</button>
        <button @click="deleteTodo(todo.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['todos'],
  methods: {
    async markCompleted(id) {
      await axios.post(`/todos/${id}/complete`);
      this.$emit('todoUpdated');
    },
    async deleteTodo(id) {
      await axios.delete(`/todos/${id}`);
      this.$emit('todoUpdated');
    },
  },
};
</script>
