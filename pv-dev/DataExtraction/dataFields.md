## Data Fields in Vendors Data Extraction

Last update: Jun 25, 2021

| Field                         | Description    |  Datatype |  Required              | Netto         | Kaufland     | Third Vendor* |
| :-------------                | :----------:   | :----------: | :----------:           | :-----------:  | :-----------: |  :-----------: |
| product_title                 | Product description | String | Required      | Yes             |     Yes        |
| product_label                 | Additional detailed information according to the vendor | String  | Optional           |              |     Yes        |
| product_image                 | Image URL of the product | String  | Required           | Yes             |     Yes        |
| product_rating                | Product rating based on the vendors website's | String | Optional            | Yes             |           |
| product_price                 | Current product price | String | Required             | Yes             |     Yes        |
| product_base_price            | Product price per quantity. For example, 1 KG = 3.38 EUR  | String  | Required        | Yes             |     Yes        |
| product_original_price        | Original price of the product before its discount | String  | Optional           | Yes             |     Yes        |
| product_discount              | Discount from the current date (as %) | String  | Optional          | Yes             |     Yes        |
| product_category              | Food category to which this product belongs to. For instance, Kühlprodukte.  | String | Required       | Yes             |     Yes        |
| product_subcategory           | Food subcategory to which this product belongs to. For instance, Brot & Backwaren. It will show the same category name if any is not especified. | String   | Required         | Yes             |     Yes       |
| product_ingredients           | List of product ingredients. It could be just a description or a list with percentages. | String  | Required  |    |   Yes*          |
| product_brand                 |  | String | Optional            |              |     Yes*        |
| product_vendor                | Vendor where this product can be found  | String | Required          | Yes             |     Yes        |
| product_availability          | Indicates whether the product is still available or not   | String   | Optional       |              |     Yes       |
| product_insert_dt             | Date in which this product is being extracted   | datetime | Required         | Yes             |     Yes       |

*Fields that still need to be processed and extracted