<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Активные заказы</div>
      <div>
        <div class="order-form">
          <div class="orders">
            <div class="order" v-for="_ in orders" v-bind:key="_.order_number">
                <span class="badge bg-success">Объект {{_.object}}, Версия {{_.version}}</span><br/>
                <span class="badge bg-success">Принтер {{_.machine}}, Материал {{_.material}}, Цвет {{_.color_desc}}</span><br/>
                <span>Цена: {{Math.round(_.price)}} сум</span><br/>
                <span>Статус: {{_.status}}</span><br/>
            </div>
          </div>
        </div>
      </div>
      <button @click="cancel" class="btn btn-dark btn-lg btn-block cancel-order">
        Закрыть
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

axios.defaults.withCredentials = true;
export default {
  name: "OrdersForm",
  props: [],
  data() {
    return {
      orders: [],
      failed: false,
      error: "",
      ordered: false
    };
  },
  methods: {
    getOrders() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/orders/get_active_orders/";
      axios
        .post(
          url,
          {
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (response.data.success) {
            this.orders = response.data.result;
          } else {
            this.failed = true;
            this.error = response.data.reason;
          }
        });
    },
    cancel() {
      this.$emit("close", {});
    },
  },
  mounted() {
    this.getOrders();
  },
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 1000092;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal-window {
  border: rgb(169, 255, 202);
  background-color: white;
  position: fixed;
  width: 600px;
  height: 600px;
  top: 30%;
  left: calc(50% - 150px);
  margin-top: -100px;
  margin-left: -200px;
  z-index: 1000093;
}

.message {
  font-weight: bolder;
  color: black;
  text-align: center;
}

.order {
  cursor: pointer;
  background-color: rgb(152, 152, 152);
  margin: 10px;
  width: 96%;
}

</style>
