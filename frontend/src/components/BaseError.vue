<template>
  <v-alert v-show="!!error" color="red" type="error">{{ error }}</v-alert>
</template>
<script>
export default {
  props: {
    error: String,
  },
};
</script>