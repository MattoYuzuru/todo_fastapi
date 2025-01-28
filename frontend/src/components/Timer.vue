<template>
  <div class="timer">
    <h2>{{ formattedTime }}</h2>
    <div class="controls">
      <button @click="startTimer" :disabled="isRunning">Start</button>
      <button @click="pauseTimer" :disabled="!isRunning">Pause</button>
      <button @click="resetTimer">Reset</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    initialTime: {
      type: Number,
      default: 25 * 60, // Default to 25 minutes in seconds
    },
  },
  data() {
    return {
      timeLeft: this.initialTime,
      isRunning: false,
      timer: null,
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60)
          .toString()
          .padStart(2, '0');
      const seconds = (this.timeLeft % 60).toString().padStart(2, '0');
      return `${minutes}:${seconds}`;
    },
  },
  methods: {
    startTimer() {
      if (!this.isRunning) {
        this.isRunning = true;
        this.timer = setInterval(() => {
          if (this.timeLeft > 0) {
            this.timeLeft--;
          } else {
            this.stopTimer();
            alert('Time is up!');
          }
        }, 1000);
      }
    },
    pauseTimer() {
      this.stopTimer();
    },
    resetTimer() {
      this.stopTimer();
      this.timeLeft = this.initialTime;
    },
    stopTimer() {
      clearInterval(this.timer);
      this.isRunning = false;
    },
  },
};
</script>

<style scoped>
.timer {
  text-align: center;
}

h2 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.controls button {
  margin: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
}
</style>
