<template>
  <div>
    <div class="ui form">
      <div class="grouped fields">
        <h3><label>Vendors</label></h3>
        <div class="field" v-for="vendor in Object.keys(storeState)" :key="vendor">
          <div class="ui checkbox">
            <input type="checkbox" 
              :checked="storeState[vendor]"
              @click="() => toggleVendor(vendor)"/>
            <label>{{ vendor[0].toUpperCase() + vendor.slice(1).toLowerCase() }}</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VendorFilter',
  computed: {
    storeState(){
      return this.$store.state.vendorFilter;
    },
  },
  methods: {
    toggleVendor(vendor){
      this.$store.commit('toggleVendorFilter', { vendor });
    }
  }
}
</script>