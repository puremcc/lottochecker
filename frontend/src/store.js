import Vue from "vue";
import Vuex from "vuex";
import utils from "./utils";
import { Ticket } from "./models/firebase";

Vue.use(Vuex);

const ticketModel = new Ticket();

export const store = new Vuex.Store({
  state() {
    return {
      winningNumbers: JSON.parse(localStorage.getItem("winningNumbers")) || [],
      lastFetched: new Date(+localStorage.getItem("lastFetched")) || null,
      tickets: [],
    };
  },
  mutations: {
    setWinningNumbers(state, payload) {
      state.winningNumbers = payload;
      localStorage.setItem("winningNumbers", JSON.stringify(payload));
    },
    setLastFetched(state) {
      state.lastFetched = new Date().getTime();
      localStorage.setItem("lastFetched", JSON.stringify(state.lastFetched));
    },
    setTickets(state, payload) {
      state.tickets = payload;
    },
  },
  actions: {
    async loadWinningNumbers(context) {
      console.log("loadWinningNumbers...");
      console.log(
        " - lastFetched: " + context.state.lastFetched.toLocaleString()
      );
      console.log(" - shouldUpdate: " + context.getters.shouldUpdate);
      if (!context.getters.shouldUpdate) {
        return;
      }
      const winningNumbers = await utils.getWinningNumbers();
      context.commit("setWinningNumbers", winningNumbers);
      context.commit("setLastFetched");
    },
    async loadTickets(context) {
      context.commit("setTickets", await ticketModel.listTickets());
    },
  },
  getters: {
    winningNumbers(state) {
      return state.winningNumbers;
    },
    shouldUpdate(state) {
      const lastFetched = state.lastFetched;
      if (!lastFetched) {
        return true;
      }
      const currentTimeStamp = new Date().getTime();
      return (currentTimeStamp - lastFetched) / 1000 > 3600;
    },
    tickets(state) {
      return state.tickets;
    },
    results(state) {
      return state.tickets.map((ticket) => {
        ticket.dates = `${ticket.startDate} – ${ticket.endDate}`;
        ticket.results = utils.getResults(ticket, state.winningNumbers);
        ticket.playsRemaining = ticket.results.filter(result => !result.winningNumbers).length;
        // ticket.picks[0].numbers = ticket.picks[0].numbers.join(", ");
        ticket.picks.map(pick => {
          pick.numbers = pick.numbers.join(", ");
          return pick;
        });
        ticket.prize = ticket.results
          .map((result) => result.prize)
          .reduce((a, b) => a + b, 0);
        return ticket;
      });
    },
  },
});
