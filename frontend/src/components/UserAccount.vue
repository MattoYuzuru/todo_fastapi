<template>
  <div class="container">
    <nav class="nav-bar">
      <router-link to="/">Home</router-link>
      <button @click="logout">Logout</button>
    </nav>

    <div class="account-section">
      <h1>Account Settings</h1>
      <div v-if="user">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Current Streak:</strong> {{ user.current_streak }}</p>
        <p><strong>Longest Streak:</strong> {{ user.longest_streak }}</p>
        <p><strong>Pomodoro Sessions:</strong> {{ user.pomodoro_sessions }}</p>
        <p><strong>Tasks Completed:</strong> {{ user.tasks_completed }}</p>
      </div>

      <h2>Update Email</h2>
      <input v-model="email" type="email" placeholder="New Email" />
      <button @click="updateEmail">Update Email</button>

      <h2>Change Password</h2>
      <input v-model="password" type="password" placeholder="New Password" />
      <button @click="updatePassword">Update Password</button>

      <h2>Danger Zone</h2>
      <button class="delete-button" @click="showDeletePopup = true">Delete Account</button>
    </div>

    <div v-if="showDeletePopup" class="popup">
      <p>Are you sure you want to delete your account? This action is irreversible.</p>
      <button @click="deleteAccount">Yes, Delete</button>
      <button @click="showDeletePopup = false">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: null,
      email: '',
      password: '',
      showDeletePopup: false,
    };
  },
  async mounted() {
    await this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await axios.get('http://localhost:8000/users/me/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async updateEmail() {
      try {
        await axios.put(`http://localhost:8000/users/${this.user.id}`, { email: this.email }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert('Email updated successfully');
        await this.fetchUserData();
      } catch (error) {
        console.error('Error updating email:', error);
      }
    },
    async updatePassword() {
      try {
        await axios.put(`http://localhost:8000/users/${this.user.id}`, { password: this.password }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert('Password updated successfully');
      } catch (error) {
        console.error('Error updating password:', error);
      }
    },
    async deleteAccount() {
      try {
        await axios.delete(`http://localhost:8000/users/${this.user.id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        localStorage.removeItem('token');
        this.$router.push('/');
      } catch (error) {
        console.error('Error deleting account:', error);
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  }
};
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}
.nav-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.account-section {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
}
.delete-button {
  background-color: red;
  color: white;
}
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border: 1px solid #ccc;
  box-shadow: 0px 0px 10px #ccc;
}
</style>
