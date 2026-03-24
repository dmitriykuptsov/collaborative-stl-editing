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
