<template>
  <div class="container" v-if="this.$store.state.displayNotification">
    <div class="alert alert-success alert-dismissible fade show"
        style="width: 66.5%; margin-left: 5%;"
        v-if="this.$store.state.notificationType === 'Success'">
      <button type="button" class="close"
       @click="hideNotification">&times;</button>
      <strong>Success</strong> {{ this.$store.state.notificationMessage }}
    </div>

    <div class="alert alert-danger alert-dismissible fade show"
      style="width: 66.5%; margin-left: 5%;"
      v-if="this.$store.state.notificationType === 'Error'">
      <button type="button" class="close"
       @click="hideNotification">&times;</button>
      <strong>Error</strong> {{ this.$store.state.notificationMessage }}
    </div>

    <div class="alert alert-info alert-dismissible fade show"
      style="width: 66.5%; margin-left: 5%;"
      v-if="this.$store.state.notificationType === 'Info'">
      <button type="button" class="close"
        @click="hideNotification">&times;</button>
      <strong>Info</strong> {{ this.$store.state.notificationMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Notification',
  methods: {
    hideNotification() {
      this.$store.commit('hideNotification');
    },
  },
};
</script>

<style scoped>

</style>
