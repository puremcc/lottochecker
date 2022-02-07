<template>
  <v-card>
    <base-error :error="error" />
    <v-card-title
      >Ticket Details
      <v-spacer />
      <v-card-actions
        ><v-btn @click="$emit('close-ticket-details')"
          >Close</v-btn
        ></v-card-actions
      >
    </v-card-title>
    <v-data-table
      :headers="ticketDetailHeaders"
      :items="ticketDetailItems"
      sort-by="drawingDate"
      :loading="isDataLoading"
      class="elevation-1"
    >
      <template v-slot:[`item.drawingDate`]="{ item }">
        {{ isoStringToLocaleString(item.drawingDate) }}
      </template>
      <template v-slot:[`item.prize`]="{ item }">
        <v-chip :color="getColor(item.prize)">
          {{ item.prize }}
        </v-chip>
      </template>
    </v-data-table>
  </v-card>
</template>
<script>
import BaseError from "./BaseError.vue";
import utils from "../utils";

export default {
  components: {
    BaseError,
  },
  props: {
    ticket: Object,
    dateKey: String,
    isDataLoading: Boolean,
  },
  data() {
    return {
      ticketDetailHeaders: [
        { text: "Drawing Date", value: "drawingDate" },
        { text: "Matches", value: "matches" },
        { text: "Prize", value: "prize" },
      ],
      error: null,
    };
  },
  computed: {
    ticketDetailItems() {
      var ticket;
      if (!this.ticket && this.dateKey) {
        ticket = this.$store.getters.results.find(
          (_) => this.dateKey == _.dates.replace(" – ", "-")
        );
      }
      return ticket.results.map((result, index) => {
        return {
          id: index,
          prize: result.prize !== null ? "$" + result.prize : "--",
          matches: result.matches ? result.matches.length : "--",
        };
      });
    },
  },
  methods: {
    getTicketResult(dateKey) {
      if (!this.ticket && dateKey) {
        this.ticket = this.$store.getters.results.find(
          (ticket) => dateKey == `${ticket.dates.replace(" - ", "#")}`
        );
      }
    },
    isoStringToLocaleString(isoDateString) {
      return utils.isoStringToLocaleString(isoDateString);
    },
    getColor(prize) {
      return utils.getColor(prize);
    },
  },
};
</script>