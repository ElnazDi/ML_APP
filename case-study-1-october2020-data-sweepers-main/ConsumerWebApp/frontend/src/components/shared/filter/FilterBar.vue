<template>
  <div>
    <div class="row">
      <VendorFilter/>
    </div>
  </div>
</template>

<script>
import VendorFilter from './VendorFilter.vue';

export default {
  name: 'FilterBar',
  components: {
    VendorFilter,
  }
}
</script>