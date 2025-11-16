<template>
  <div class="login-main">
    <div class="login-text">
      <h3>
        Share, edit and order your 3D object for printing
      </h3>
    </div>
    <div class="login-div">
      <form class="login-form">
        <div class="form-group">
          <label>Username</label>
          <div class="input-group input-group-lg">
            <div class="input-group-addon">
              <span class="input-group-text">
                <i class="bi bi-person fs-3"></i>
              </span>
            </div>
            <input
              type="username"
              class="form-control form-control-lg"
              v-model="username"
            />
          </div>
        </div>
        <div class="form-group">
          <label>Password</label>
          <div class="input-group input-group-lg">
            <div class="input-group-append">
              <span class="input-group-text">
                <i class="bi bi-lock fs-3"></i>
              </span>
            </div>
            <input
              type="password"
              class="form-control form-control-lg"
              v-model="password"
            />
          </div>
        </div>
        <div class="form-group" style="margin-top: 10px">
          <button @click="login" class="btn btn-dark btn-lg btn-block btn-add">
            <i class="bi bi-door-open fs-3"></i>
            Login
          </button>
        </div>
        <div class="form-group" v-if="failed" style="margin-top: 10px">
          <div class="alert alert-danger" role="alert">
            Invalid username or password
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";


export default {
  name: "AuthLogin",
  data() {
    return {
      username: "",
      password: "",
      failed: false
    };
  },
  methods: {
    login(e) {
      const data = { username: this.username, password: this.password };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/signin/", data, { headers })
        .then((response) => {
          if (response.data.success) {
            sessionStorage.setItem("token", response.data[0].token);
            this.$parent.isAuthenticated = true;
            this.$router.push("/5gr/");
          }
          this.failed = !response.data.success;
        });
      e.preventDefault();
    }
  },
  components: {
  },
};
</script>

<style scoped>
h3 {
  color: #372d69;
  text-align: center;
}

.login-div {
  position: absolute;

  width: 450px;
  height: 300px;

  /* Center form on page horizontally & vertically */
  top: 420px;
  left: 50%;
  margin-top: -150px;
  margin-left: -225px;
}

.login-form {
  width: 450px;
  height: 300px;

  background: white;
  border-radius: 10px;

  margin: 0;
  padding: 0;
}

.login-text {
  margin-left: auto;
  margin-top: 200px;
  width: 100%;
}

.login-main {
  width: 100%;
}
</style>
