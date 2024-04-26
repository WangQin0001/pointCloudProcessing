<template>
  <div class="container">
    <el-link type="primary" @click="startProgress">AUTO START</el-link>
    <el-dialog title="Progress" :visible.sync="showProgress">
      <el-progress :percentage="progress"></el-progress>
    </el-dialog>
  </div>
</template>

<script>
import { startTask, fetchProgress } from '@/network/controller';

export default {
  data() {
    return {
      progress: 0,
      showProgress: false,
      intervalId: null
    };
  },
  methods: {
    pollProgress() {
      fetchProgress()
          .then(response => {
            this.progress = response.data;
            if (this.progress >= 100) {
              clearInterval(this.intervalId);
              setTimeout(() => {
                this.showProgress = false;  // Hide the progress bar after 2 seconds when complete
              }, 2000);
            }
          })
          .catch(error => {
            console.error("Error fetching progress:", error);
            this.$message.error('Failed to fetch progress!');
          });
    },
    startProgress() {
      this.progress = 0; // Reset progress
      startTask()
          .then(() => {
            this.showProgress = true;  // Show progress bar dialog
            this.intervalId = setInterval(this.pollProgress, 1000);
          })
          .catch(error => {
            console.error("Error starting task:", error);
            this.$message.error('Failed to start the task!');
          });
    }
  }
}
</script>

<style scoped>
/* Style as needed */
</style>
