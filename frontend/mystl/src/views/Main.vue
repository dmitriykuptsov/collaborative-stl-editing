<template>
  <div v-if="isAuthenticated">
    <SimpleSpinner v-if="showSpinner" />
    <OrderForm 
      v-if="showOrderForm" 
      v-bind:object="selectedProject" 
      v-bind:version="selectedVersion"
      v-on:close="closeOrederForm" />
    <ConfirmModal 
      v-if="showConfirmModal" 
      v-on:confirm="remove" 
      v-on:cancel="hideConfirm" 
      v-bind:header="header" 
      v-bind:message="message" />
    <OrdersForm 
      v-if="showOrdersForm" 
      v-on:close="closeOredersForm" />
    <CreateObject v-if="showCreateObject" v-on:close="closeCreateObject" />
    <div class="menu">
      <div class="menu-item" @click="createObject">
        <i class="bi bi-plus fs-4"></i>
        Новый проект
      </div>
      <div class="menu-item">
        <i class="bi bi-file fs-4"></i>
        Настройки
      </div>
      <div class="menu-item" @click="getOrders">
        <i class="bi bi-cart fs-4"></i>
        Заказы
      </div>
      <div class="menu-item" @click="logout">
        <i class="bi bi-door-open fs-4"></i>
        Выйти
      </div>
    </div>
    <div class="container">
      <div class="col1">
        <div class="col-header">Проекты</div>
        <SimplePaginator
          v-bind:count="totalObjects"
          v-bind:ipp="ipp"
          v-bind:currentPage="currentObjectPage"
          v-on:page-click="changeObjectPage"
          v-bind:autoMargin="true"
        />
        <br />
        <br />
        <br />
        <div
          v-for="_ in objects"
          v-bind:key="_.name"
          class="project"
          @click="changeProject(_.name)"
        >
          <div style="font-weight: bolder">Проект: {{ _.name }}</div>
          Дата создания:
          <span class="badge bg-danger">{{ _.creation_date }}</span>
          <button @click="confirm(_.name)" class="btn btn-dark btn-lg btn-block remove">
            <i class="bi bi-trash fs-6"></i> Удалить
          </button>
        </div>
      </div>
      <div class="col2">
        <div class="col-header">
          3D вьювер <span v-if="selectedProject"><b style="margin-left: 10px">Прокет</b>:
          <span class="badge bg-danger">{{ selectedProject }}</span>
          <b style="margin-left: 10px">Версия</b>:
          <span class="badge bg-danger">{{ selectedVersion }}</span>
          </span>
        </div>
        <StlViewer
          v-bind:object="selectedProject"
          v-bind:version="selectedVersion"
          v-on:loaded="onSTLLoaded"
        />
      </div>
      <div class="col3">
        <div class="col-header">
          Версии и свойства 
        </div>
        <div>
          <input type="file" @change="handleFile" ref="fileInput" hidden />
          <button @click="upload" class="btn btn-dark btn-lg btn-block upload">
            Загрузить
          </button>
        </div>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Свойство</th>
              <th>Значение</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Версия</td>
              <td>{{ info.version }}</td>
            </tr>
            <tr>
              <td>Oбъем</td>
              <td>{{ Math.round(info.volume*100)/100 }}</td>
            </tr>
            <tr>
              <td>Площадь</td>
              <td>{{ Math.round(info.surface_area*100)/100 }}</td>
            </tr>
            <tr>
              <td>Герметичный</td>
              <td>{{ info.is_water_tight }}</td>
            </tr>
            <tr>
              <td>Ширина</td>
              <td>{{ Math.round(info.width*100)/100 }}</td>
            </tr>
            <tr>
              <td>Высота</td>
              <td>{{ Math.round(info.height*100)/100 }}</td>
            </tr>
            <tr>
              <td>Длина</td>
              <td>{{ Math.round(info.length*100)/100 }}</td>
            </tr>
          </tbody>
        </table>
        <SimplePaginator
          v-bind:count="totalVersions"
          v-bind:ipp="ipp"
          v-bind:currentPage="currentVersionPage"
          v-on:page-click="changeVersionPage"
          v-bind:autoMargin="true"
        />
        <br />
        <br />
        <br />
        <div
          v-for="_ in versions"
          v-bind:key="_.version"
          class="versions"
          @click="changeVersion(_.name, _.version)"
        >
          <div style="font-weight: bolder">
            Объект: {{ _.name }}, Версия: {{ _.version }}
          </div>
          Дата создания:
          <span class="badge bg-danger">{{ _.date_uploaded }}</span> Хеш:
          {{ _.hash.substring(0, 6) + "..." }}
          <button class="btn btn-dark btn-lg btn-block upload" @click="order">Заказать печать</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateObject from "../components/CreateObject.vue";
import SimplePaginator from "../components/SimplePaginator.vue";
import StlViewer from "../components/StlViewer.vue";
import SimpleSpinner from "../components/SimpleSpinner.vue";
import OrderForm from "../components/OrderForm.vue";
import OrdersForm from "../components/OrdersForm.vue";
import ConfirmModal from "../components/ConfirmModal.vue";

axios.defaults.withCredentials = true;

export default {
  name: "App",
  data() {
    return {
      header: "",
      message: "",
      showConfirmModal: false,
      showSpinner: false,
      showOrderForm: false,
      showOrdersForm: false,
      showCreateObject: false,
      isAuthenticated: true,
      loaded: false,
      menuItemsActive: {},
      objects: [],
      objectToRemove: "",
      selectedProject: "",
      selectedVersion: "",
      versions: [],
      totalVersions: 0,
      totalObjects: 0,
      currentVersionPage: 1,
      currentObjectPage: 1,
      ipp: 4,
      info: {
        object: "",
        version: "",
        surface_area: 0,
        volume: 0,
        width: 0,
        length: 0,
        height: 0,
        is_water_tight: false,
      },
    };
  },
  methods: {
    confirm(object) {
      this.objectToRemove = object;
      this.header = "Удаление"
      this.message = "Удалить проект " + object + "?"
      this.showConfirmModal = true;
    },
    hideConfirm() {
      this.showConfirmModal = false;
    },
    remove() {
      this.showConfirmModal = false;
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/remove_object/";
      axios
        .post(
          url,
          {
            name: this.objectToRemove
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (!response.data.auth_fail) {
            this.isAuthenticated = true;
            this.getObjectsCount()
          } else {
            this.isAuthenticated = false;
            this.$router.push("/login/");
          }
        });
    },
    closeOredersForm() {
      this.showOrdersForm = false;
    },
    getOrders() {
      this.showOrdersForm = true;
    },
    closeOrederForm() {
      this.showOrderForm = false;
    },
    order() {
      if (!this.selectedVersion || !this.selectedProject) return;
      this.showOrderForm = true;
    },
    onSTLLoaded() {
      this.showSpinner = false;
    },
    changeVersion(object, version) {
      if (this.selectedVersion != version || this.selectedProject != object) {
        this.showSpinner = true;
      }
      this.selectedProject = object;
      this.selectedVersion = version;
      this.getStlInfo();
    },
    changeObjectPage(page) {
      this.currentObjectPage = page.page;
      this.getObjects();
    },
    changeVersionPage(page) {
      this.currentVersionPage = page.page;
      this.getVersions();
    },
    changeProject(object) {
      if (this.selectedProject != object) {
        this.showSpinner = true;
      }
      this.selectedProject = object;
      this.selectedVersion = 1;
      this.getStlInfo();
      this.getVersionsCount();
      this.getVersions();
    },
    handleFile(e) {
      this.file = e.target.files[0];
      const formData = new FormData();
      formData.append("model", this.file);
      formData.append("name", this.selectedProject);
      const url = this.$BASE_URL + "/upload/upload_file/";
      axios.post(url, formData).then((response) => {
        this.loaded = true;
        if (!response.data.auth_fail) {
          this.isAuthenticated = true;
          this.getVersions();
        } else {
          this.isAuthenticated = false;
          this.$router.push("/login/");
        }
      });
      this.$refs.fileInput.value = null;
    },
    upload() {
      this.$refs.fileInput.click();
    },
    closeCreateObject() {
      this.showCreateObject = false;
      this.getObjects();
    },
    createObject(e) {
      this.showCreateObject = true;
      this.getObjectsCount();

      e.preventDefault();
    },
    getStlInfo() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/get_stl_info/";
      axios
        .post(
          url,
          {
            name: this.selectedProject,
            version: this.selectedVersion,
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (!response.data.auth_fail) {
            this.isAuthenticated = true;
            this.info = response.data.result;
            if (!this.info) {
              this.info = {
                object: "",
                version: "",
                surface_area: 0,
                volume: 0,
                width: 0,
                length: 0,
                height: 0,
                is_water_tight: false,
              }
            }
          } else {
            this.isAuthenticated = false;
            this.$router.push("/login/");
          }
        });
    },
    getObjectsCount() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/get_objects_count/";
      axios.post(url, {}, { headers }).then((response) => {
        this.loaded = true;
        if (!response.data.auth_fail) {
          this.isAuthenticated = true;
          this.totalObjects = response.data.result;
          this.getObjects();
        } else {
          this.isAuthenticated = false;
          this.$router.push("/login/");
        }
      });
    },
    getVersionsCount() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/get_versions_count/";
      axios
        .post(
          url,
          {
            name: this.selectedProject,
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (!response.data.auth_fail) {
            this.isAuthenticated = true;
            this.totalVersions = response.data.result;
          } else {
            this.isAuthenticated = false;
            this.$router.push("/login/");
          }
        });
    },
    getVersions() {
      //this.showSpinner = true;
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/get_versions/";
      axios
        .post(
          url,
          {
            name: this.selectedProject,
            limit: 4,
            offset: this.ipp * (this.currentVersionPage - 1),
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (!response.data.auth_fail) {
            this.isAuthenticated = true;
            this.versions = response.data.result;
            //this.changeVersion(this.selectedProject, 1);
          } else {
            this.isAuthenticated = false;
            this.$router.push("/login/");
          }
        });
    },
    getObjects() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/upload/get_objects/";
      axios
        .post(
          url,
          {
            limit: 4,
            offset: this.ipp * (this.currentObjectPage - 1),
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (!response.data.auth_fail) {
            this.isAuthenticated = true;
            this.objects = response.data.result;
            this.selectedProject = ""
            this.selectedVersion = ""
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
    this.getObjectsCount();
    //this.getObjects();
  },
  components: {
    CreateObject,
    SimplePaginator,
    StlViewer,
    SimpleSpinner,
    OrderForm,
    OrdersForm,
    ConfirmModal
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

.versions {
  cursor: pointer;
  background-color: rgb(152, 152, 152);
  margin: 10px;
}

.versions:hover {
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
