<template>
  <div>
    <div v-if="this.$store.state.notify.display">
      <div class="ui red message" v-if="this.$store.state.notify.type == 'error'">
        <i class="close icon" @click="hideNotification"></i>
        <div class="header">
          Error
        </div>
        <p>{{ this.$store.state.notify.message }}</p>
      </div>
      <div class="ui blue message" v-if="this.$store.state.notify.type == 'info'">
        <i class="close icon" @click="hideNotification"></i>
        <div class="header">
          Info
        </div>
        <p>{{ this.$store.state.notify.message }}</p>
      </div>
      <div class="ui green message" v-if="this.$store.state.notify.type == 'success'">
        <i class="close icon" @click="hideNotification"></i>
        <div class="header">
          Success
        </div>
        <p>{{ this.$store.state.notify.message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Notification',
  methods: {
    hideNotification(){
      this.$store.commit('hideNotification');
    }
  }
}
</script>