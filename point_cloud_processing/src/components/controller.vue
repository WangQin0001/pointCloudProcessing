<template>
<div>
  <div>
    <el-button type="primary" icon="el-icon-arrow-left" @click="turnRight">Turn Left</el-button>
    <el-button type="primary" @click="turnLeft">Turn Right<i class="el-icon-arrow-right el-icon--right"></i></el-button>
  </div>
</div>
</template>


<script>

export default {
  components:{},
  data(){
    return{

    }
  },
  methods:{
    turnRight(){
      console.log("turn right")
    },
    turnLeft(){
      console.log("turn left")
    }
  }
}
</script>



<style scoped>

</style>