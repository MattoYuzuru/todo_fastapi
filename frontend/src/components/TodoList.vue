<template>
  <div class="container">
    <h2>Your ToDos</h2>
    <ul class="list-group mt-4">
      <li v-for="todo in todos" :key="todo.id"
          class="list-group-item d-flex justify-content-between align-items-center">
        <router-link :to="'/todos/' + todo.id">
          <span>{{ todo.title }}</span>
          <span>{{ todo.description }}</span>
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
  data() {
    return {
      todos: []
    };
  },
  async mounted() {
    await this.fetchTodos();
  },
  methods: {
    async fetchTodos() {
      try {
        const response = await axios.get("http://localhost:8000/todos/all/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.todos = response.data;
      } catch (error) {
        console.error("Error fetching todos:", error.response ? error.response.data : error);
      }
    },
    async deleteTodo(todoId) {
      try {
        await axios.delete(`http://localhost:8000/todos/${todoId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        await this.fetchTodos();
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
    async markCompleted(todoId) {
      try {
        await axios.post(`http://localhost:8000/todos/${todoId}/complete`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        await this.fetchTodos();
      } catch (error) {
        console.error("Error marking todo as completed:", error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  margin-left: 10px;
  padding: 5px 10px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #0056b3;
}
</style>
