<template>
  <v-app>
    <v-app-bar app>
      <h2>Lotto Checker</h2>
      <v-spacer></v-spacer>
      <user-auth />
    </v-app-bar>
    <v-main v-if="isLoggedIn">
      <v-container>
        <base-error :error="error" />
        <v-row>
          <v-col>
            <enter-ticket
              v-if="showEnterNewTicket"
              @saved="onNewTicketSaved"
              @canceled="onNewTicketCanceled"
            /> </v-col
        ></v-row>
        <v-row>
          <v-col>
            <list-tickets
              :isDataLoading="isDataLoading"
              :get-color="getColor"
              @selected-ticket="onTicketSelected"
              @add-new-ticket="showEnterNewTicket = true" /></v-col
        ></v-row>
        <v-row>
          <v-col>
            <ticket-details
              :ticket="selectedTicket"
              v-if="!!selectedTicket && !isDataLoading"
              :isDataLoading="isDataLoading"
              :get-color="getColor"
              @close-ticket-details="selectedTicket = null"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import UserAuth from './components/UserAuth'
import EnterTicket from "./components/EnterTicket.vue";
import ListTickets from "./components/ListTickets.vue";
import TicketDetails from "./components/TicketDetails";
import BaseError from "./components/BaseError.vue";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "app",
  components: {
    UserAuth,
    EnterTicket,
    ListTickets,
    TicketDetails,
    BaseError,
  },
  async created() {
    try {
      this.isDataLoading = true;
      await this.loadWinningNumbers();
      await this.loadTickets();
      this.isDataLoading = false;
    } catch (error) {
      this.error = error;
    } finally {
      this.isDataLoading = false;
    }
  },
  data() {
    return {
      selectedTicket: null,
      showEnterNewTicket: false,
      isDataLoading: false,
      error: null,
    };
  },
  computed: {
    ...mapGetters(["winningNumbers", "isLoggedIn"]),
  },
  methods: {
    ...mapActions(["loadAuthState", "loadWinningNumbers", "loadTickets"]),
    async onNewTicketSaved() {
      this.showEnterNewTicket = false;
    },
    onNewTicketCanceled() {
      this.showEnterNewTicket = false;
    },
    onTicketSelected(ticket) {
      this.selectedTicket = ticket;
    },
    getColor(winnings) {
      let _winnings = +winnings.substring(1);
      if (_winnings > 0 && _winnings < 1000) return "yellow";
      if (_winnings >= 1000) return "green";
    },
  },
};
</script>
