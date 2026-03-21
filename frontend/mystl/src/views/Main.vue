<template>
  <div v-if="isAuthenticated">
    <CreateObject
      v-if="showCreateObject"
      v-on:close="closeCreateObject"
    />
    <div class="menu">
      <div class="menu-item" @click="createObject">
        <i class="bi bi-plus fs-4"></i>
        Новый проект
      </div>
      <div class="menu-item">
        <i class="bi bi-file fs-4"></i>
        Настройки
      </div>
      <div class="menu-item" @click="logout">
        <i class="bi bi-door-open fs-4"></i>
        Выйти
      </div>      
    </div>
    <div class="container">
      <div class="col1">
        <div class="col-header">
          Проекты
        </div>
        <div v-for="_ in objects" v-bind:key="_.name" class="project">
          <div style="font-weight: bolder;">Проект: {{_.name}}</div> 
          Дата создания: <span class="badge bg-danger">{{_.creation_date}}</span>
        </div>
      </div>
      <div class="col2">
        <div class="col-header">
          3D вьюер
        </div>
      </div>
      <div class="col3">
        <div class="col-header">
          Версии
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateObject from '../components/CreateObject.vue';

axios.defaults.withCredentials = true;

export default {
  name: "App",
  data() {
    return {
      showCreateObject: false,
      isAuthenticated: true,
      loaded: false,
      menuItemsActive: {},
      objects: []
    };
  },
  methods: {
    closeCreateObject() {
      this.showCreateObject = false;
      this.getObjects();
    },
    createObject(e) {
      this.showCreateObject = true;
      this.getObjects();
      e.preventDefault();
    },
    getObjects() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/get_objects/";
      axios.post(url, {}, { headers }).then((response) => {
        this.loaded = true;
        if (!response.data.auth_fail) {
          this.isAuthenticated = true;
          this.objects = response.data.result;
        } else {
          this.isAuthenticated = false;
          this.$router.push("/login/");
        }
      });
    },
    checkAuth() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/auth/validate_token/";
      axios.post(url, {}, { headers }).then((response) => {
        this.loaded = true;
        if (response.data.valid) {
          this.isAuthenticated = true;
        } else {
          this.isAuthenticated = false;
          this.$router.push("/login/");
        }
      });
    },
    renewToken() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/auth/renew_token/";
      axios.post(url, {}, { headers }).then(() => {});
    },
    logout() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/auth/logout/";
      axios.post(url, {}, { headers }).then((response) => {
        if (response.data.success) {
          this.isAuthenticated = false;
          this.$router.push("/login/");
        }
      });
    },
    pollAuthData() {
      this.polling = setInterval(() => {
        this.checkAuth();
      }, 60000);
    },
    pollRenewToken() {
      this.renewing = setInterval(() => {
        this.renewToken();
      }, 10 * 60000);
    },
  },
  mounted() {
    this.checkAuth();
    this.pollAuthData();
    this.pollRenewToken();
    this.getObjects();
  },
  components: {
    CreateObject,
  },
};
</script>

<style scoped>
.menu {
  background-color: rgb(255, 255, 255);
}

.menu-item {
  padding-left: 10px;
  padding-right: 10px;
  margin-left: 2px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background-color: rgb(152, 152, 152);
  vertical-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-item:hover {
  cursor: pointer;
  background-color: rgb(73, 73, 73);
  vertical-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.project {
  cursor: pointer;
  background-color: rgb(152, 152, 152);
  margin: 10px;
}

.project:hover {
  cursor: pointer;
  background-color: rgb(73, 73, 73);
  margin: 10px;
}

.container {
  max-width: 2000px;
  margin-top: 20px;
  width: 100%;
  display: flex;
  gap: 20px;
}

.col1 {
  width: 20%;
  background: #eee;
  height: 90vh;
}

.col2 {
  width: 60%;
  background: #eee;
  height: 90vh;
}

.col3 {
  width: 20%;
  background: #eee;
  height: 90vh;
}

.col-header {
  height: 40px;
  display: flex;
  vertical-align: center;
  align-items: center;
  justify-content: center;
  background-color: rgb(182, 182, 182);
}
</style>
