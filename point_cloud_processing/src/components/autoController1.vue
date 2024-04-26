<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
      <el-link type="primary" @click="auto">AUTO START</el-link>
  </div>
</template>


<script>

import {auto} from "@/network/controller";

export default {
  components: {},
  data() {
    return {
    }
  },
  methods: {
    auto() {
      auto().then(res=>{
        this.$message.success("START !")
        console.log(res)
      }).catch(error=>{
        console.log(error)
      })
    },
  }
}
</script>


<style scoped>

</style>
