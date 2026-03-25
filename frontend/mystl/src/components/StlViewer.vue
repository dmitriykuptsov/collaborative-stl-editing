<template>
  <div ref="container" style="width: 100%; height: 86vh"></div>
</template>

<script>
import * as THREE from "three";
import axios from "axios";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { TransformControls } from 'three/examples/jsm/controls/TransformControls.js';

export default {
  name: "StlViewer",
  props: ["object", "version"],
  data() {
    return {
      name: "",
      description: "",
      failed: false,
      error: "",
    };
  },
  watch: {
    $props: {
      handler() {
        this.loadModel();
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    loadModel() {
      if (!this.$refs.container) {
        this.$emit("loaded", {});
        return;
      }
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(
        75,
        this.$refs.container.clientWidth / this.$refs.container.clientHeight,
        0.1,
        1000,
      );
      camera.position.z = 100;
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(
        this.$refs.container.clientWidth,
        this.$refs.container.clientHeight,
      );
      this.$refs.container.replaceChildren();
      this.$refs.container.appendChild(renderer.domElement);
      const controls = new OrbitControls(camera, renderer.domElement);

      const transform = new TransformControls(camera, renderer.domElement);


      // Light
      const light = new THREE.DirectionalLight(0xffffff, 1);
      light.position.set(10, 10, 10);
      scene.background = new THREE.Color(0xffffff)
      scene.add(light);

      const grid = new THREE.GridHelper(200, 10);
      scene.add(grid);

      const axes = new THREE.AxesHelper(4);
      axes.scale.set(25, 25, 25);
      scene.add(axes);

      const origin = new THREE.Vector3(0, 0, 0);

      // X axis (red)
      const xDir = new THREE.Vector3(100, 0, 0);
      const xArrow = new THREE.ArrowHelper(xDir, origin, 100, 0xff0000);

      // Y axis (green)
      const yDir = new THREE.Vector3(0, 100, 0);
      const yArrow = new THREE.ArrowHelper(yDir, origin, 100, 0x00ff00);

      // Z axis (blue)
      const zDir = new THREE.Vector3(0, 0, 100);
      const zArrow = new THREE.ArrowHelper(zDir, origin, 100, 0x0000ff);

      scene.add(xArrow, yArrow, zArrow);

      // Loader
      const loader = new STLLoader();

      const headers = {
        
      };
      if (!this.object || !this.version) {
        this.$emit("loaded", {});
        return;
      }
      const url =
        this.$BASE_URL + "/upload/get_stl/";
      axios
        .get(
          url,

          {
            headers,
            responseType: "arraybuffer",
            maxContentLength: Infinity,
            maxBodyLength: Infinity,
            transformResponse: [(data) => data],
            transitional: {
                forcedJSONParsing: false,
            },
            params: {
              object: this.object,
              version: this.version,
            },
          },
        )
        .then((response) => {
          try {
            const arrayBuffer = response.data;
            var geometry = loader.parse(arrayBuffer);
            geometry.center()
          } catch (e) {
            this.$emit("loaded", {});
            return;
          }

          const mesh = new THREE.Mesh(
            geometry,
            new THREE.MeshPhongMaterial({ color: 0xffff00 }),
          );

          scene.add(mesh);

          camera.add(light);
          scene.add(camera);

          transform.attach(mesh);
          scene.add(transform);

          // Render loop
          function animate() {
            requestAnimationFrame(animate);
            controls.update();
            light.position.copy(camera.position);
            renderer.render(scene, camera);
          }

          animate();
          this.$emit("loaded", {});
        });
    },
  },
  mounted() {
    //this.loadModel();
  },
};
</script>
