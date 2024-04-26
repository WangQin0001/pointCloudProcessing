<template>
  <div class="container">
    <el-link type="primary" @click="autoStart">AUTO START</el-link>
    <br>
    <br>
    <!-- showProgressButton 控制显示隐藏 -->
    <el-link v-if="showProgressButton" type="primary" @click="toggleProgressDialog">show progress</el-link>
      <el-dialog
        title="Progress of Calculation"
        :visible.sync="dialogVisible"
        custom-class="custom-dialog"
    >
      <el-progress :percentage="progress"></el-progress>
      <template #footer>
        <div class="dialog-footer">
          Limited by equipment performance the calculation time is long.
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { auto, fetchProgress } from '@/network/controller';

export default {
  data() {
    return {
      progress: 0,
      dialogVisible: false,
      showProgressButton: false,
      intervalId: null,
      isCalculating: false // State to keep track of calculation status
    };
  },
  created() {
    this.checkCalculationStatus();
  },
  methods: {
    checkCalculationStatus() {
      // Check if a calculation was previously marked as running
      const isCalcRunning = localStorage.getItem('isCalculating') === 'true';
      this.isCalculating = isCalcRunning;
      if (isCalcRunning) {
        // If a calculation is running, set up the environment as if the AUTO button had been pressed
        this.showProgressButton = true;
        this.startPolling();
      }
    },
    startPolling() {
      // Initialize polling for progress
      this.intervalId = setInterval(() => {
        this.pollProgress();
      }, 3000);
    },
    pollProgress() {
      console.log("开始执行pollProgress");
      fetchProgress()
          .then(res => {
            console.log("成功获取进度:", res);
            this.progress = res;
            if (this.progress >= 100) {
              clearInterval(this.intervalId);
              this.dialogVisible = false;
              this.showProgressButton = false;
              localStorage.setItem('isCalculating', 'false');
              this.isCalculating = false;
              this.$message.success("Automated calculation completed!");
            }
          })
          .catch(error => {
            console.error("获取进度时发生错误:", error);
          });
    },
    autoStart() {
      if (this.isCalculating) {
        this.$message.error('A calculation is already in progress. Please wait until it completes.');
        return;
      }
      this.isCalculating = true;
      localStorage.setItem('isCalculating', 'true');
      this.showProgressButton = true;
      this.progress = 0;
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      this.startPolling();
      auto().then(res => {
        this.$message.success("Automatic calculation completed!");
        localStorage.setItem('isCalculating', 'false');
        this.isCalculating = false;
      }).catch(error => {
        localStorage.setItem('isCalculating', 'false');
        this.isCalculating = false;
        console.error("启动自动化计算时发生错误:", error);
        this.$message.error('Failed to start AUTO!');
      });
    },
    toggleProgressDialog() {
      this.dialogVisible = !this.dialogVisible;
    }
  }
}

</script>


<style scoped>
  .custom-dialog {
    border-radius: 10px; /* 设置圆角 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  }

  .dialog-footer {
    text-align: right;
    font-size: 12px;
    color: #888;
    padding-right: 20px; /* 增加右边距以调整文本位置 */
  }
</style>
