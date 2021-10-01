<template>
  <div class="container" style="margin-top: 10%; ">
    <h5>Base on:</h5>
    <form action="/action_page.php">
      <div class="form-check">
        <label class="form-check-label" for="radio1">
          <input type="radio" class="form-check-input" id="radio1"
          name="optradio" value="option1" checked>Recommended Only
        </label>
      </div>
      <div class="form-check">
        <label class="form-check-label" for="radio2">
          <input type="radio" class="form-check-input" id="radio2"
          name="optradio" value="option2">Discount Only
        </label>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RatingFilter',
};
</script>

<style scoped>

</style>
