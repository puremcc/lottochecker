<template>
  <span>
    <span v-if="isLoggedIn">
      <span id="username">{{ username }}</span>
      <v-menu left bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="signOut">Sign out</v-list-item>
        </v-list>
      </v-menu>
    </span>
    <span v-else>
      <v-btn @click="signIn" color="primary">Login</v-btn>
    </span>
  </span>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["username", "isLoggedIn"]),
    userHtml() {
      return `<v-btn icon>mdi-account</v-btn><span id="username">${
        this.username ?? ""
      }</span>`;
    },
  },
  methods: {
    ...mapActions(["signIn", "signOut"]),
  },
};
</script>
<style>
#user-icon {
  font-size: 1.1em;
}
#username {
  color: rgba(0, 0, 0, 0.5);
}
</style>