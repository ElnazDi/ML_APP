<!-- ABOUT THE PROJECT -->
# About The Project
Rest API to provide data about all collections from the vendors web app.

## Table of Contents
<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#build-with">Built With</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#folder-structure">Folder Structure</a></li>
      </ul>
    </li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started
The following instructions help you set up your project locally to execute the data extractors from different vendors.

### Built With
The data extractor for vendors was developed with the following python version:
  ```sh
  Nodejs 10.19.0
  ```

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/Big-Data-And-Data-Analytics/case-study-1-october2020-data-sweepers.git
   ```
2. Navigate to Customeer WebApp > Backend and install the dependencies within `package.json` file
   ```sh
   $ npm install
   ```
3. Enter the proper mongo db url in `Customer WebApp/Backend/config.json`
   ```JS
    uri = 'your_uri_connection'
    dbName = 'your_db'
   ```
4. The default port is 8000. You can change it on the `Customer WebApp/Backend/index.js` file
```JS
    app.listen(8000, ...
   ```
5. Execute the application
```JS
    node index.js
   ```
  If you have nodemon installed, you can run the following command
```JS
    npm start
   ```
6. Call the apis routes in `Customer WebApp/Backend/routes/product.js`, for example
```JS
    http://localhost:8000/product/discounts
    http://localhost:8000/product/all
  ```

### Folder structure

```sh
.
├── index.js
├── package.json
├── package-lock.json
├── config.json
├── models
│   └── cart.js
│   └── mongo.js
│   └── products.js
│   └── user.js
├── routes
│   ├── bookmark.js
│   └── cart.js
│   └── product.js
│   └── user.js
```

1. *models/*: Contains the entities to extract information from the db:
    - cart.js = defines the cart entity that can extract data from carts collection using the sinlge db connection
    - mongo.js = creates the single instance to connect to the db
    - product.js = defines the product entity that can extract data from products collection using the sinlge db connection
    - user.js = defines the user entity that can extract data from user collection using the sinlge db connection
2. *routes/*: Contains the endpoints of the application:
    - bookmark.js = exposes the available endpoints of all realted to bookmarks
    - cart.js = exposes the available endpoints of all realted to carts
    - product.js = exposes the available endpoints of all realted to products
    - user.js = exposes the available endpoints of all realted to users
4. index.js = runs the app 