<template>
  <div class="card border-primary" style="width: 18rem;">
    <div class="card-header">
      {{ title }}
    </div>
    <div class="image">
      <img :src="imageLink" class="card-img-top" :alt="imageAlt">
    </div>    
    <div class="card-body">
      
    </div>
    <div class="card-footer">
      <div class="btn-toolbar text-end">
        <div class="btn-group me-2">
          <p>{{ price }} Eur </p>
        </div>
        <div class="btn-group me-2">
          <button class="btn btn-primary">Add</button>
        </div>        
        <div class="btn-group">
          <button class="btn btn-primary"> Notify</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Product',
  props:{
    title: String,
    imageLink: String,
    imageAlt: String,
    price: Number
  }
}
</script>

<style>
.image{
  padding: 20px;
}
</style>