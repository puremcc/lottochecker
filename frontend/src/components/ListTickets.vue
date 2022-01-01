<template>
  <v-card>
    <base-error :error="error" />
    <v-card-title
      >My Tickets<v-spacer /><v-card-actions class="text-right"
        ><v-btn
          @click="$emit('add-new-ticket')"
          title="Enter new ticket"
          fab
          small
          color="primary"
          ><v-icon>mdi-plus</v-icon></v-btn
        ></v-card-actions
      ></v-card-title
    >
    <!-- <v-list>
      <v-list-item v-for="ticket in myTicketsItems" :key="ticket.id">
        <v-card>
          <v-row>
            <v-col>{{ `${ticket.startDate} – ${ticket.endDate}` }}</v-col>
            <v-col>
              {{ "$" + ticket.prize }}
            </v-col>
          </v-row>
        </v-card>
      </v-list-item>
    </v-list> -->
    <v-data-table
      @item-selected="onItemSelected"
      :headers="myTicketsHeaders"
      :items="myTicketsItems"
      :items-per-page="3"
      sort-by="startDate"
      sort-desc
      v-model="selectedTicket"
      single-select
      item-key="startDate + endDate"
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
    </v-data-table>
  </v-card>
</template>
<script>
import BaseError from "./BaseError.vue";

export default {
  components: { BaseError },
  props: {
    isDataLoading: Boolean,
    getColor: Function
  },
  emits: ["addNewTicket", "selected-ticket"],
  data() {
    return {
      myTicketsHeaders: [
        { text: "Dates", value: "dates" },
        { text: "Numbers", value: "picks[0].numbers" },
        { text: "Plays Remaining", value: "playsRemaining" },
        { text: "Winnings", value: "prize" },
      ],
      selectedTicket: [],
      error: null,
    };
  },
  computed: {
    // Formatted for display in My Tickets data table.
    myTicketsItems() {
      return this.$store.getters.results.map((ticket, index) => {
        ticket.id = index;
        ticket.prize = "$" + ticket.prize;
        return ticket;
      });
    },
  },
  methods: {
    onItemSelected($event) {
      this.$emit("selected-ticket", $event.item);
    },
  },
};
</script>