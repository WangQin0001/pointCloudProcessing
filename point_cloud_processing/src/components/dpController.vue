<template xmlns="http://www.w3.org/1999/html">
  <div>
      <el-link type="primary" @click="startDp">start caculate the 3D model</el-link>
      <br>
  </div>
</template>


<script>

import {startDp} from "@/network/dpController";

export default {
  components: {},
  data() {
    return {

    }
  },
  methods: {
    startDp() {
      startDp().then(res => {
        this.$message.success("start to calculate!")
        console.log(res)
      }).catch(error => {
        console.log(error)
      })
    },

  }
}
</script>


<style scoped>

.input-container {
  display: flex;
  justify-content: space-between; /* Adjusts the space between the input fields */
  width: 80%; /* Reduces the width of the input container to 50% of its parent. Adjust as needed. */
  height: 40%;
  margin: 0 auto; /* Centers the container */
}

.input-item {
  flex: 1;
  margin-right: 10px;
  max-width: 100px;
}


.input-item:last-child {
  margin-right: 0;
}
</style>
