<template>
  <div class="form-group" style="margin-top: 100px">
    <div style="width: 20%; margin-left: calc(40%)">
      <p class="alert alert-success" style="text-align: center">
        Нажмите кнопку подтвердить для завершения верификации!
      </p>
      <button
        @click="confirm"
        class="btn btn-light btn-small btn-block btn-confirm"
      >
        Подтвердить
      </button>
      <div class="form-group" v-if="confirmed" style="margin-top: 10px">
        <div class="alert alert-success" role="alert">
          Учетная запись подтверждена. Вы будете перенаправлены на страницу
          входа через 3 секунды
        </div>
      </div>

      <div
        v-if="error"
        class="alert alert-danger"
        role="alert"
        style="margin-top: 10px; text-align: center"
      >
        {{ error_msg }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ConfirmEmail",
  data() {
    return {
      confirmed: false,
      error: false,
      error_msg: "",
    };
  },
  methods: {
    confirm() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/auth/confirm_email/";
      axios
        .post(
          url,
          {
            username: this.$route.query.username,
            token: this.$route.query.token,
          },
          { headers },
        )
        .then((response) => {
          if (response.data.success) {
            this.confirmed = true;
            setTimeout(() => {
              this.$router.push("/login");
            }, 2000);
          } else {
            this.error = true;
            this.error_msg = response.data.reason;
          }
        });
    },
  },
  mounted() {},
  components: {},
};
</script>

<style scoped>
.btn-confirm {
  width: 100%;
}
</style>
