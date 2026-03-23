<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Создать новый проект</div>
      <div>
        <form class="registration-form">
          <div class="form-group">
            <label style="color: black">Название</label>
            <div class="input-group input-group-lg">
              <input
                type="text"
                class="form-control form-control-lg"
                v-model="name"
              />
            </div>
            <label style="color: black">Описание</label>
            <div class="input-group input-group-lg">
              <input
                type="text"
                class="form-control form-control-lg"
                v-model="description"
              />
            </div>
            <div class="form-group" v-if="failed" style="margin-top: 10px">
              <div class="alert alert-danger" role="alert">
                {{ error }}
              </div>
            </div>
          </div>
        </form>
      </div>
      <button @click="confirm" class="btn btn-dark btn-lg btn-block confirm">
        Создать
      </button>
      <button @click="cancel" class="btn btn-dark btn-lg btn-block cancel">
        Отменить
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

axios.defaults.withCredentials = true;
export default {
  name: "ConfirmModal",
  props: [],
  data() {
    return {
      name: "",
      description: "",
      failed: false,
      error: "",
    };
  },
  methods: {
    create(cb) {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/create_object_description/";
      axios
        .post(
          url,
          {
            name: this.name,
            description: this.description,
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (response.data.success) {
            cb();
          } else {
            this.failed = true;
            this.error = response.data.reason;
          }
        });
    },
    confirm() {
      this.create(this.cancel);
    },
    cancel() {
      this.$emit("close", {});
    },
  },
  mounted() {},
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 1000092;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal-window {
  border: rgb(169, 255, 202);
  background-color: white;
  position: fixed;
  width: 400px;
  height: 300px;
  top: 50%;
  left: 50%;
  margin-top: -100px;
  margin-left: -200px;
  z-index: 1000093;
}

.message {
  font-weight: bolder;
  color: black;
  text-align: center;
}
</style>
