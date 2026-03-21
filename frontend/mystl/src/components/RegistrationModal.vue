<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Регистрация пользователя</div>
      <div class="registration-div">
        <form class="registration-form">
          <div class="form-group">
            <label style="color: white">Имя пользователя</label>
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
            <label style="color: white">Email</label>
            <div class="input-group input-group-lg">
              <div class="input-group-addon">
                <span class="input-group-text">
                  <i class="bi bi-person fs-4"></i>
                </span>
              </div>
              <input
                type="text"
                class="form-control form-control-lg"
                @keyup="verifyEmail"
                v-model="email"
              />
            </div>
            <label style="color: white">Телефон</label>
            <div class="input-group input-group-lg">
              <div class="input-group-addon">
                <span class="input-group-text">
                  <i class="bi bi-person fs-4"></i>
                </span>
              </div>
              <input
                type="text"
                class="form-control form-control-lg"
                @keyup="verifyPhone"
                v-model="phone"
              />
            </div>
            <label style="color: white">Имя</label>
            <div class="input-group input-group-lg">
              <div class="input-group-addon">
                <span class="input-group-text">
                  <i class="bi bi-person fs-4"></i>
                </span>
              </div>
              <input
                type="text"
                class="form-control form-control-lg"
                v-model="first_name"
              />
            </div>
            <label style="color: white">Фамилия</label>
            <div class="input-group input-group-lg">
              <div class="input-group-addon">
                <span class="input-group-text">
                  <i class="bi bi-person fs-4"></i>
                </span>
              </div>
              <input
                type="text"
                class="form-control form-control-lg"
                v-model="last_name"
              />
            </div>
            <label style="color: white">Адрес</label>
            <div class="input-group input-group-lg">
              <div class="input-group-addon">
                <span class="input-group-text">
                  <i class="bi bi-person fs-4"></i>
                </span>
              </div>
              <input
                type="text"
                class="form-control form-control-lg"
                v-model="street_address"
              />
            </div>
            <label style="color: white">Почтовый индекс</label>
            <div class="input-group input-group-lg">
              <div class="input-group-addon">
                <span class="input-group-text">
                  <i class="bi bi-person fs-4"></i>
                </span>
              </div>
              <input
                type="text"
                class="form-control form-control-lg"
                v-model="postal_code"
              />
            </div>
            <label style="color: white">Страна</label>
            <div class="input-group input-group-lg">
              <select
                class="form-select form-control-lg"
                v-model="country"
                @change="selectCities"
                aria-label="Страна"
              >
                <option
                  v-for="_ in countries"
                  v-bind:value="_.code"
                  v-bind:key="_.country"
                >
                  {{ _.country }}
                </option>
              </select>
            </div>
            <label style="color: white">Город</label>
            <div class="input-group input-group-lg">
              <select
                class="form-select form-control-lg"
                v-model="city"
                aria-label="Страна"
              >
                <option
                  v-for="_ in cities"
                  v-bind:value="_.code"
                  v-bind:key="_.city"
                >
                  {{ _.city }}
                </option>
              </select>
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
                @click="register"
                class="btn btn-light btn-small btn-block btn-login btn-login-group"
              >
                <i class="bi bi-people"></i>
                Зарегестрироваться
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
  name: "RegistrationModal",
  props: [],
  data() {
    return {
      countries: [],
      cities: [],
      username: "",
      email: "",
      phone: "",
      first_name: "",
      last_name: "",
      country: "",
      city: "",
      postal_code: "",
      password: "",
      failed: false,
    };
  },
  methods: {
    verifyEmail() {
      if (
        !RegExp("[a-zA-Z.0-9_-]+@[a-zA-Z0-9]+.[a-zA-Z0-9]{2,5}").exec(
          this.email
        )
      ) {
        this.failed = true;
        this.error = "Неверный адрес электронной почты";
      } else {
        this.failed = false;
      }
    },
    verifyPhone() {
      if (!RegExp("\\+[0-9]{3}-[0-9]{2}-[0-9]{7}").exec(this.phone)) {
        this.failed = true;
        this.error = "Неверный номер телефона (+998-XX-XXXXX)";
      } else {
        this.failed = false;
      }
    },
    selectCities() {
      const data = { country: this.country };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/get_cities/", data, { headers })
        .then((response) => {
          if (response.data.success) {
            this.cities = response.data.result;
          }
        });
    },
    selectCountries() {
      const data = {};
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/get_contries/", data, { headers })
        .then((response) => {
          if (response.data.success) {
            this.countries = response.data.result;
          }
          this.failed = !response.data.success;
        });
    },
    register(e) {
      const data = {
        username: this.username,
        email: this.email,
        phone: this.phone,
        first_name: this.first_name,
        last_name: this.last_name,
        street_address: this.street_address,
        postal_code: this.postal_code,
        city_code: this.city,
        country_code: this.country,
        password: this.password,
      };
      const headers = {
        "Content-Type": "application/json",
      };
      axios
        .post(this.$BASE_URL + "/auth/register/", data, { headers })
        .then((response) => {
          if (response.data.success) {
            this.$emit("close", {});
          }
          this.failed = true;
          this.error = response.data.reason;
        });
      e.preventDefault();
    },
  },
  mounted() {
    this.selectCountries();
  },
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
  height: 800px;
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

.registration-div {
  border-radius: 10px;
  position: absolute;
  width: 600px;
  height: 860px;
}

.registration-form {
  width: 600px;
  height: 800px;
  background-color: rgb(205, 203, 235) !important;
  border-radius: 10px;
  margin: 0;
  padding: 0;
}
</style>
