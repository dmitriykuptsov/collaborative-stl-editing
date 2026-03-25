<template>
  <div class="modal-mask">
    <div class="modal-window">
      <div class="header">Создать заказ</div>
      <div>
        <div class="order-form">
          <span style="color: black" class="badge bg-danger">Проект {{object}} Версия {{version}}</span>
          <div class="printers">
            <div class="printer" v-for="_ in machinery" v-bind:key="_.machine + _.material + _.color">
                <span class="badge bg-success">Принтер {{_.machine}}, Материал {{_.material}}, Цвет {{_.color_desc}}</span>
                <span class="badge bg-success" v-if="!_.overfit">Размерность нормальная</span>
                <span class="badge bg-danger" v-if="_.overfit">Объект превышает размерность</span><br/>
                <span>Цена: {{Math.round(_.price)}} сум</span><br/>
                <button @click="order(_.machine, _.material, _.color)" class="btn btn-dark btn-lg btn-block order">Заказать</button>
            </div>
          </div>
        </div>
      </div>
      <div class="form-group" v-if="ordered" style="margin-top: 10px">
          <div class="alert alert-success" role="alert">
            Заказ создан
          </div>
        </div>
        <div class="form-group" v-if="failed" style="margin-top: 10px">
          <div class="alert alert-success" role="alert">
            {{error}}
          </div>
        </div>
      <button @click="cancel" class="btn btn-dark btn-lg btn-block cancel-order">
        Отменить
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

axios.defaults.withCredentials = true;
export default {
  name: "OrderForm",
  props: ["object", "version"],
  data() {
    return {
      machinery: [],
      failed: false,
      error: "",
      ordered: false
    };
  },
  methods: {
    getMachinery() {
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/orders/get_machinery/";
      axios
        .post(
          url,
          {
            name: this.object,
            version: this.version,
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (response.data.success) {
            this.machinery = response.data.result;
          } else {
            this.failed = true;
            this.error = response.data.reason;
          }
        });
    },
    order(machine, material, color) {
        alert(machine)
      const headers = {
        "Content-Type": "application/json",
      };
      const url = this.$BASE_URL + "/orders/place_order/";
      axios
        .post(
          url,
          {
            name: this.object,
            version: this.version,
            machine: machine,
            material: material,
            color: color
          },
          { headers },
        )
        .then((response) => {
          this.loaded = true;
          if (response.data.success) {
            this.ordered = true;
            setTimeout(() => {
                this.ordered = false;
                this.$emit("close", {});
            }, 5000);
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
    this.getMachinery();
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

.printer {
  cursor: pointer;
  background-color: rgb(152, 152, 152);
  margin: 10px;
}

</style>
