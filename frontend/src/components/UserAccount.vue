<template>
  <div class="container">
    <nav class="nav-bar">
      <router-link to="/">Home</router-link>
      <br>
      <button @click="logoutUser">Logout</button>
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
      <input v-model="email" type="email" placeholder="New Email"/>
      <button @click="updateEmail">Update Email</button>

      <h2>Change Password</h2>
      <input v-model="password" type="password" placeholder="New Password"/>
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
import {mapActions, mapGetters} from "vuex";
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      showDeletePopup: false,
    };
  },
  computed: {
    ...mapGetters(["getUser"]),
    user() {
      return this.getUser || {};
    }
  },
  methods: {
    ...mapActions(["fetchUser", "logout"]),

    async updateEmail() {
      try {
        await axios.put(`http://localhost:8000/users/${this.user.id}`, {email: this.email}, {
          headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}
        });
        alert("Email updated successfully");
        await this.fetchUser();
      } catch (error) {
        console.error("Error updating email:", error);
      }
    },

    async updatePassword() {
      try {
        await axios.put(`http://localhost:8000/users/${this.user.id}`, {password: this.password}, {
          headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}
        });
        alert("Password updated successfully");
      } catch (error) {
        console.error("Error updating password:", error);
      }
    },

    async deleteAccount() {
      try {
        await axios.delete(`http://localhost:8000/users/${this.user.id}`, {
          headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}
        });
        this.logoutUser();
      } catch (error) {
        console.error("Error deleting account:", error);
      }
    },

    logoutUser() {
      this.logout();
      this.$router.push("/login");
    }
  },
  async mounted() {
    await this.fetchUser();
  }
};
</script>


<style scoped>

* {
  font-family: Andale Mono, monospace;
}

.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border: 2px solid black;
}

.nav-bar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 5px;
  margin-bottom: 20px;
}

.nav-bar a,
.nav-bar button {
  text-decoration: none;
  color: black;
  font-weight: bold;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-bar a:hover,
.nav-bar button:hover {
  color: #007bff;
}

.account-section {
  text-align: center;
}

h1, h2 {
  font-size: 20px;
  margin-bottom: 15px;
}

.account-section p {
  text-align: left;
  margin: 5px 0;
  font-size: 16px;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  margin-top: 15px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
  font-weight: bold;
}

button:hover {
  opacity: 0.8;
}

button:not(.delete-button) {
  background: #007bff;
  color: white;
}

button:not(.delete-button):hover {
  background: #0056b3;
}

.delete-button {
  background: #dc3545;
  color: white;
}

.delete-button:hover {
  background: #b02a37;
}

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.popup p {
  margin-bottom: 15px;
  font-size: 16px;
}

.popup button {
  width: 48%;
  margin: 3px;
  display: inline-block;
}
</style>
