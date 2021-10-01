<template>
  <div class="container bg-light">
    <div class="form">
      <h5>Vendor</h5>
      <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" id="netto" checked>
        <label class="form-check-label" for="netto">
          Netto
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" id="rewe" checked>
        <label class="form-check-label" for="rewe">
          Rewe
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" id="aldi" checked>
        <label class="form-check-label" for="aldi">
          Aldi
        </label>
      </div>
    </div>

    <div class="form">
      <h5>Ratings</h5>
      <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="allratings" checked>
        <label class="form-check-label" for="allratings">
          All ratings
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="rating4">
        <label class="form-check-label" for="rating4">
          4 star and above
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="rating3">
        <label class="form-check-label" for="rating3">
          3 star and above
        </label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="rating2">
        <label class="form-check-label" for="rating2">
          2 star and above
        </label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Filter'
}
</script>

<style scoped>
.container .form{
  margin-top: 3vh;
}
.container h5{
  text-decoration: underline;
}
</style>