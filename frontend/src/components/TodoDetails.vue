<template>
  <div class="todo-details">
    <h2>{{ todo.title }}</h2>
    <p>{{ todo.description }}</p>
    <button @click="markCompleted">Mark as Completed</button>
    <button @click="deleteTodo">Delete</button>
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
        const response = await axios.get("http://localhost:8000/todos/all", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        this.todos = response.data;
      } catch (error) {
        console.error(
            "Error fetching todos:",
            error.response ? error.response.data : error
        );
      }
    },
    async deleteTodo() {
      try {
        await axios.delete(`http://localhost:8000/todos/${this.id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        await this.$router.push('/');
      } catch (error) {
        console.error(error);
      }
    },
    async markCompleted() {
      try {
        await axios.post(`http://localhost:8000/todos/${this.id}/complete`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        await this.$router.push('/');
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.todo-details {
  padding: 20px;
}
</style>
