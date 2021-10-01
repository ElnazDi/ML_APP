<template>
  <div>
    <page-header/>
    <register/> 
  </div>
</template>

<script>
import PageHeader from './PageHeader.vue'
import Register from './RegisterComponent.vue'

export default{
  name: 'Login',
  components: {
    PageHeader,
    Register
  }
}
</script>
