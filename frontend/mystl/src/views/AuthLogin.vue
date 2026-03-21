<template>
  <div class="login-main">
    <img src="@/assets/logo.png" class="logo" />
    <div class="login-text">
      <h3 style="color: white; margin-bottom: 100px">
        Solid Engineering - то место где цифра
        <br />
        превращается в физический объект
      </h3>
    </div>
    <RegistrationModalVue
      v-if="showRegistrationModal"
      v-on:close="closeRegistrationModal"
    />
    <div class="login-div">
      <form class="login-form">
        <div class="form-group">
          <label style="color: white">Имя пользователя</label>
          <div class="input-group input-group-lg">
            <div class="input-group-addon">
              <span class="input-group-text">
                <i class="bi bi-person fs-4"></i>
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
          <label style="color: white">Пароль</label>
          <div class="input-group input-group-lg">
            <div class="input-group-append">
              <span class="input-group-text">
                <i class="bi bi-lock fs-4"></i>
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
          <button
            @click="login"
            class="btn btn-light btn-small btn-block btn-login btn-login-group"
          >
            <i class="bi bi-door-open"></i>
            Войти
          </button>
          <button
            @click="reset"
            class="btn btn-light btn-small btn-block btn-reset btn-login-group"
          >
            <i class="bi bi-pass"></i>
            Восстановить пароль
          </button>
          <button
            @click="register"
            class="btn btn-light btn-small btn-block btn-login btn-login-group"
          >
            <i class="bi bi-people"></i>
            Зарегестрироваться
          </button>
        </div>
        <div class="form-group" v-if="failed" style="margin-top: 10px">
          <div class="alert alert-danger" role="alert">
            Неверный логин или пароль
          </div>
        </div>
        <div class="form-group" v-if="registered" style="margin-top: 10px">
          <div class="alert alert-success" role="alert">
            Пользователь зарегистрирован. Проверьте почту для подтверждения
          </div>
        </div>
      </form>
      <div class="services">
        Что мы предлагаем:
        <ul>
          <li>Колаборация и совместное обсуждение ваших 3D дезайнов</li>
          <li>Валидация 3D моделей</li>
          <li>Подготовка к печати</li>
          <li>
            Высокоточная SLA печать на оборудование от ведущих производителей
            (на данный момент мы используем Formlabs Form 4 3D)
          </li>
          <li>Доставка ваших изделий курьером</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import RegistrationModalVue from "../components/RegistrationModal.vue";

export default {
  name: "AuthLogin",
  data() {
    return {
      username: "",
      password: "",
      failed: false,
      registered: false,
      showRegistrationModal: false,
    };
  },
  methods: {
    closeRegistrationModal() {
      this.showRegistrationModal = false;
      this.registered = true;
    },
    register(e) {
      this.showRegistrationModal = true;
      e.preventDefault();
    },
    login(e) {
      const data = { username: this.username, password: this.password };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/signin/", data, { headers, withCredentials: true })
        .then((response) => {
          if (response.data.success) {
            this.$parent.isAuthenticated = true;
            this.$router.push("/main");
          } else {
            this.failed = !response.data.success;
          }
        });
      e.preventDefault();
    },
  },
  components: {
    RegistrationModalVue,
  },
};
</script>

<style scoped>
h3 {
  color: #372d69;
  text-align: center;
}

.services {
  margin-top: 100px;
  padding-left: 10px;
  padding-top: 10px;
  padding-right: 10px;
  font-weight: bolder;
  border: solid;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  border-width: 1px;
  border-radius: 10px;
  color: #f3f2f7;
}

.btn-login-group {
  margin-top: 10px;
}

.login-div {
  position: absolute;

  width: 450px;
  height: 300px;

  /* Center form on page horizontally & vertically */
  top: 450px;
  left: 50%;
  margin-top: -150px;
  margin-left: -225px;
}

.logo {
  margin-top: 10px;
  margin-left: calc(50% - 100px);
  width: 200px;
  height: 200px;
}

.login-form {
  width: 450px;
  height: 300px;

  background-color: rgb(178, 176, 217) !important;
  border-radius: 10px;

  margin: 0;
  padding: 0;
}

.login-text {
  margin-left: auto;
  margin-top: 10px;
  width: 100%;
}

.login-main {
  width: 100%;
}
</style>
