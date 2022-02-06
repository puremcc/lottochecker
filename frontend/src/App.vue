<template>
  <v-app>
    <v-app-bar app>
      <h2>Lotto Checker</h2>
      <v-spacer></v-spacer>
      <router-link :to="'/tickets/active'">Active Tickets</router-link>
      <v-spacer></v-spacer>
      <user-auth />
    </v-app-bar>
    <v-main v-if="isLoggedIn">
      <v-container>
        <base-error :error="error" />
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import UserAuth from "./components/UserAuth";
import BaseError from "./components/BaseError.vue";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "app",
  components: {
    UserAuth,
    BaseError,
  },
  async created() {
    try {
      await this.loadAuthState();
      if (this.isLoggedIn) {
        this.isDataLoading = true;
        await this.loadTickets();
        await this.loadWinningNumbers();
        this.isDataLoading = false;
      }
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
    ...mapActions(["loadAuthState", "loadTickets", "loadWinningNumbers"]),
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
