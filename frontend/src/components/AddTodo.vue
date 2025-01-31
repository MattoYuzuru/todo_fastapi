<template>
  <div class="add-todo">
    <h2>Add New Task</h2>
    <input v-model="title" placeholder="Task Title"/>
    <textarea v-model="description" placeholder="Task Description"></textarea>
    <button @click="addTodo">Add Task</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      title: '',
      description: '',
    };
  },
  methods: {
    async addTodo() {
      try {
        await axios.post('http://localhost:8000/todos', {
          title: this.title,
          description: this.description,
        }, {
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
.add-todo {
  padding: 20px;
}
</style>
