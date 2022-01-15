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
    getColor: Function,
    isDataLoading: Boolean,
  },
  data() {
    return {
      ticketDetailHeaders: [
        { text: "Drawing Date", value: "drawingDate" },
        { text: "Matches", value: "matches" },
        { text: "Prize", value: "fprize" },
      ],
      error: null,
    };
  },
  computed: {
    ticketDetailItems() {
      return this.ticket.results.map((result, index) => {
        result.id = index;
        result.fprize = result.prize !== null ? "$" + result.prize : "--";
        result.matches = result.matches ? result.matches.length : "--";
        return result;
      });
    },
  },
  methods: {
    isoStringToLocaleString(isoDateString) {
      return utils.isoStringToLocaleString(isoDateString);
    },
  },
};
</script>