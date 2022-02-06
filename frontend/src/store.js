import Vue from "vue";
import Vuex from "vuex";
import lotteryResults from "./models/lotteryResults";
import { Ticket } from "./models/tickets";
import utils from "./utils";

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
      var fromDate;
      var toDate;
      // Determine data range of winningNumbers to retrieve based on min/max of ticket dates.
      if (payload && "fromDate" in payload) {
        fromDate = payload.fromDate;
      } else {
        // Get earliest ticket startDate.
        let fromDates = context.state.tickets.map((_) => _.startDate);
        fromDates.sort((a, b) => a > b);
        fromDate = fromDates[0];
      }
      if (payload && "toDate" in payload) {
        toDate = payload.toDate;
      } else {
        // Get latest ticket endDate.
        let toDates = context.state.tickets.map((_) => _.startDate);
        toDates.sort((a, b) => a < b);
        toDate = toDates[0];
      }

      const winningNumbers = await lotteryResults.getWinningNumbers(
        context.state.accessToken,
        fromDate,
        toDate
      );
      context.commit("setWinningNumbers", winningNumbers);
    },
    async loadTickets(context) {
      let ticketService = new Ticket(context.state.accessToken);
      let tickets = await ticketService.listTickets();
      context.commit("setTickets", tickets);
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
      var results = [];
      results = state.tickets.map((ticket) => {
        let _results = utils.getResults(ticket, state.winningNumbers);
        return {
          dates: `${ticket.startDate} – ${ticket.endDate}`,
          results: _results,
          playsRemaining: _results.filter((_) => !_.winningNumbers).length,
          picks: ticket.picks,
          prize: _results
            .map((result) => result.prize)
            .reduce((a, b) => a + b, 0),
        };
      });
      return results;
    },
  },
});
