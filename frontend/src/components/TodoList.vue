<template>
  <div class="container">
    <h2>Your ToDos</h2>
    <ul class="list-group mt-4">
      <li v-for="todo in todos" :key="todo.id"
          class="list-group-item d-flex justify-content-between align-items-center">
        <router-link :to="'/todos/' + todo.id">
          <span>{{ todo.title }}</span>
        </router-link>
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
    async deleteTodo(todoId) {
      try {
        await axios.delete(`http://localhost:8000/todos/${todoId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.$emit('todoUpdated');
      } catch (error) {
        console.error(error);
      }
    },
    async markCompleted(todoId) {
      try {
        await axios.post(`http://localhost:8000/todos/${todoId}/complete`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.$emit('todoUpdated');
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>
