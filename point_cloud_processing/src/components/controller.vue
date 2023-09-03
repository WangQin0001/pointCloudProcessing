<template xmlns="http://www.w3.org/1999/html">
  <div>
    <div>
      <el-link type="primary" @click="offsetPosition">Goto offset position</el-link>
      <br>
      <el-link type="primary" @click='captureCurrentImage'>Capture images in current position</el-link>
      <br>
      <el-link type="primary" @click="captureSurroundingImage">Capture images of the surrounding scenes</el-link>
      <br>
      <el-link type="primary" @click="manualRotate">Manual rotate</el-link>
      <br>
      <el-link type="primary"></el-link>
    </div>
  </div>
</template>


<script>

import {offsetPosition,captureCurrentImage,captureSurroundingImage,manualRotate} from "@/network/controller";

export default {
  components: {},
  data() {
    return {}
  },
  methods: {
    offsetPosition() {
      offsetPosition().then(res => {
        this.$message.success("Offset Position sucess!")
        console.log(res)
      }).catch(error => {
        console.log(error)
      })
    },

    captureCurrentImage() {
      captureCurrentImage().then(res=>{
        this.$message.success("captureCurrentImage sucess!")
        console.log(res)
      }).catch(error=>{
        console.log(error)
      })
    },

    captureSurroundingImage() {
      captureSurroundingImage().then(res=>{
        this.$message.success("captureSurroundingImage sucess!")
        console.log(res)
      }).catch(error=>{
        console.log(error)
      })
    },

    manualRotate() {
      manualRotate().then(res=>{
        this.$message.success("ManualRotate sucess!")
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