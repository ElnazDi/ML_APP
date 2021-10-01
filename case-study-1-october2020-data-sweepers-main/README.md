<!-- ABOUT THE PROJECT -->
# About The Project
Integration platform that regularly collects product data from multiple online websites of different vendors and allows a user to make a better choice in buying items from specific vendors.

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
      </ul>
    </li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started
The following instructions help you set up your project locally to execute the data extractors from different vendors.

### Build With
The data extractor for vendors was developed with the following python version:
  ```sh
  Python 3.8.5
  ```

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/Big-Data-And-Data-Analytics/case-study-1-october2020-data-sweepers.git
   ```
2. Install dependencies from `requirements.txt` file
   ```sh
   $ pip install -r requirements.txt
   ```
3. Enter database name and url python connection in `DataExtraction/config.py`
   ```PY
    MONGO_DB = 'your_db'
    MONGO_URL = 'your_mongo_url_connection_string'
   ```
4. Execute Kaufland extractor
```PY
    python getDataKaufland.py
   ```
5. Execute Netto extractor
```PY
    python getDataNetto.py
   ```
