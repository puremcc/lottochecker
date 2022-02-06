import Vue from "vue";
import { router } from "./router";
import { store } from "./store";
import App from "./App.vue";
import vuetify from "@/plugins/vuetify"; // path to vuetify export

Vue.config.productionTip = false;

new Vue({
  store,
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
