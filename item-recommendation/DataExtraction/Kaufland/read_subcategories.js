() => {
  var subcategories = []
  var element = document.getElementsByClassName('rd-category-tiles')[0] ? document.getElementsByClassName('rd-category-tiles')[0].getElementsByTagName('a') : ''
  var subcategories_links = element ? element : []
  subcategories_links.forEach(function(link){
      subcategory = {}
      subcategory['name'] = link.getElementsByClassName('rd-tile__title')[0].innerText
      subcategory['url'] = link.href
      subcategory['category'] = /***0***/
      if(typeof link.href != 'undefined' && link.href != ''){
          subcategories.push(subcategory)
      }
  })
  return subcategories
}