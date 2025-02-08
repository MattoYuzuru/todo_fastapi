<template>
  <div class="todo-details">
    <h2>{{ todo.title }}</h2>
    <p class="description">{{ todo.description }}</p>

    <div class="details">
      <p><strong>Status:</strong> {{ todo.status }}</p>
      <p><strong>Priority:</strong> {{ todo.priority }}</p>
      <p v-if="todo.due_date"><strong>Due Date:</strong> {{ todo.due_date }}</p>
      <p v-if="todo.completed_at"><strong>Completed At:</strong> {{ todo.completed_at }}</p>
      <p><strong>Pomodoro Sessions:</strong> {{ todo.pomodoro_sessions }}</p>
      <p><strong>Total Time Spent:</strong> {{ todo.total_time_spent }} minutes</p>
      <p><strong>Current Streak:</strong> {{ todo.current_streak }} days</p>
    </div>

    <div class="actions">
      <button v-if="todo.status !== 'Completed'" @click="markCompleted" class="complete-btn">Mark as Completed</button>
      <button @click="deleteTodo" class="delete-btn">Delete</button>
    </div>

    <div class="pomodoro-actions">
      <h3>Pomodoro Timer</h3>
      <button @click="startPomodoro" class="start-btn">Start</button>
      <button @click="pausePomodoro" class="pause-btn">Pause</button>
      <button @click="finishPomodoro" class="finish-btn">Finish</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['id'],
  data() {
    return {
      todo: {}
    };
  },
  async mounted() {
    await this.fetchTodo();
  },
  methods: {
    async fetchTodo() {
      try {
        const response = await axios.get(`http://localhost:8000/todos/${this.id}`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        this.todo = response.data;
      } catch (error) {
        console.error("Error fetching todo:", error.response ? error.response.data : error);
      }
    },
    async deleteTodo() {
      try {
        await axios.delete(`http://localhost:8000/todos/${this.id}`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        await this.$router.push('/');
      } catch (error) {
        console.error(error);
      }
    },
    async markCompleted() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/complete`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        this.todo.status = "Completed";
      } catch (error) {
        console.error(error);
      }
    },
    async startPomodoro() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/start`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
      } catch (error) {
        console.error("Error starting Pomodoro session:", error);
      }
    },
    async pausePomodoro() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/pause`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
      } catch (error) {
        console.error("Error pausing Pomodoro session:", error);
      }
    },
    async finishPomodoro() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/finish`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        this.todo.pomodoro_sessions += 1;
      } catch (error) {
        console.error("Error finishing Pomodoro session:", error);
      }
    }
  }
};
</script>

<style scoped>
.todo-details {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border: 2px solid black;
}

h2 {
  text-align: center;
}

.description {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
}

.details {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.actions {
  display: flex;
  justify-content: space-between;
}

.pomodoro-actions {
  text-align: center;
  margin-top: 20px;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
  margin-right: 10px;
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

.start-btn {
  background: #28a745;
  color: white;
}

.start-btn:hover {
  background: #218838;
}

.pause-btn {
  background: #ffc107;
  color: black;
}

.pause-btn:hover {
  background: #e0a800;
}

.finish-btn {
  background: #17a2b8;
  color: white;
}

.finish-btn:hover {
  background: #138496;
}
</style>
