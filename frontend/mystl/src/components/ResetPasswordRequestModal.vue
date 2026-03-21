<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Сброс пароля</div>
      <div class="reset-div">
        <form class="reset-form">
          <div class="form-group">
            <label style="color: white">Имя пользователя или почта</label>
            <div class="input-group input-group-lg">
              <div class="input-group-addon">
                <span class="input-group-text">
                  <i class="bi bi-person fs-4"></i>
                </span>
              </div>
              <input
                type="text"
                class="form-control form-control-lg"
                v-model="username"
              />
            </div>
            <div class="form-group" style="margin-top: 10px">
              <button
                @click="reset"
                class="btn btn-light btn-small btn-block btn-login btn-login-group"
              >
                <i class="bi bi-people"></i>
                Запросить сброс
              </button>
            </div>
            <div class="form-group" v-if="failed" style="margin-top: 10px">
              <div class="alert alert-danger" role="alert">
                {{ error }}
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ResetPasswordRequestModal",
  props: [],
  data() {
    return {
      username: "",
      failed: false,
    };
  },
  methods: {
    reset(e) {
      const data = {
        username: this.username,
      };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/reset_password_request/", data, {
          headers,
        })
        .then((response) => {
          if (response.data.success) {
            this.$emit("close", {});
          } else {
            this.failed = true;
            this.error = response.data.reason;
          }
        });
      e.preventDefault();
    },
  },
  mounted() {},
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 1000094;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal-window {
  background-color: rgb(205, 203, 235) !important;
  border-radius: 10px;
  position: fixed;
  width: 600px;
  height: 200px;
  top: 200px;
  left: calc(50% - 100px);
  margin-top: -100px;
  margin-left: -200px;
  z-index: 1000095;
}

.header {
  border-radius: 10px;
  height: 30px;
  width: 100%;
  background-color: rgb(205, 203, 235) !important;
  text-align: center;
  font-weight: bold;
}

.reset-div {
  border-radius: 10px;
  position: absolute;
  margin-left: 50px; 
  width: 500px;
  height: 100px;
}

.reset-form {
  width: 500px;
  height: 100px;
  background-color: rgb(205, 203, 235) !important;
  border-radius: 10px;
  margin: 0;
  padding: 0;
}
</style>
