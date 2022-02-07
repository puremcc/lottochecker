<template>
  <v-card>
    <base-error :error="error" />
    <v-card-title
      >My Tickets<v-spacer /><v-card-actions class="text-right">
        <router-link :to="'/tickets/create'">
          <v-btn title="Enter new ticket" fab small color="primary"
            ><v-icon>mdi-plus</v-icon></v-btn
          >
        </router-link>
      </v-card-actions></v-card-title
    >
    <v-data-table
      @item-selected="onItemSelected"
      :headers="myTicketsHeaders"
      :items="myTicketsItems"
      :items-per-page="3"
      sort-by="dates"
      sort-desc
      v-model="selectedTicket"
      single-select
      item-key="id"
      show-select
      :loading="isDataLoading"
      per-page="5"
      class="elevation-1"
    >
      <template v-slot:[`item.prize`]="{ item }">
        <v-chip :color="getColor(item.prize)">
          {{ item.prize }}
        </v-chip>
      </template>
      <template v-slot:[`item.details`]="{ item }">
        <router-link :to='`/tickets/${item.dateRange}`'
          ><v-icon small class="mr-2">
            mdi-information-outline
          </v-icon></router-link
        >
        <!-- <v-icon small @click="console.log(item)"> mdi-delete </v-icon> -->
      </template>
    </v-data-table>
  </v-card>
</template>
<script>
import BaseError from "./BaseError.vue";
import utils from "../utils";

export default {
  components: { BaseError },
  props: {
    isDataLoading: Boolean,
  },
  emits: ["addNewTicket", "selected-ticket"],
  data() {
    return {
      myTicketsHeaders: [
        { text: "Dates", value: "dates" },
        { text: "Numbers", value: "picks[0].numbers" },
        { text: "Plays Remaining", value: "playsRemaining" },
        { text: "Winnings", value: "prize" },
        { text: "Details", value: "details" },
      ],
      selectedTicket: [],
      error: null,
    };
  },
  computed: {
    // Formatted for display in My Tickets data table.
    myTicketsItems() {
      return this.$store.getters.results.map((ticket, index) => {
        return {
          id: index,
          dates: ticket.dates,
          dateRange: ticket.dates.replace(' – ', '-'),
          playsRemaining: ticket.playsRemaining,
          prize: "$" + ticket.prize,
          picks: ticket.picks.map((pick) => {
            return { numbers: pick.numbers.join(", ") };
          }),
        };
      });
    },
  },
  methods: {
    onItemSelected($event) {
      this.$emit("selected-ticket", $event.item);
    },
    getColor(prize) {
      return utils.getColor(prize);
    },
  },
};
</script>