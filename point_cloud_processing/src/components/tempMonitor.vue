<template>
  <div class="container">
    <p style="color: #409EFF">CPU Temperature：{{ temperature }} °C</p>
  </div>
</template>

<script>
import {tempMonitor} from "@/network/controller";

export default {
  components: {},
  data() {
    return {
      temperature: 0
    }
  },
  created() {
    this.fetchTemperature();
    setInterval(this.fetchTemperature, 300000);
  },
  methods: {
    fetchTemperature() {
      tempMonitor().then(res => {
        this.temperature = res; // 假设后端直接返回温度值
        // this.$message({
        //   message: `Renew temperature: ${this.temperature} °C`,
        //   type: 'success',
        //   duration: 2000
        // });
      }).catch(error => {
        console.log('Get CPU temperature failed')
      });
    }
  }
}
</script>

<style scoped>
</style>
