import Vue from "vue";
import VueRouter from "vue-router";
import ActiveTickets from "./components/ActiveTickets";
import ListTickets from "./components/ListTickets";
import TicketDetails from "./components/TicketDetails"

Vue.use(VueRouter);

const routes = [
  { path: "/tickets/active", component: ActiveTickets },
  { path: "/tickets", component: ListTickets },
  { path: "/ticket/{dateRange}", TicketDetails },
];

export const router = new VueRouter({
  routes, // short for `routes: routes`
});
