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
      <button @click="startPomodoro" :disabled="isRunning">Start</button>
      <button @click="pausePomodoro" :disabled="!isRunning">Pause</button>
      <button @click="finishPomodoro" :disabled="!isRunning">Finish</button>
    </div>

    <button @click="markCompleted">Mark as Completed</button>
    <button @click="deleteTodo">Delete</button>
    <router-link to="/todos/all/">
      <button class="all-button">Go back to Todos</button>
    </router-link>
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
    confirmReload(event) {
      event.preventDefault();
      event.returnValue = "Do you want to reload the page? Changes you made may not be saved.";
    },
    async fetchPomodoroTime() {
      try {
        const response = await axios.get(`http://localhost:8000/todos/${this.id}/pomodoro/status`, {
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
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
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
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
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
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
          headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
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
  background: #b9b9b9;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  opacity: 0.8;
}

button:nth-child(1) {
  background: #3ea9db;
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


.all-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4391dd;
  color: white;
  border: none;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.4s ease;
}

.all-button:hover {
  background-color: #2377c4;
}

</style>
