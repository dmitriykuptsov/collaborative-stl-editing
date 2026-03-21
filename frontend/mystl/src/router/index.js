import { createRouter, createWebHistory } from "vue-router";
import ConfirmEmail from "@/views/ConfirmEmail.vue";
import ResetPassword from "@/views/ResetPassword.vue";
import AuthLogin from "@/views/AuthLogin.vue";
import Main from "@/views/Main.vue";

const routes = [
  {
    path: "/confirm_email",
    name: "ConfirnEmail",
    component: ConfirmEmail,
  },
  {
    path: "/password_reset",
    name: "ResetPassword",
    component: ResetPassword,
  },
  {
    path: "/login",
    name: "AuthLogin",
    component: AuthLogin,
  },
  {
    path: "/main",
    name: "Main",
    component: Main,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.replace({ path: "*", redirect: "/" });

export default router;
