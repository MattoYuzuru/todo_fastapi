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
      await axios.post('/todos', {
        title: this.title,
        description: this.description,
      });
      this.$emit('todoAdded');
    },
  },
};
</script>

<style scoped>
.add-todo {
  padding: 20px;
}
</style>
