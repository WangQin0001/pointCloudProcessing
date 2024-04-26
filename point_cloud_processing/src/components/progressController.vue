<template>
  <div>
    <el-progress :percentage="progress" />
    <button @click="startProgress">开始任务</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      progress: 0,
      intervalId: null
    };
  },
  methods: {
    fetchProgress() {
      axios.get('/api/progress')
        .then(response => {
          this.progress = response.data;
          if (this.progress >= 100) {
            clearInterval(this.intervalId);
            this.intervalId = null;
          }
        })
        .catch(error => {
          console.error("Error fetching progress:", error);
        });
    },
    startProgress() {
      // 重置进度
      this.progress = 0;
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      // 启动任务（需要后端支持启动任务的API）
      axios.post('/api/start-task')
        .then(() => {
          this.intervalId = setInterval(this.fetchProgress, 1000);
        })
        .catch(error => {
          console.error("Error starting task:", error);
        });
    }
  }
}
</script>
