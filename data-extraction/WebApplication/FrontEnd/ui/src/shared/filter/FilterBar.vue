<template>
  <div class="filter">
    <VendorFilter/>
    <RatingFilter/>
  </div>
</template>

<script>
import VendorFilter from './VendorFilter.vue';
import RatingFilter from './RatingFilter.vue';

export default {
  name: 'FilterBar',
  components: {
    VendorFilter,
    RatingFilter,
  },
};
</script>

<style scoped>

</style>
