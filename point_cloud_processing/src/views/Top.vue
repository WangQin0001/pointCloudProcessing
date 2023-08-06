<template>
  <div id="top">
    <el-menu
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
<!--      <el-menu-item index="1" @click="getUsername" >test</el-menu-item>-->
      <el-menu-item index="3" v-show="this.point1[0] !== 0">{{ `X: ${point1[0]}, Y: ${point1[1]}, Z: ${point1[2]}`}}</el-menu-item>
      <el-menu-item index="3" v-show="this.point2[0] !== 0">{{ `X: ${point2[0]}, Y: ${point2[1]}, Z: ${point2[2]}` }}</el-menu-item>


      <el-menu-item index="4" @click="getDistance">{{ content }}</el-menu-item>

      <div style="display: flex; margin-left: auto;">
        <el-menu-item v-show="this.username">{{"Welcome "+this.username + "!"}}</el-menu-item>
        <el-menu-item index="2" @click="logout" v-show="this.username">Logout</el-menu-item>
      </div>
    </el-menu>
  </div>
</template>


<script>
import {logout,getUsername} from '../network/loginAndRegister'
import { mapMutations,mapState } from 'vuex';

export default {
  data() {
    return {
      username:'',
      distance: null,
    };
  },
  computed: {
    content() {
      if (this.username == null){
        return 'Welcome To PointCloud System'
      }else {
        return 'Get Distance'
      }
    },
    ...mapState(['point1', 'point2']),

    // distanceText: {
    //
    //   get() {
    //     if (this.distance === null || this.distance === 0) {
    //       return 'Get Distance';
    //     }
    //     else {
    //       // reset points
    //
    //       return `Distance: ${this.distance}`;
    //     }
    //   },
    //   set(newValue) {
    //     // Do nothing, we only need the getter to return a value
    //   },
    // },
  },
  watch: {
    point1: {
      handler() {
        // 当point1更新时，将距离重置为null，以便重新计算距离
        this.distance = null;
      },
      deep: true,
    },
    point2: {
      handler() {
        // 当point2更新时，将距离重置为null，以便重新计算距离
        this.distance = null;
      },
      deep: true,
    },
  },
  created() {
    this.getUsername()
  },
  methods: {
    ...mapMutations(['setPoint1', 'setPoint2']),

    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    getDistance(){
      const dx = this.point2[0] - this.point1[0];
      const dy = this.point2[1] - this.point1[1];
      const dz = this.point2[2] - this.point1[2];
      const distance = Math.sqrt(dx * dx + dy * dy + dz * dz).toFixed(2);
      this.distance = distance
      this.$message.success("Distance: "+ this.distance)
      // reset points
      this.setPoint1(new Float32Array(3));
      this.setPoint2(new Float32Array(3));

      console.log('Distance:', distance);
    },
    logout(){
      logout().then(res=>{
        this.$message.success("logout success!")
        this.$router.push('/login')
      }).catch(error=>{
        console.log(error)
      })
    },
    getUsername(){
      getUsername().then(res=>{
        this.username = res.data.data
      }).catch(error=>{
        console.log(error)
      })

    }
  }
}
</script>


<style>

</style>