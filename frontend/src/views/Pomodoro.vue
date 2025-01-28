<template>
  <div class="pomodoro">
    <h1>Pomodoro Timer</h1>

    <div class="timer">
      <p v-if="timerActive">Time left: {{ formattedTime }}</p>
      <p v-else>Pomodoro completed: {{ completedCycles }} cycles</p>
    </div>

    <div class="controls">
      <button @click="startTimer" v-if="!timerActive">Start</button>
      <button @click="pauseTimer" v-if="timerActive">Pause</button>
      <button @click="resetTimer" v-if="!timerActive && completedCycles > 0">Reset</button>
    </div>

    <div class="cycle-info">
      <p>Break: {{ breakDuration }} minutes</p>
      <p>Work: {{ workDuration }} minutes</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      workDuration: 25, // Work time in minutes
      breakDuration: 5, // Break time in minutes
      timeLeft: 25 * 60, // Time left in seconds
      timerActive: false, // Whether the timer is running
      interval: null, // Reference to the setInterval
      completedCycles: 0, // Track number of completed Pomodoro cycles
    };
  },
  computed: {
    // Format time to mm:ss
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    },
  },
  methods: {
    startTimer() {
      if (!this.timerActive) {
        this.timerActive = true;
        this.interval = setInterval(this.countdown, 1000);
      }
    },
    pauseTimer() {
      clearInterval(this.interval);
      this.timerActive = false;
    },
    resetTimer() {
      clearInterval(this.interval);
      this.timerActive = false;
      this.timeLeft = this.workDuration * 60; // Reset to work duration
    },
    countdown() {
      if (this.timeLeft > 0) {
        this.timeLeft--;
      } else {
        this.handleCycleCompletion();
      }
    },
    handleCycleCompletion() {
      clearInterval(this.interval);
      this.completedCycles++;
      alert(`Pomodoro ${this.completedCycles} completed!`);

      // Toggle between work and break periods
      if (this.completedCycles % 2 === 0) {
        this.timeLeft = this.workDuration * 60; // Start work period
      } else {
        this.timeLeft = this.breakDuration * 60; // Start break period
      }

      // Start the next cycle automatically
      this.startTimer();
    },
  },
};
</script>

<style scoped>
.pomodoro {
  text-align: center;
  max-width: 400px;
  margin: 0 auto;
}

.timer {
  font-size: 2em;
  margin-bottom: 20px;
}

.controls button {
  font-size: 1.2em;
  margin: 10px;
  padding: 10px 20px;
}

.cycle-info {
  margin-top: 20px;
}
</style>
