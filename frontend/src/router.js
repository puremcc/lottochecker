import Vue from "vue";
import VueRouter from "vue-router";
import ActiveTickets from "./components/ActiveTickets";

Vue.use(VueRouter);

const routes = [{ path: "/tickets/active", component: ActiveTickets }];

export const router = new VueRouter({
  routes, // short for `routes: routes`
});
