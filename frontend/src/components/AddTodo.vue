<template>
  <div class="add-todo">
    <h2>Create New Todo</h2>
    <form @submit.prevent="createTodo">
      <label>Title:</label>
      <input v-model="todo.title" required/>

      <label>Description:</label>
      <textarea v-model="todo.description" required></textarea>

      <label>Status:</label>
      <select v-model="todo.status">
        <option value="Pending">Pending</option>
        <option value="Postpone">Postpone</option>
        <option value="In-progress">In Progress</option>
        <option value="Completed">Completed</option>
      </select>

      <label>Priority:</label>
      <select v-model="todo.priority">
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>

      <label>Due Date:</label>
      <input type="date" v-model="todo.due_date"/>

      <label>Pomodoro Sessions:</label>
      <input type="number" v-model="todo.pomodoro_sessions" min="0"/>

      <label>Total Time Spent (minutes):</label>
      <input type="number" v-model="todo.total_time_spent" min="0"/>

      <label>Current Streak (days):</label>
      <input type="number" v-model="todo.current_streak" min="0"/>

      <button type="submit" class="submit-btn">Create Todo</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      todo: {
        title: "",
        description: "",
        status: "Pending",
        priority: "Medium",
        due_date: "",
        pomodoro_sessions: 0,
        total_time_spent: 0,
        current_streak: 0
      }
    };
  },
  methods: {
    async createTodo() {
      try {
        await axios.post("http://localhost:8000/todos/", this.todo, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        this.$router.push("/");
      } catch (error) {
        console.error("Error creating todo:", error.response ? error.response.data : error);
      }
    }
  }
};
</script>

<style scoped>
.add-todo {
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

form {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-top: 10px;
}

input,
textarea,
select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-top: 5px;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

button {
  padding: 10px;
  margin-top: 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
}

.submit-btn {
  background: #007bff;
  color: white;
}

.submit-btn:hover {
  background: #0056b3;
}
</style>
