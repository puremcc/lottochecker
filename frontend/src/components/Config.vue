<template>
  <!-- <v-list>
    <v-list-item v-for="key in Object.keys(config)" :key="key">
      <v-card>
        <v-row>
          <v-col>
            <pre>{{ key }}</pre>
          </v-col>
          <v-col>
            <pre>{{ config[key] }}</pre>
          </v-col>
        </v-row>
      </v-card>
    </v-list-item>
  </v-list> -->
  <v-data-table :items="config" class="elevation-1"></v-data-table>
</template>
<script>
export default {
  data() {
    return {
      config: [
        { API_URL: process.env.VUE_APP_API_URL },
        { AUTH_URL: process.env.VUE_APP_AUTH_URL },
      ],
    };
  },
};
</script>