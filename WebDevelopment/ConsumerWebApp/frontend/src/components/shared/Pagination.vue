<template>
  <div>
    <button :class="getPreviousButtonClass" @click="firstPage">
      <i class="angle double left icon"></i>
    </button>
    <button :class="getPreviousButtonClass" @click="previousPage">
      <i class="angle left icon"></i>
    </button>
    <span> {{ current }} </span>
    <button :class="getNextButtonClass" @click="nextPage">
      <i class="angle right icon"></i>
    </button>
    <button :class="getNextButtonClass" @click="lastPage">
      <i class="angle double right icon"></i>
    </button>
  </div>  
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    context: String,
    fieldName: String,
    length: Number,
    itemsPerPage: Number,
  },
  data() {
    return {
      current: 1,
      maxPage: Math.ceil(this.length / this.itemsPerPage),
    }
  },
  computed: {
    getPreviousButtonClass() {
      const buttonClass = ["ui" , "icon", "button"];
      if(this.current == 1){
        buttonClass.push("disabled");
      }
      return buttonClass;
    },
    getNextButtonClass() {
      const buttonClass = ["ui" , "icon", "button"];
      if(this.current >= this.maxPage){
        buttonClass.push("disabled");
      }
      return buttonClass;
    },
  },
  methods: {
    firstPage() {
      this.current = 1;
      this.$emit('pageChanged', {
        context: this.context,
        field: this.fieldName,
        page: this.current
      })
    },
    lastPage() {
      this.current = this.maxPage;
      this.$emit('pageChanged', {
        context: this.context,
        field: this.fieldName,
        page: this.current
      })
    },
    nextPage() { 
      this.current += 1;
      this.$emit('pageChanged', {
        context: this.context,
        field: this.fieldName,
        page: this.current
      })
    },
    previousPage() {
      this.current -= 1;
      this.$emit('pageChanged', {
        context: this.context,
        field: this.fieldName,
        page: this.current
      })
    }
  }
}
</script>