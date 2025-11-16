<template>
  <div v-if="loaded">
    <div v-if="isAuthenticated">
      <header>
        <div class="title">
          <span id="caption-text">Share, edit and order your parts</span>
        </div>
      </header>
      <router-view></router-view>
    </div>
    <div v-if="!isAuthenticated">
      <AuthLogin />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AuthLogin from "@/views/AuthLogin.vue";

export default {
  name: "App",
  data() {
    return {
      isAuthenticated: false,
      loaded: false,
      menuItemsActive: {},
    };
  },
  methods: {
    checkAuth() {
      const headers = {
        "Content-Type": "application/json"
      };
      const url = this.$BASE_URL + "/auth/validate_token/";
      axios.post(url, {}, { headers }).then((response) => {
        this.loaded = true;
        if (response.data[0].valid) {
          this.isAuthenticated = true;
        } else {
          this.isAuthenticated = false;
        }
      });
    },
    logout() {
      const headers = {
        "Content-Type": "application/json"
      };
      const url = this.$BASE_URL + "/auth/logout/";
      axios.post(url, {}, { headers }).then((response) => {
        this.loaded = true;
        if (response.data[0].valid) {
          this.isAuthenticated = true;
        } else {
          this.isAuthenticated = false;
        }
      });
    },
    pollAuthData() {
      this.polling = setInterval(() => {
        this.checkAuth();
      }, 60000);
    },
  },
  mounted() {
    this.checkAuth();
    this.pollAuthData();
    this.$router.push("/mystl");
  },
  components: {
    AuthLogin,
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
}

#nav {
  padding: 25px 30px;
  margin: 0 auto;
}

#nav a {
  font-weight: bold;
  color: #ffffff;
  /* min-height: 75px; */
  font-family: "Dazzed", sans-serif;
  /* align-items: center; */
  text-decoration: none;
  margin: 0 1px;
}

#caption-text {
  font-size: 18px;
}

#logo {
  position: absolute;
  bottom: 20px;
  margin-left: 20px;
}

#logo_top {
  position: absolute;
  display: block;
  margin-left: 3.4%;
}

.nav-btn {
  display: inline-block;
  height: 35px;
  max-width: 100%;
  align-items: center;
  line-height: 2.28571em;
  vertical-align: middle;
  padding: 0 6px;
}

.nav-btn:hover {
  color: rgb(255, 255, 255);
  box-shadow: transparent 0px 0px 0px 2px;
  background-color: rgba(120, 119, 125, 0.6);
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}

.nav-btn:focus {
  background-color: rgba(106, 103, 121, 0.6);
  border-radius: 3px;
}

#exit-btn {
  background-color: rgb(79, 67, 140);
  border-style: none;
  border-radius: 3px;
  display: inline-flex;
  height: 35px;
  max-width: 100%;
  align-items: center;
  line-height: 2.28571em;
  vertical-align: middle;
  padding: 0 6px;
}

#exit-btn:hover {
  background-color: rgba(79, 67, 140, 0.8);
  box-shadow: transparent 0px 0px 0px 2px;
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}

#exit-btn:focus {
  background-color: inherit;
}

.title {
  width: 100%;
  display: block;
  position: fixed;
  top: 0%;
  z-index: 1;
  background: #ffffff;
  text-align: center;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  font-weight: bold;
}

.selected-menu-item {
  color: rgb(255, 255, 255);
  box-shadow: transparent 0px 0px 0px 2px;
  background-color: rgba(120, 119, 125, 0.6);
  transition: background 0.1s ease-out 0s,
    box-shadow 0.15s cubic-bezier(0.47, 0.03, 0.49, 1.38) 0s;
  border-radius: 3px;
}
</style>
