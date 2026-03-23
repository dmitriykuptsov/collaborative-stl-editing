import { createApp } from "vue";
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "@/assets/css/main.css";
import router from "./router";

const app = createApp(App);
app.config.globalProperties["$BASE_URL"] = "http://localhost:5006";
//app.config.globalProperties["$BASE_URL"] = "https://solid-engineering.strangebit.io";
app.use(router);
app.mount("#app");
