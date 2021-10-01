# Extractor.md

- Create a new configuration file under the config folder with an appropriate name
- The required keys to be specified in the file would be 
  - [ ] homepage: default homepage of the website to be loaded
  - [ ] cookieModal: cookie modal that would appear if the website is loaded 
  - [ ] cookieButton: cookie button that needs to be clicked for the selected model
  - [ ] paginationButton: button on website to click next page 
  - [ ] parentSelector: a class that represents each list item on the page
  - [ ] children: an array of detailed instructions 
    - Each object of the children must contain the following pattern of JSON
    - [ ] selector: selector of the property within the item that needs to be extracted
    - [ ] tag: field with which data needs to be stored in DB
    - [ ] property: property of the selected element that needs to be accessed such as 'innerHTML', 'href', 'src' etc..
