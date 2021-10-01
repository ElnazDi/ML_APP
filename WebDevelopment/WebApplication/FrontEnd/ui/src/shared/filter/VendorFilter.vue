<template>
  <div class="container" style="margin-top: 10%;">
    <h5>Vendors:</h5>
    <div class="form-check">
      <label class="form-check-label" for="check1">
        <input type="checkbox" class="form-check-input"
        checked @click="() => toggleVendor('aldi')"/>ALDI
      </label>
    </div>
    <div class="form-check">
      <label class="form-check-label" for="check2">
        <input type="checkbox" class="form-check-input"
        checked @click="() => toggleVendor('rewe')"/>Rewe
      </label>
    </div>
    <div class="form-check">
      <label class="form-check-label">
        <input type="checkbox" class="form-check-input"
        checked @click="() => toggleVendor('netto')"/>Netto
      </label>
    </div>
    <div class="form-check">
      <label class="form-check-label">
        <input type="checkbox" class="form-check-input"
        checked @click="() => toggleVendor('kaufland')"/>Kaufland
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VendorFilter',
  methods: {
    toggleVendor(vendor) {
      this.$store.commit('updateFilters', vendor);
    },
  },
};
</script>

<style scoped>

</style>
