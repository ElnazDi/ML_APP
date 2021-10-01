<template>
  <div>
    <page-header/>
    <div class="row">
      <div class="col-sm-2">
        <filter-component/>
      </div>
      <div class="col-sm-8">
        <div class="container products">
          <product-component class="product"
            imageLink = 'https://media.kaufland-online.de/images/items/200x200/85b7b36525271088bede2324b2b33001.jpg' 
            imageAlt="A bicycle" 
            title="Fischer Alu City Ebike" 
            price=1111,00 />
          <product-component class="product"
            imageLink = 'https://media.kaufland-online.de/images/items/200x200/85b7b36525271088bede2324b2b33001.jpg' 
            imageAlt="A bicycle" 
            title="Fischer Alu City Ebike" 
            price=1111,00 />
          <product-component class="product"
            imageLink = 'https://media.kaufland-online.de/images/items/200x200/85b7b36525271088bede2324b2b33001.jpg' 
            imageAlt="A bicycle" 
            title="Fischer Alu City Ebike" 
            price=1111,00 />
          <product-component class="product"
            imageLink = 'https://media.kaufland-online.de/images/items/200x200/85b7b36525271088bede2324b2b33001.jpg' 
            imageAlt="A bicycle" 
            title="Fischer Alu City Ebike" 
            price=1111,00 />
          <product-component class="product"
            imageLink = 'https://media.kaufland-online.de/images/items/200x200/85b7b36525271088bede2324b2b33001.jpg' 
            imageAlt="A bicycle" 
            title="Fischer Alu City Ebike" 
            price=1111,00 />
        </div>
      </div>
      <div class="col-sm-2">

      </div>
    </div>
  </div>
</template>

<script>
import PageHeader from './PageHeader.vue'
import FilterComponent from './FilterComponent.vue'
import ProductComponent from './ProductComponent.vue'

export default{
  name: 'Home',
  components: {
    PageHeader,
    FilterComponent,
    ProductComponent
  }  
}
</script>

<style scoped>
.products{
  margin-top: 3vh;
  display: flex;
  max-width: 70vw;
}
.product{
  margin-right: 1vh;
  min-width: 300px;
}
</style>