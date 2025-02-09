<template>
  <div class="container">
    <h2>Your ToDos</h2>

    <ul class="list-group mt-4">
      <li v-for="todo in todos" :key="todo.id"
          class="list-group-item d-flex justify-content-between align-items-center">
        <router-link :to="'/todos/' + todo.id">
          <span>{{ todo.title }}<br></span>
          <span>{{ todo.description }}</span>
          <br>
        </router-link>
        <button @click="markCompleted(todo.id)">Complete</button>
        <button @click="deleteTodo(todo.id)">Delete</button>
      </li>
    </ul>

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }}</span>
      <button @click="nextPage" :disabled="todos.length < limit">Next</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      currentPage: 1,
      limit: 10,
    };
  },
  async mounted() {
    await this.fetchTodos();
  },
  methods: {
    async fetchTodos() {
      try {
        const skip = (this.currentPage - 1) * this.limit;
        const response = await axios.get(`http://localhost:8000/todos/all/?skip=${skip}&limit=${this.limit}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.todos = response.data;
      } catch (error) {
        console.error("Error fetching todos:", error);
      }
    },
    async deleteTodo(todoId) {
      try {
        await axios.delete(`http://localhost:8000/todos/${todoId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        await this.fetchTodos();
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
    async markCompleted(todoId) {
      try {
        await axios.post(`http://localhost:8000/todos/${todoId}/complete`, {}, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        await this.fetchTodos();
      } catch (error) {
        console.error("Error marking todo as completed:", error);
      }
    },
    nextPage() {
      this.currentPage++;
      this.fetchTodos();
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchTodos();
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0 10px;
  padding: 5px 10px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}

.pagination button:disabled {
  background-color: gray;
  cursor: not-allowed;
}

.pagination span {
  font-size: 18px;
  font-weight: bold;
}
</style>
