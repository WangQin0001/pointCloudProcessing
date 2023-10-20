// this page define main logic of render
//没用的上个版本文件

import * as THREE from 'three';
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import model from './model.js'; //import pcd model
import { Message } from 'element-ui';

//create a scene
const scene = new THREE.Scene();
// add model to scene
scene.add(model);

//auxiliary observation coordinates
// const axesHelper = new THREE.AxesHelper(10);
// scene.add(axesHelper);

//get current width and heighe of brower window
const width = window.innerWidth;
const height = window.innerHeight;

// create a perspectiveCamera
const camera = new THREE.PerspectiveCamera(30, width / height, 1, 3000);
// Set camera position according to the magnitude of rendering size
camera.position.set(340, 410, 550);
camera.lookAt(0, 0, 0);

// create a renderen
const renderer = new THREE.WebGLRenderer();
renderer.setSize(width, height);

// create a control
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0, 0);

// set canvas size changes with window
window.onresize = function () {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
};

// create a mouse object in vectors type for store current mouse position
const mouse = new THREE.Vector2();
document.addEventListener('mousemove', onMouseMove, false);
//throttling time to improve rendering efficiency
let throttleTimeout = null;
function onMouseMove(event) {
  if (!throttleTimeout) {
    throttleTimeout = setTimeout(() => {
      event.preventDefault();
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
      throttleTimeout = null;
    }, 10); //no recalculation within 10ms
  }
}

// raycaster to obtain objects down current mouse, https://threejs.org/docs/#api/en/core/Raycaster
const raycaster = new THREE.Raycaster();
// precision of raycaster
raycaster.params.Points.threshold = 1.0;
let previousIndex = null;
const previousColor = new THREE.Color();

// when mouse move out, restore the properties of previous point
function updatePreviousPoint(model, index, color) {
  model.geometry.attributes.customSize.array[index] = 1;
  model.geometry.attributes.customColor.array[index * 3] = color.r;
  model.geometry.attributes.customColor.array[index * 3 + 1] = color.g;
  model.geometry.attributes.customColor.array[index * 3 + 2] = color.b;
}

// change the color of point to red when mouse move in
function highlightPoint(model, index) {
  model.geometry.attributes.customSize.array[index] = 8;
  previousColor.setRGB(
      model.geometry.attributes.customColor.array[index * 3],
      model.geometry.attributes.customColor.array[index * 3 + 1],
      model.geometry.attributes.customColor.array[index * 3 + 2]
  );
  model.geometry.attributes.customColor.array[index * 3] = 1;
  model.geometry.attributes.customColor.array[index * 3 + 1] = 0;
  model.geometry.attributes.customColor.array[index * 3 + 2] = 0;
}

// Handle the click event
function createOnClickHandler(intersects) {
  return function () {
    // alert the information of current point when click on it
    Message({
      message:
          'DistanceToCamera : ' + intersects[0].distance.toFixed(2) +
          '<br/>' +
          'Position.X :' + intersects[0].point.x.toFixed(2) +
          '<br/>' +
          'Position.Y :' + intersects[0].point.y.toFixed(2) +
          '<br/>' +
          'Position.Z :' + intersects[0].point.z.toFixed(2),
      dangerouslyUseHTMLString: true
    });
  };
}

let intersects;//objects down current mouse
let index;//the index of current object
let pointModel;
let currentOnClickHandler;
function render() {
  if (model.children.length > 0) {
    raycaster.setFromCamera(mouse, camera);
    intersects = raycaster.intersectObjects(model.children);//the objects obtained
    if (intersects.length > 0) {
      index = intersects[0].index;
      pointModel = model.children[0];
      if (previousIndex !== null) {
        updatePreviousPoint(pointModel, previousIndex, previousColor);
      }
      highlightPoint(pointModel, index);
      pointModel.geometry.attributes.customSize.needsUpdate = true;
      pointModel.geometry.attributes.customColor.needsUpdate = true;
      previousIndex = index;
      document.removeEventListener('click', currentOnClickHandler);//remove previous click event before new click event
      currentOnClickHandler = createOnClickHandler(intersects, pointModel);//handel click event
      document.addEventListener('click', currentOnClickHandler);
    }
    renderer.render(scene, camera);
  }
}


// create a clock object
var clock = new THREE.Clock();
// the rendering frequency and circle
var FPS = 120;
var renderT = 1 / FPS;
// timeS is cumulative time of the render() function call. If renderer.render() is executed once, timeS is reset to 0
var timeS = 0;

// control the excution of render
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  var T = clock.getDelta();//get the time interval between two times render
  timeS = timeS + T;
  if (timeS > renderT) {
    render();
    timeS = 0;
  }
}

animate()

export { renderer };