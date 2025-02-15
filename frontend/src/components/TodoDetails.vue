<template>
  <div class="todo-details">
    <h2>{{ todo.title }}</h2>
    <h4>{{ todo.description }}</h4>

    <div class="todo-info">
      <p><strong>Status:</strong> {{ todo.status }}</p>
      <p><strong>Priority:</strong> {{ todo.priority }}</p>
      <br>
      <p v-if="todo.due_date"><strong>Due Date:</strong> {{ todo.due_date }}</p>
      <p v-if="todo.completed_at"><strong>Completed At:</strong> {{ formattedCompletedAt }}</p>
      <br>
      <p><strong>Pomodoro Sessions:</strong> {{ todo.pomodoro_sessions }}</p>
      <p><strong>Total Time Spent:</strong> {{ formattedTotalTime }}</p>
      <p><strong>Current Streak:</strong> {{ todo.current_streak }} days</p>
    </div>

    <div class="timer">
      <h3>🍅 Pomodoro Timer</h3>
      <p class="timer-display">{{ formattedTime }}</p>
      <button @click="startPomodoro" :disabled="isRunning" class="start-btn">Start</button>
      <button @click="pausePomodoro" :disabled="!isRunning" class="pause-btn">Pause</button>
      <button @click="finishPomodoro" :disabled="!isRunning" class="finish-btn">Finish</button>
    </div>

    <button v-if="todo.status !== 'Completed'" @click="markCompleted">Mark as Completed</button>
    <button @click="deleteTodo">Delete</button>
    <div class="navigation-buttons">
      <router-link to="/">
        <button class="all-button">Go back to Menu</button>
      </router-link>
      <router-link to="/todos/all/">
        <button class="all-button">Go back to Todos</button>
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
      redisFetchInterval: null,
      startTime: null,
      accumulatedTime: 0,
    };
  },
  computed: {
    authToken() {
      return localStorage.getItem('token');
    },
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
    },
    formattedCompletedAt() {
      return this.todo.completed_at ? this.todo.completed_at.split("T")[0] : "N/A";
    }
  },
  async mounted() {
    if (!this.authToken) {
      this.$router.push('/login');
      return;
    }
    window.addEventListener("beforeunload", this.confirmReload);
    await this.fetchTodo();
    this.fetchPomodoroTime();
    this.redisFetchInterval = setInterval(this.fetchPomodoroTime, 30000);
  },
  beforeUnmount() {
    window.removeEventListener("beforeunload", this.confirmReload);
    clearInterval(this.timerInterval);
    clearInterval(this.redisFetchInterval);
  },
  methods: {
    async fetchTodo() {
      try {
        const response = await axios.get(`http://localhost:8000/todos/${this.id}`, {
          headers: {Authorization: `Bearer ${this.authToken}`}
        });
        this.todo = response.data;
      } catch (error) {
        console.error("Error fetching todo:", error);
      }
    },
    async deleteTodo() {
      try {
        await axios.delete(`http://localhost:8000/todos/${this.id}`, {
          headers: {Authorization: `Bearer ${this.authToken}`}
        });
        this.$router.push('/');
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
    async markCompleted() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/complete`, {}, {
          headers: {Authorization: `Bearer ${this.authToken}`}
        });
        await this.fetchTodo();
      } catch (error) {
        console.error("Error marking todo as completed:", error);
      }
    },
    confirmReload(event) {
      event.preventDefault();
      event.returnValue = "Do you want to reload the page? Changes you made may not be saved.";
    },
    async fetchPomodoroTime() {
      try {
        const response = await axios.get(`http://localhost:8000/todos/${this.id}/pomodoro/status`, {
          headers: {Authorization: `Bearer ${this.authToken}`}
        });
        this.timeInSeconds = response.data.elapsed_time;
        this.isRunning = response.data.is_running;
        this.accumulatedTime = Math.round(response.data.accumulated_time) || 0;
        if (this.isRunning) {
          this.startLocalTimer();
        } else {
          clearInterval(this.timerInterval);
        }
      } catch (error) {
        console.error("Error fetching Pomodoro time:", error);
      }
    },
    async startPomodoro() {
      try {
        const response = await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/start`, {}, {
          headers: {Authorization: `Bearer ${this.authToken}`}
        });
        this.isRunning = true;
        this.startTime = new Date(response.data.start_time);
        this.accumulatedTime = Math.round(response.data.accumulated_time) || 0;
        this.startLocalTimer();
      } catch (error) {
        console.error("Error starting pomodoro:", error);
      }
    },
    async pausePomodoro() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/pause`, {}, {
          headers: {Authorization: `Bearer ${this.authToken}`}
        });
        this.isRunning = false;
        clearInterval(this.timerInterval);
        const elapsedTime = (new Date() - this.startTime) / 1000;
        this.accumulatedTime += Math.round(elapsedTime);
        this.timeInSeconds = this.accumulatedTime;
        await this.fetchTodo();
      } catch (error) {
        console.error("Error pausing pomodoro:", error);
      }
    },
    async finishPomodoro() {
      try {
        const response = await axios.post(`http://localhost:8000/todos/${this.id}/pomodoro/finish`, {}, {
          headers: {Authorization: `Bearer ${this.authToken}`}
        });
        this.isRunning = false;
        clearInterval(this.timerInterval);
        this.timeInSeconds = 0;
        this.todo.total_time_spent += Math.round(response.data.elapsed_time);
        this.todo.pomodoro_sessions += 1;
        await this.fetchTodo();
      } catch (error) {
        console.error("Error finishing pomodoro:", error);
      }
    },
    startLocalTimer() {
      clearInterval(this.timerInterval);
      this.timerInterval = setInterval(() => {
        this.timeInSeconds = Math.round(this.accumulatedTime) + Math.floor((new Date() - this.startTime) / 1000);
        if (this.timeInSeconds >= 1500) {
          this.finishPomodoro();
        }
      }, 1000);
    },
  }
};
</script>

<style scoped>
* {
  font-family: Andale Mono, monospace;
}

.todo-details {
  max-width: 600px;
  margin: auto;
  padding: 24px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 2px solid #ddd;
}

h2 {
  text-align: center;
  margin-bottom: 10px;
}

.todo-info {
  margin: 15px 0;
  font-size: 16px;
}

.todo-info p {
  margin: 6px 0;
  color: #333;
}

.timer {
  text-align: center;
  margin-top: 20px;
}

.timer-display {
  font-size: 24px;
  font-weight: bold;
  color: #222;
  margin: 10px 0;
}

button {
  display: block;
  width: 100%;
  padding: 12px;
  margin-top: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  transition: background 0.3s ease-in-out;
}

button:disabled {
  background: #b9b9b9;
  cursor: not-allowed;
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
  background: #dc3545;
  color: white;
}

.finish-btn:hover {
  background: #c82333;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.all-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-align: center;
}

.all-button:hover {
  background-color: #0056b3;
}
</style>
