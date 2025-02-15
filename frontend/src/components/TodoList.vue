<template>
  <div>
    <div class="container">
      <h2>Your ToDos</h2>
      <ul v-if="todos.length" class="list-group mt-4">
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
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
          <span>Page {{ currentPage }}</span>
          <button @click="nextPage" :disabled="todos.length < limit">Next</button>
        </div>
      </ul>
      <p v-else class="no-todos">There are no todos yet.</p>
    </div>
    <div class="create-button-container">
      <router-link to="/todos/create">
        <button class="all-button">📃 Add New Todo</button>
      </router-link>
      <router-link to="/">
        <button class="all-button">Home Page</button>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      todos: [],
      currentPage: 1,
      limit: 10,
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
    authToken() {
      return localStorage.getItem('token');
    }
  },
  async mounted() {
    if (!this.authToken) {
      this.$router.push('/login');
      return;
    }
    await this.fetchTodos();
  },
  methods: {
    async fetchTodos() {
      try {
        const skip = (this.currentPage - 1) * this.limit;
        const response = await axios.get(`http://localhost:8000/todos/all/?skip=${skip}&limit=${this.limit}`, {
          headers: {
            Authorization: `Bearer ${this.authToken}`
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
          headers: { Authorization: `Bearer ${this.authToken}` }
        });
        await this.fetchTodos();
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
    async markCompleted(todoId) {
      try {
        await axios.post(`http://localhost:8000/todos/${todoId}/complete`, {}, {
          headers: { Authorization: `Bearer ${this.authToken}` }
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
* {
  font-family: Andale Mono, monospace;
}

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
  flex-direction: column;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 8px;
  transition: background-color 0.2s ease-in-out;
}

.list-group-item:hover {
  background-color: #f9f9f9;
}

.completed-todo {
  border-color: #4caf50;
  background-color: #e8f5e9;
}

.todo-link {
  text-decoration: none;
  color: #333;
  flex-grow: 1;
  font-weight: 500;
}

.todo-link:hover {
  text-decoration: underline;
}

.todo-title {
  font-size: 18px;
  font-weight: bold;
  color: #212121;
}

.todo-description {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.button-group {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

button {
  padding: 8px 14px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease-in-out;
}

.complete-btn {
  background-color: #4caf50;
  color: white;
}

.complete-btn:hover {
  background-color: #388e3c;
}

button:nth-child(2) {
  background-color: #f44336;
  color: white;
}

button:nth-child(2):hover {
  background-color: #d32f2f;
}

button:disabled {
  background-color: #bdbdbd;
  cursor: not-allowed;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  background-color: #007bff;
  color: white;
}

.pagination button:hover {
  background-color: #0056b3;
}

.create-button-container {
  text-align: center;
  margin-top: 20px;
}

.all-button {
  margin: 2px;
  display: inline-block;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.all-button:hover {
  background-color: #388e3c;
}

.no-todos {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: #757575;
}
</style>
