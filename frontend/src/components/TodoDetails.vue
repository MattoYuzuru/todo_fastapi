<template>
  <div class="todo-details">
    <h2>{{ todo.title }}</h2>
    <p>{{ todo.description }}</p>

    <div class="todo-info">
      <p><strong>Status:</strong> {{ todo.status }}</p>
      <p><strong>Priority:</strong> {{ todo.priority }}</p>
      <p v-if="todo.due_date"><strong>Due Date:</strong> {{ todo.due_date }}</p>
      <p v-if="todo.completed_at"><strong>Completed At:</strong> {{ todo.completed_at }}</p>
      <p><strong>Pomodoro Sessions:</strong> {{ todo.pomodoro_sessions }}</p>
      <p><strong>Total Time Spent:</strong> {{ formattedTotalTime }}</p>
      <p><strong>Current Streak:</strong> {{ todo.current_streak }} days</p>
    </div>

    <div class="timer">
      <h3>🍅Pomodoro Timer</h3>
      <p class="timer-display">{{ formattedTime }}</p>
      <button @click="startPomodoro" :disabled="isRunning">Start</button>
      <button @click="pausePomodoro" :disabled="!isRunning">Pause</button>
      <button @click="finishPomodoro" :disabled="!isRunning">Finish</button>
    </div>

    <button @click="markCompleted">Mark as Completed</button>
    <button @click="deleteTodo">Delete</button>
    <div class="all-todos-button">
      <router-link to="/todos/all/">
        <button class="add-button">Go back to Todos</button>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['id'],
  data() {
    return {
      todo: {},
      timeInSeconds: 0,
      isRunning: false,
      timerInterval: null,
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeInSeconds / 60);
      const seconds = this.timeInSeconds % 60;
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    },
    formattedTotalTime() {
      if (!this.todo.total_time_spent) return "0:00";
      const minutes = Math.floor(this.todo.total_time_spent / 60);
      const seconds = this.todo.total_time_spent % 60;
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
  },
  async mounted() {
    await this.fetchTodo();
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  },
  methods: {
    async fetchTodo() {
      try {
        const response = await axios.get(`http://localhost:8000/todos/${this.id}`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });
        this.todo = response.data;
      } catch (error) {
        console.error("Error fetching todo:", error);
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
        await this.fetchTodo();
      } catch (error) {
        console.error(error);
      }
    },
    async startPomodoro() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/start`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });

        this.isRunning = true;
        this.timerInterval = setInterval(() => {
          this.timeInSeconds++;
        }, 1000);
      } catch (error) {
        console.error("Error starting pomodoro:", error);
      }
    },
    async pausePomodoro() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/pause`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });

        this.isRunning = false;
        clearInterval(this.timerInterval);
      } catch (error) {
        console.error("Error pausing pomodoro:", error);
      }
    },
    async finishPomodoro() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/finish`, {}, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
        });

        this.isRunning = false;
        clearInterval(this.timerInterval);

        const secondsSpent = this.timeInSeconds;

        this.todo.total_time_spent += secondsSpent;
        this.todo.pomodoro_sessions += 1;
        this.timeInSeconds = 0;
      } catch (error) {
        console.error("Error finishing pomodoro:", error);
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

.todo-info {
  margin: 10px 0;
}

.todo-info p {
  margin: 5px 0;
}

.timer {
  text-align: center;
  margin-top: 20px;
}

.timer-display {
  font-size: 24px;
  font-weight: bold;
  margin: 10px 0;
}

.all-todos-button {
  max-width: 600px;
  margin: 20px auto;
  text-align: center;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

button:disabled {
  background: gray;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  opacity: 0.8;
}

button:nth-child(1) {
  background: #28a745;
  color: white;
}

button:nth-child(2) {
  background: #ffc107;
  color: black;
}

button:nth-child(3) {
  background: #dc3545;
  color: white;
}

</style>
