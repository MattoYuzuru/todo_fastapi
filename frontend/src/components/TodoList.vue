<template>
  <div class="container">
    <h2>Your ToDos</h2>
    <ul class="todo-list">
      <li v-for="todo in todos" :key="todo.id"
          class="todo-item"
          :class="{ completed: todo.status === 'Completed' }">
        <div class="todo-content">
          <router-link :to="'/todos/' + todo.id" class="todo-link">
            <h3>{{ todo.title }}</h3>
            <p>{{ todo.description }}</p>
            <p><strong>Priority:</strong> {{ todo.priority }}</p>
            <p><strong>Pomodoro Sessions:</strong> {{ todo.pomodoro_sessions }}</p>
          </router-link>
        </div>
        <div class="todo-actions">
          <button v-if="todo.status !== 'Completed'" @click="markCompleted(todo.id)" class="complete-btn">
            Complete
          </button>
          <button @click="deleteTodo(todo.id)" class="delete-btn">Delete</button>
        </div>
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
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        this.todos = response.data;
      } catch (error) {
        console.error("Error fetching todos:", error.response ? error.response.data : error);
      }
    },
    async deleteTodo(todoId) {
      try {
        await axios.delete(`http://localhost:8000/todos/${todoId}`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        this.todos = this.todos.filter(todo => todo.id !== todoId);
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
    async markCompleted(todoId) {
      try {
        await axios.post(`http://localhost:8000/todos/${todoId}/complete`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        const todo = this.todos.find(todo => todo.id === todoId);
        if (todo) todo.status = "Completed";
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
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.todo-list {
  list-style: none;
  padding: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  border: 2px solid black;
  border-radius: 8px;
  transition: background 0.3s ease;
}

.todo-item.completed {
  background-color: #d4edda; /* Light green */
  border-color: #28a745;
}

.todo-content {
  flex: 1;
}

.todo-link {
  text-decoration: none;
  color: black;
}

.todo-actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

.complete-btn {
  background: #007bff;
  color: white;
}

.complete-btn:hover {
  background: #0056b3;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #b02a37;
}
</style>
