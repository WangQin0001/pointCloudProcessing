// 在 model.js 文件中
import * as THREE from 'three';
import { PCDLoader } from "three/examples/jsm/loaders/PCDLoader.js";
import vertexShader from './shaders/vertexShader.glsl';
import fragmentShader from './shaders/fragmentShader.glsl';

const DEFAULT_PCD_PATH = "static/models/pcd/newOutput.pcd";
function loadModel(file,callback) {
  const loader = new PCDLoader();
  const model = new THREE.Group();
  const url = (typeof file === "string") ? file : URL.createObjectURL(file);
  console.log("Loading model from URL: ", url); // 添加调试信息
  const pointCloudMaterial = new THREE.ShaderMaterial({
    vertexShader: vertexShader,
    fragmentShader: fragmentShader,
    transparent: true
  });

  loader.load(url, function (loadedPointCloud) {
    console.log("PointCloud loaded: ", loadedPointCloud);
    const geometry = loadedPointCloud.geometry;
    const customSize = new Float32Array(geometry.attributes.position.count);
    const customColor = new Float32Array(geometry.attributes.color.array);

    for (let i = 0; i < geometry.attributes.position.count; i++) {
      customSize[i] = 2;
    }

    geometry.setAttribute('customSize', new THREE.BufferAttribute(customSize, 1));
    geometry.setAttribute('customColor', new THREE.BufferAttribute(customColor, 3));

    const pointCloud = new THREE.Points(geometry, pointCloudMaterial);
    model.add(pointCloud);
    callback(model);
    if (typeof file !== "string") {
      URL.revokeObjectURL(url);
    }
  });
}

export { loadModel, DEFAULT_PCD_PATH };
