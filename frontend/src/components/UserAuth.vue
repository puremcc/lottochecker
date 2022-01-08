<template>
  <span>
    <b-nav-item-dropdown v-if="isLoggedIn" :html="userHtml" right>
      <b-dropdown-item href="#" @click="signOut">Sign out</b-dropdown-item>
    </b-nav-item-dropdown>

    <b-nav-item v-else :html="userHtml" right>
      <b-button @click="signIn" variant="primary">Sign in</b-button>
    </b-nav-item>
  </span>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['username', 'isLoggedIn']),
    userHtml() {
      return `<i id="user-icon" class="bi bi-person-fill mr-2"></i><span id="username">${
        this.username ?? ''
      }</span>`
    },
  },
  methods: {
    ...mapActions(['signIn', 'signOut']),
  },
}
</script>
<style>
#user-icon {
  font-size: 1.1em;
}
</style>