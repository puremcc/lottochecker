<template>
  <!-- Enter Ticket -->

  <v-card>
    <v-card-title>Enter new ticket</v-card-title>
    <v-card-text>
      <v-form class="mb-10">
        <v-row>
          <v-col class="text-left form-group">
            <label for="start-date" class="mr-2">Start date</label>
            <input id="start-date" type="date" v-model="ticket.startDate" />
          </v-col>
          <v-col class="text-left form-group">
            <label for="end-date" class="mr-2">End date</label>
            <input id="end-date" type="date" v-model="ticket.endDate" />
          </v-col>
          <v-spacer />
          <!-- Start date -->
          <!-- <v-col cols="12" sm="6" md="4">
                <v-dialog
                  ref="dialog"
                  v-model="modal"
                  :return-value.sync="ticket.startDate"
                  persistent
                  width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="ticket.startDate"
                      label="Start date"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="ticket.startDate"
                    :allowed-dates="allowedDates"
                    scrollable
                  >
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="modal = false">
                      Cancel
                    </v-btn>
                    <v-btn
                      text
                      color="primary"
                      @click="$refs.dialog.save(ticket.startDate)"
                    >
                      OK
                    </v-btn>
                  </v-date-picker>
                </v-dialog>
              </v-col> -->
          <!-- End date -->
          <!-- <v-col cols="12" sm="6" md="4">
                <v-dialog
                  ref="dialog"
                  v-model="modal"
                  :return-value.sync="ticket.endDate"
                  persistent
                  width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="ticket.endDate"
                      label="End date"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="ticket.endDate"
                    :allowed-dates="allowedDates"
                    scrollable
                  >
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="modal = false">
                      Cancel
                    </v-btn>
                    <v-btn
                      text
                      color="primary"
                      @click="$refs.dialog.save(ticket.endDate)"
                    >
                      OK
                    </v-btn>
                  </v-date-picker>
                </v-dialog>
              </v-col> -->
        </v-row>
        <v-row class="form-group ml-1">
          <v-col>
            <v-row><label>My numbers</label></v-row>
            <v-row class="pick">
              <v-text-field
                v-for="(number, i) in ticket.picks[0].numbers"
                :key="i"
                v-model="ticket.picks[0].numbers[i]"
                type="number"
                solo
                dense
                :rules="[(val) => 1 <= +val <= 99 || 'Must be a number']"
              />
            </v-row>
          </v-col>
        </v-row>
        <v-row>
          <v-card-actions>
            <v-btn
              type="cancel"
              @click.prevent="onCancel"
              right
              class="ml-auto mr-5"
              >Cancel</v-btn
            >
            <v-btn
              type="submit"
              @click.prevent="saveTicket"
              color="primary"
              right
              class="ml-auto mr-5"
              >Save Ticket</v-btn
            >
          </v-card-actions>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import utils from "../utils";

const today = () => new Date().toISOString().substring(0, 10);

export default {
  name: "EnterTicket",
  emits: ["saved", "canceled"],
  data() {
    return {
      ticket: {
        startDate: today(),
        endDate: today(),
        picks: [{ numbers: new Array(6) }],
      },
      modal: false,
      allowedDates: utils.isValidDrawingDate,
      ticketSaved: false,
      error: "",
    };
  },
  methods: {
    async saveTicket() {
      await this.$store.dispatch("saveTicket", {
        ticket: this.ticket,
      });
      this.ticketSaved = true;
      this.$emit("saved");
      this.resetTicket();
    },
    resetTicket() {
      this.ticket = {
        startDate: today(),
        endDate: today(),
        picks: [{ numbers: new Array(6) }],
      };
    },
    onCancel() {
      this.$emit("canceled");
      this.resetTicket();
    },
  },
};
</script>

<style>
.pick .v-input.v-text-field {
  margin: 0 3px;
  max-width: 3em;
}
.pick input {
  width: 1em;
  text-align: center;
}
input[type="date"] {
  max-width: 130px;
}
/**
 * Hide arrows from number inputs.
 */
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
/* Firefox */
input[type="number"] {
  -moz-appearance: textfield;
}
</style>