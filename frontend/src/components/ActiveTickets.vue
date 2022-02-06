<template>
  <v-list>
    <v-list-item v-for="ticket in results()" :key="ticket.id">
      <v-card>
        <v-row>
          <v-col>{{ `${ticket.startDate} – ${ticket.endDate}` }}</v-col>
          <v-col>
            {{ "$" + ticket.prize }}
          </v-col>
        </v-row>
        <!-- <v-row>
            {{ ticket. }}
        </v-row> -->
      </v-card>
    </v-list-item>
  </v-list>
</template>
<script>

export default {
  data() {
    return {};
  },
  computed: {
    results() {
      return this.$store.getters.results.map((ticket, index) => {
        ticket.id = index;
        ticket.prize = "$" + ticket.prize;
        return ticket;
      });
    },
  },
};
</script>