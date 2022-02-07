import Vue from "vue";
import VueRouter from "vue-router";
import ActiveTickets from "./components/ActiveTickets";
import ListTickets from "./components/ListTickets";
import TicketDetails from "./components/TicketDetails";
import EnterTicket from "./components/EnterTicket";

Vue.use(VueRouter);

const routes = [
  { path: "/tickets/active", component: ActiveTickets },
  { path: "/tickets", component: ListTickets },
  { path: "/tickets/create", name: "CreateTicket", component: EnterTicket },
  { path: "/tickets/:dateKey", component: TicketDetails, props:true },
  { path: "/ticketDetails", component: TicketDetails, props: true },
];

export const router = new VueRouter({
  routes, // short for `routes: routes`
});
