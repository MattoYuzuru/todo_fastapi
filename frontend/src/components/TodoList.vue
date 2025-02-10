<template>
  <div>
    <div class="container">
      <h2>Your ToDos</h2>
      <ul class="list-group mt-4">
        <li v-for="todo in todos" :key="todo.id"
            :class="['list-group-item', { 'completed-todo': todo.status === 'Completed' }]">
          <router-link :to="'/todos/' + todo.id" class="todo-link">
            <span class="todo-title">{{ todo.title }}</span><br>
            <span class="todo-description">{{ todo.description }}</span>
          </router-link>
          <div class="button-group">
            <button v-if="todo.status !== 'Completed'" @click="markCompleted(todo.id)" class="complete-btn">
              Complete
            </button>
            <button @click="deleteTodo(todo.id)">Delete</button>
          </div>
        </li>
      </ul>
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }}</span>
        <button @click="nextPage" :disabled="todos.length < limit">Next</button>
      </div>
    </div>
    <div class="create-button-container">
      <router-link to="/todos/create">
        <button class="add-button">📃 Add New Todo</button>
      </router-link>
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
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        await this.fetchTodos();
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
    async markCompleted(todoId) {
      try {
        await axios.post(`http://localhost:8000/todos/${todoId}/complete`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
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

.list-group {
  list-style: none;
  padding: 0;
}

.list-group-item {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  align-items: center;
  background: #f8f9fa;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.completed-todo {
  border-color: #28a745;
  background-color: #daf5da;
}

.todo-link {
  text-decoration: none;
  color: inherit;
  flex-grow: 1;
}

.todo-link:hover {
  text-decoration: none;
}

.button-group {
  display: flex;
  gap: 5px;
  margin-top: 5px;
}

button {
  padding: 8px 12px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s ease;
}

button:hover {
  background-color: #0056b3;
}

.complete-btn {
  background-color: #28a745;
}

.complete-btn:hover {
  background-color: #218838;
}

button:disabled {
  background-color: gray;
  cursor: not-allowed;
}

.pagination {
  text-align: center;
  margin-top: 20px;
}

.pagination > button {
  margin: 0 5px;
}

.create-button-container {
  max-width: 600px;
  margin: 20px auto;
  text-align: center;
}

.add-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.add-button:hover {
  background-color: #218838;
}
</style>