<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <el-link type="primary" @click="offsetPosition">Goto offset position</el-link>
    <br>
    <br>
    <el-link type="primary" @click='captureCurrentImage'>Capture images in current position</el-link>
    <br>
    <br>
    <div class="input-container">
      <el-input
          placeholder="step"
          v-model="three.step"
          clearable
          class="input-item">
      </el-input>
      <el-input
          placeholder="dir"
          v-model="three.dir"
          clearable
          class="input-item">
      </el-input>
      <el-input
          placeholder="angle"
          v-model="three.angle"
          clearable
          class="input-item">
      </el-input>
    </div>

    <el-link type="primary" @click="captureSurroundingImage">Capture images of the surrounding scenes</el-link>
    <br>
    <br>
    <div class="input-container">
      <el-input
          placeholder="dir"
          v-model="four.dir"
          clearable
          class="input-item">
      </el-input>
      <el-input
          placeholder="angle"
          v-model="four.angle"
          clearable
          class="input-item">
      </el-input>
    </div>
    <el-link type="primary" @click="manualRotate">Manual rotate</el-link>
    <br>
    <el-link type="primary"></el-link>
  </div>
</template>


<script>

import {offsetPosition,captureCurrentImage,captureSurroundingImage,manualRotate} from "@/network/controller";

export default {
  components: {},
  data() {
    return {
      three:{
        methodName:3,
        step:'',
        dir:'',
        angle:'',
      },
      four:{
        methodName:4,
        step:'0',
        dir:'',
        angle:'',
      }
    }
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
      captureSurroundingImage(this.three.methodName,this.three.step,this.three.dir,this.three.angle).then(res=>{
        this.$message.success("captureSurroundingImage sucess!")
        console.log(res)
      }).catch(error=>{
        console.log(error)
      })
    },

    manualRotate() {
      manualRotate(this.four.methodName,this.four.step,this.four.dir,this.four.angle).then(res=>{
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
.container{
  max-width: 400px;
}

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
