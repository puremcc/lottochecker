import Vue from "vue";
import Vuex from "vuex";
import utils from "./utils";
import lotteryResults from "./models/lotteryResults";
import { Ticket } from "./models/tickets";

import Amplify, { Auth } from "aws-amplify";
import awsconfig from "./aws-exports";

Vue.use(Vuex);
Amplify.configure(awsconfig);

export const store = new Vuex.Store({
  state() {
    return {
      username: null,
      accessToken: null,
      winningNumbers: [],
      tickets: [],
      ticketResults: [],
    };
  },
  mutations: {
    setUser(state, payload) {
      state.username = payload.username;
      state.accessToken = payload.accessToken;
    },
    setWinningNumbers(state, payload) {
      state.winningNumbers = payload;
    },
    setTickets(state, payload) {
      state.tickets = payload;
    },
    setTicketResults(state, payload) {
      state.ticketResults = payload;
    },
  },
  actions: {
    /* Auth */
    async loadAuthState(context) {
      try {
        const user = await Auth.currentAuthenticatedUser();
        context.commit("setUser", {
          username: user.signInUserSession.idToken.payload.email,
          accessToken: user.signInUserSession.accessToken.jwtToken,
        });
      } catch (error) {
        return;
      }
    },
    async signIn() {
      try {
        await Auth.federatedSignIn();
      } catch (error) {
        console.log("Error signing in", error);
        throw error;
      }
    },
    async signOut() {
      try {
        await Auth.signOut();
      } catch (error) {
        console.log("Error signing out: ", error);
        throw error;
      }
    },
    async loadWinningNumbers(context, payload) {
      console.log("loadWinningNumbers...");
      const winningNumbers = await lotteryResults.getWinningNumbers(
        context.state.accessToken,
        payload.fromDate,
        payload.toDate
      );
      context.commit("setWinningNumbers", winningNumbers);
    },
    async loadTickets(context) {
      let ticketService = new Ticket(context.state.accessToken);
      let tickets = await ticketService.listTickets();
      context.commit("setTickets", tickets);
    },
    async loadTicketResults(context) {
      await context.dispatch("loadTickets");

      // Determine data range of winningNumbers to retrieve based on min/max of ticket dates.
      // Get earliest ticket startDate.
      let fromDates = context.state.tickets.map((_) => _.startDate);
      fromDates.sort((a, b) => a > b);
      let fromDate = fromDates[0];

      // Get latest ticket endDate.
      let toDates = context.state.tickets.map((_) => _.startDate);
      toDates.sort((a, b) => a < b);
      let toDate = toDates[0];

      await context.dispatch("loadWinningNumbers", { fromDate, toDate });

      // Generate ticket results.
      const ticketResults = context.state.tickets.map((ticket) => {
        ticket.dates = `${ticket.startDate} – ${ticket.endDate}`;
        ticket.results = utils.getResults(ticket, context.state.winningNumbers);
        ticket.playsRemaining = ticket.results.filter(
          (result) => !result.winningNumbers
        ).length;
        ticket.picks.map((pick) => {
          pick.numbers = pick.numbers.join(", ");
          return pick;
        });
        ticket.prize = ticket.results
          .map((result) => result.prize)
          .reduce((a, b) => a + b, 0);
        return ticket;
      });
      context.commit("setTicketResults", ticketResults);
    },
    async saveTicket(context, payload) {
      let ticketModel = new Ticket(context.state.accessToken);
      await ticketModel.createTicket(payload.ticket);
      context.dispatch("loadTickets");
    },
  },
  getters: {
    username(state) {
      return state.username;
    },
    isLoggedIn(state) {
      return !!state.accessToken;
    },
    accessToken(state) {
      return state.accessToken;
    },
    winningNumbers(state) {
      return state.winningNumbers;
    },
    tickets(state) {
      return state.tickets;
    },
    results(state) {
      return state.ticketResults;
    },
  },
});
