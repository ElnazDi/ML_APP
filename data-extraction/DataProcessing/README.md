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
  Docker 20.10.08
  image => apache/airflow:2.1.4-python3.8
  ```

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/Big-Data-And-Data-Analytics/case-study-1-october2020-data-sweepers.git
   ```
2. Build the docker image from `Dockerfile` within the DataProcessing folder as follows
   ```sh
   $ docker build . -f Dockerfile --tag vendors:0.0.1
   ```
3. Run the `docker-compose.yaml` file within the DataProcessing folder
   ```sh
    docker-compose up
   ```
4. Navigate to 'http://localhost:8080/home' (The current port is 8080. The docker-compose file contains this configuration by default)

5. Once on the home page you'll see two workflows: `dataExtraction` and `etl`
  - dataExtraction: Runds the web crawlers to extract data from vendor's websites
  - etl: Runds the data cleaning rules to generate the final data we use for ML models and display on web app

6. Add steps for scheduling

