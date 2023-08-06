<template>
  <div ref="webgl" class="canvas">
  </div>
</template>

<script>
import { renderer } from "./threejs/main04gsap.js";//将渲染器引入


export default {
  name: "threeTest",
  created: function () {
    // this.$refs.webgl.appendChild(renderer.domElement);//不可以
    // Three.js渲染结果Canvas画布插入到body元素中
    // document.body.appendChild(renderer.domElement);//可以访问body
  },
  mounted: function () {
    this.$refs.webgl.appendChild(renderer.domElement);
    // // Three.js渲染结果Canvas画布插入到body元素中
    // document.body.appendChild(renderer.domElement);
  },
};
</script>

<style scoped>
.canvas{
  margin-top:100px;
  margin-left:150px;
}
</style>
