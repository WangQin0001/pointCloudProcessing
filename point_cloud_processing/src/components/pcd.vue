<template>
  <div class="container">
    <top ref="top" class="top"></top>
    <div id="webgl" class="canvas" ref="div"></div>
    <controller class="controller"></controller>
  </div>

</template>

<script>
import top from '../views/Top.vue';
import controller from "@/components/controller.vue";
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import loadModel  from './utils/model.js'; // import pcd model
import {throttle} from 'lodash';
import { mapMutations,mapState } from 'vuex';

// const CAMERA_POSITION = new THREE.Vector3(340, 410, 550);
const CAMERA_POSITION = new THREE.Vector3(10, 10, 10);

// const CAMERA_LOOK_AT = new THREE.Vector3(-109, 36, -85);
const CAMERA_LOOK_AT = new THREE.Vector3(0,0,0);

const THRESHOLD = 0.01//精度


export default {
  components: {
    top,
    controller
  },
  data() {
    return {
      model: null,
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      mouse: new THREE.Vector2(),
      raycaster: new THREE.Raycaster(),
      previousIndex: null,
      previousColor: new THREE.Color(),
      clock: new THREE.Clock(),
      FPS: 120,
      timeS: 0,
      topHeight:0,
    };
  },

  computed: {
    ...mapState(['point1', 'point2','isAuthenticated']),
  },

  beforeDestroy() {
    this.removeEventListeners();
  },
  watch: {
    isAuthenticated(loggedIn) {
      if (loggedIn) {
        this.initPointCloud();
      } else {
        this.clearPointCloud();
      }
    },
  },

  mounted() {
    if (this.$store.state.isAuthenticated) {
      // 用户已登录，初始化点云数据
      this.initPointCloud();
    }

  },
  methods: {
    ...mapMutations(['setPoint1', 'setPoint2']),

    initPointCloud(){
      this.setTopHeight();
      this.initScene();
      this.initCamera();
      this.initRenderer();
      this.initControls();
      this.initEventListeners();

      // 使用 loadModel 函数加载模型
      loadModel((loadedModel) => {
        this.model = loadedModel; // 将加载的模型存储在组件的数据属性中
        this.scene.add(this.model); // 添加模型到场景
        this.$refs.div.appendChild(this.renderer.domElement);
        this.animate(); // 开始渲染循环
      });
    },

    // 清除点云数据的代码
    clearPointCloud() {
      if (this.scene) {
        // 清除场景中的所有子项
        while(this.scene.children.length > 0){
          this.scene.remove(this.scene.children[0]);
        }
        this.$store.commit('setPoint1', new Float32Array(3));
        this.$store.commit('setPoint2', new Float32Array(3));
      }
    },

    removeEventListeners() {
      document.removeEventListener('mousemove', this.onMouseMove);
      document.removeEventListener('mouseup', this.onMouseUp);
    },

    setTopHeight() {
      this.$nextTick(() => {
        const topComponent = this.$refs.top.$el; // Change this line
        if (topComponent) {
          this.topHeight = topComponent.offsetHeight;
        }
      });
    },

    initScene() {
      this.scene = new THREE.Scene();

      const axesHelper = new THREE.AxesHelper(4);
      // axesHelper.position.set(-109, 36, -85);
      axesHelper.position.set(0,0,0);

      this.scene.add(axesHelper);
    },
    initCamera() {
      this.camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight, 1, 3000);
      this.camera.position.copy(CAMERA_POSITION);
      this.camera.lookAt(CAMERA_LOOK_AT);
    },
    initRenderer() {
      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    },
    initControls() {
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.target.copy(CAMERA_LOOK_AT);
    },
    initEventListeners() {
      window.addEventListener('resize', this.onWindowResize);
      document.addEventListener('mousemove', throttle(this.onMouseMove, 10));
      // document.addEventListener('mousedown', this.onMouseDown);
      document.addEventListener('mouseup', this.onMouseUp);
    },
    onWindowResize() {
      this.renderer.setSize(window.innerWidth,window.innerHeight);
      this.camera.aspect = window.innerWidth/window.innerHeight;
      this.camera.updateProjectionMatrix();
    },
    onMouseMove(event) {
      event.stopPropagation();
      // event.preventDefault();
      this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      this.mouse.y = -((event.clientY - this.topHeight) / window.innerHeight) * 2 + 1;
      this.highlightPointUnderMouse(event);
    },
    onMouseUp(event) {
      event.stopPropagation();
      event.preventDefault();

      this.highlightPointUnderMouse(event, true);
    },
    highlightPointUnderMouse(event,isMouseDown = false) {
      // if (event.buttons !== 1) return; // 鼠标未按下左键，不执行任何操作
      // if (event.type !== 'click') return; // 不是单次点击事件，不执行任何操作
      this.raycaster.params.Points.threshold = THRESHOLD;


      this.raycaster.setFromCamera(this.mouse, this.camera);
      const intersects = this.raycaster.intersectObjects(this.model.children);
      if (intersects.length > 0) {
        const index = intersects[0].index;
        const pointModel = this.model.children[0];

        if (this.previousIndex !== null) {
          this.updatePreviousPoint(pointModel, this.previousIndex, this.previousColor);
        }

        this.highlightPoint(pointModel, index);
        pointModel.geometry.attributes.customSize.needsUpdate = true;
        pointModel.geometry.attributes.customColor.needsUpdate = true;
        this.previousIndex = index;

        // check if the mouse button was clicked
        if (isMouseDown) {
          const point = [
            pointModel.geometry.attributes.position.array[index * 3].toFixed(2),
            pointModel.geometry.attributes.position.array[index * 3 + 1].toFixed(2),
            pointModel.geometry.attributes.position.array[index * 3 + 2].toFixed(2),
          ];
          if (this.point1[0] === 0 && this.point1[1] === 0 && this.point1[2] === 0) {
            // first point
            this.setPoint1(point);
            console.log("point1:  "+this.point1)
          } else {
            // second point, calculate distance
            this.setPoint2(point);
            console.log("point2:  "+this.point2)
          }
        }
      }
    },

    updatePreviousPoint(model, index, color) {
      model.geometry.attributes.customSize.array[index] = 1;
      model.geometry.attributes.customColor.array[index * 3] = color.r;
      model.geometry.attributes.customColor.array[index * 3 + 1] = color.g;
      model.geometry.attributes.customColor.array[index * 3 + 2] = color.b;
    },
    highlightPoint(model, index) {
      model.geometry.attributes.customSize.array[index] = 8;
      this.previousColor.setRGB(
          model.geometry.attributes.customColor.array[index * 3],
          model.geometry.attributes.customColor.array[index * 3 + 1],
          model.geometry.attributes.customColor.array[index * 3 + 2]
      );
      model.geometry.attributes.customColor.array[index * 3] = 1;
      model.geometry.attributes.customColor.array[index * 3 + 1] = 0;
      model.geometry.attributes.customColor.array[index * 3 + 2] = 0;
    },
    render() {
      if (this.model && this.model.children.length > 0) {
        this.renderer.render(this.scene, this.camera);
      }
    },
    animate() {
      requestAnimationFrame(this.animate);

      this.controls.update();
      const T = this.clock.getDelta();
      this.timeS += T;

      if (this.timeS > 1 / this.FPS) {
        this.render();
        this.timeS = 0;
      }
    },
  },


};
</script>

<style scoped>

.container {
  position: relative;
}

.canvas {
  position: absolute;
  top: 63px;
  left: 0;
}

.controller {
  position: absolute;
  top: 120px;
  right: 20px;
}
</style>