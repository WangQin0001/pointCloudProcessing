import * as THREE from 'three';
import { PCDLoader } from "three/examples/jsm/loaders/PCDLoader.js";
// import shaders to change the size and color of points
import vertexShader from './shaders/vertexShader.glsl';
import fragmentShader from './shaders/fragmentShader.glsl';

const loader = new PCDLoader();
const model = new THREE.Group();

// use shader to define pointclout material
const pointCloudMaterial = new THREE.ShaderMaterial({
  vertexShader: vertexShader,
  fragmentShader: fragmentShader,
  transparent: true
});

// load pointcloud data from "path"
let pointCloud;
loader.load("static/models/pcd/newOutput.pcd", function (loadedPointCloud) {
  const geometry = loadedPointCloud.geometry;
  // get the size and color of loaded point cloud
  const customSize = new Float32Array(geometry.attributes.position.count);
  const customColor = new Float32Array(geometry.attributes.color.array);
  // set all points size = 1
  for (let i = 0; i < geometry.attributes.position.count; i++) {
    customSize[i] = 2;
  }
  geometry.setAttribute('customSize', new THREE.BufferAttribute(customSize, 1));
  geometry.setAttribute('customColor', new THREE.BufferAttribute(customColor, 3));
  // use custom geometry and poincloud material create new three.js points model
  pointCloud = new THREE.Points(geometry, pointCloudMaterial);
  // add pointcloud to model
  model.add(pointCloud);
  console.log("model", model);
},)

export default model;
