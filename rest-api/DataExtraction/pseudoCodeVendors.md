## Data Fields in Vendors Data Extraction

Last update: Jun 30, 2021

# Kaufland

1. **Initial Web page:** 
    Visit https://filiale.kaufland.de/sortiment/das-sortiment.html
2. **Accept cookies:**
    Click on ``container ('.cookie-alert-extended-modal') > button ('.cookie-alert-extended-button')``
3. **Pagination:**
    For each page in ``('ul.m-pagination__list')`` until ``a('.m-pagination__link')['aria-label']=='Seite Weiter']`` is None => click
4. **Extract features:**
    Access individual items with container ``div.o-overview-list__list-item`` and extract the following:
    - Image => ``document.querySelector("div.o-overview-list__list-item img.a-image-responsive").src``
    - Brand => ``document.querySelector("div.o-overview-list__list-item h5.m-offer-tile__subtitle").innerText``
    - Product Title => ``document.querySelector("div.o-overview-list__list-item h4.m-offer-tile__title").innerText``
    - Content/Quantity => ``document.querySelector("div.o-overview-list__list-item div.m-offer-tile__quantity").innerText``
    - Price per Unit => ``document.querySelector("div.o-overview-list__list-item div.m-offer-tile__basic-price").innerText``
    - Discount (Optional) => ``document.querySelector("div.o-overview-list__list-item div.a-pricetag__discount").innerText`` Remarks: For Getränke it's just 'Probierpreis'
    - Old Price (Optional) => ``document.querySelector("div.o-overview-list__list-item div.a-pricetag__old-price").innerText``
    - Current Price => ``document.querySelector("div.o-overview-list__list-item .a-pricetag__price").innerText``
    - Category ?
    - Subcategory ?
    - Badges ?        
5. **Click on item for detailed information:**
    Click link ``a.m-offer-tile__link`` and extract =>
    - Thumbnail images ``document.querySelectorAll("div.o-product-gallery img").src`` (get the src for each image)
    - Product Description ``document.querySelector("div#section-description p").innerText``
    - Product Properties ``document.querySelector(".t-assortment-detail__properties").innerText``
    - Ingredients ``document.querySelector("div#section-composition p").innerText``
    - Preparation Instruction ``document.querySelector("div#section-preparationInstructions p").innerText``
    - Hints ``document.querySelector("div#section-hints p").innerText`` 
    - Manufacturer ``document.querySelector("div#section-producer p").innerText`` 

# Rewe
1. **Initial webpage** 
    Visit https://shop.rewe.de/c/obst-gemuese/

2. **Accept cookies**
    Click on ``container ('.uc-banner-content') > button ('#uc-btn-accept-banner')``
3. **Close page**
    It prompts another element called "How do you want to shop?"
    Click on Paketservice button ``button ('.gbmc-qa-parcel-intention')``
4. **Open and Visit Categories**
    - Click on ``(.nav-primary--item)`` to open the available links
    - Extract all category links from ``$('.nav-secondary--item a')``

    ``var links = document.querySelectorAll('.nav-secondary--item a')``
    ``for (i = 0; i< links.length;i++)``
    ``    console.log(links[i].href)``

    - https://shop.rewe.de/c/obst-gemuese/
    - https://shop.rewe.de/c/frische-kuehlung/
    - https://shop.rewe.de/c/tiefkuehl/
    - https://shop.rewe.de/c/nahrungsmittel/
    - https://shop.rewe.de/c/suesses-salziges/
    - https://shop.rewe.de/c/kaffee-tee-kakao/
    - https://shop.rewe.de/c/getraenke/
    - https://shop.rewe.de/c/wein-spirituosen-tabak/
    - https://shop.rewe.de/c/drogerie-kosmetik/
    - https://shop.rewe.de/c/baby-kind/
    - https://shop.rewe.de/c/kueche-haushalt/
    - https://shop.rewe.de/c/haus-freizeit/
    - https://shop.rewe.de/c/garten-outdoor/
    - https://shop.rewe.de/c/tier/

5. **Pagination**
    For each page in ``('div.style_paginationPagesContainer__2XX9y')`` until ``('.style_PostRequestGetFormButton__1ofsn')`` does not contain 'Enable' => click
    - Category => ``document.querySelector("h1.style_rsResultsTextHeadline__1gy-G").innerText``
6. **Extract features**
    Access individual items with container ``div.style_productDetailsWrapper__3HH6b`` and extract the following:
    - Image => ``document.querySelector("div.style_productDetailsWrapper__3HH6b img").src``
    - Brand => ``document.querySelector("div.style_productDetailsWrapper__3HH6b div.style_partnerName__1Uj1t").innerText``
    - Product Title => ``document.querySelector("div.style_productDetailsWrapper__3HH6b div.LinesEllipsis").innerText`` This field could be cut off due to long description
    - Content/Quantity => ``document.querySelector("div.style_productDetailsWrapper__3HH6b div.grammage_style_productGrammage__2129-").innerText`` 
    - Price per Unit => This information is present in the previous field (Content/Quantity)
    - Discount (Optional)
    - Old Price (Optional) => ``document.querySelector("div.style_productDetailsWrapper__3HH6b div.style_productOfferOriginalPrice__1GDnk").innerText`` 
    - Offer Duration (Optional) => ``document.querySelector("div.style_productDetailsWrapper__3HH6b div.style_productOfferDuration__2YaFN").innerText``
    - Current Price => ``document.querySelector("div.style_productDetailsWrapper__3HH6b div.style_productPrice__2_tkj").innerText`` When it's a package it includes a price range i.e. € 4.07 - € 11.71
    - Subcategory
    - Badges => ``document.querySelector("div.style_productDetailsWrapper__3HH6b svg")`` If not null, it's organic (could be a flag 0 | 1)
7. **Click on item for detailed information**
    Click link ``a.style_productDetailsLink__383Cq`` and extract =>
    - Product title => ``document.querySelector(".pdpr-Title").innerText``
    - Thumbnail images ``document.querySelectorAll("div.pdpr-ImageGallery__Thumbs img").src`` (get the src for each image)
    - Product Description ``document.querySelector(".pdpr-ReadMore").innerText``
    - Product Properties ``document.querySelectorAll('.pdpr-TabCordionItem__Content')[3].innerText`` [index 3] Includes Brand and Features
    - Ingredients ``document.querySelectorAll('.pdpr-TabCordionItem__Content')[0].innerText`` [index 0] Ingredients description
    - Preparation Instruction 
    - Hints ``document.querySelectorAll('.pdpr-TabCordionItem__Content')[2].innerText`` [index 2]
    - Manufacturer ``document.querySelectorAll('.pdpr-TabCordionItem__Content')[4].innerText`` [index 4] Includes Producer and Manufacturer
    - Nutritional Values ``document.querySelectorAll('.pdpr-TabCordionItem__Content')[1].innerText`` [index 1] Table with percentages %
    

# ALDI
1. **Initial webpage** 
    Visit https://www.aldi-sued.de/de/produkte/produktsortiment.html

2. **Accept cookies**
    Click on ``container ('.cookie-expiration-months') > button ('.js-privacy-accept')``

3. **Open and Visit Categories**
    - Extract all category links ``document.querySelectorAll('.wrapRichText .btn-primary')[2].href`` (Example link 2)

    ``var links = document.querySelectorAll('.wrapRichText .btn-primary')``
    ``for (i = 0; i< links.length;i++)``
    ``    console.log(links[i].href)``

    - https://www.aldi-sued.de/de/produkte/produktsortiment/kuehlung-und-tiefkuehlkost.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/nahrungsmittel.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/brot-aufstrich-und-cerealien.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/kaffee-und-tee.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/getraenke.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/suessigkeiten-und-snacks.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/drogerie-und-kosmetik.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/baby-und-kind.html
    - https://www.aldi-sued.de/de/produkte/produktsortiment/haushalt.html

4. **Pagination (Show all results)**
    For each page in previous list until ``(#showMore['data-npage']) > (#showMore['data-pagenumber']) `` => click ``(#showMore)`` to load all results
    The button contains 2 attributes: data-npage for current page and data-pagenumber for the last page on the internal pagination
    - Category => ``document.querySelector("h1.plp_title").innerText``
5. **Extract features**
    For each page (after loading all results) => extract
    Access individual items with container ``.wrapper`` and extract the following:
    - Image => ``document.querySelector(".item img").src``
    - Brand
    - Product Title => ``document.querySelector(".product-title").innerText`` This field could be cut off due to long description
    - Content/Quantity => ``document.querySelector(".additional-product-info").innerText`` 
    - Price per Unit => This information is present in the previous field (Content/Quantity) and it states Each, Package, Can, Bottle, etc
    - Discount (Optional)
    - Old Price (Optional) => ``document.querySelector(".price_before").innerText`` 
    - Offer Duration (Optional) => ``document.querySelector("div.style_productDetailsWrapper__3HH6b div.style_productOfferDuration__2YaFN").innerText``
    - Current Price => ``document.querySelector(".price").innerText``
    - Subcategory
    - Badges => ``document.querySelector(".topLeft img")`` If not null, it's organic (could get the src of the img) (Bio, Vegan, Best seller)
        
6. **Click on item for detailed information**
    Click link ``a.style_productDetailsLink__383Cq`` and extract =>
    - Product title => ``document.querySelector(".target_product_name").innerText``
    - Thumbnail images ``document.querySelectorAll("div.slick-track div")`` (get the src for each image from data-attributte: data-srcset-xs, data-srcset-sm, data-srcset-md, data-srcset-lg)
    - Product Description ``document.querySelector(".infobox").innerText``
    - Product Properties ``document.querySelectorAll('.product-description')[3].innerText``
    - Ingredients 
    - Preparation Instruction 
    - Hints 
    - Manufacturer 
    - Nutritional Values 
    

# EDEKA
1. **Initial webpage** 
    Visit https://www.edeka.de/eh/angebote.jsp

2. **Accept cookies**
    Click on ``container ('popin_tc_privacy') > button ('#popin_tc_privacy_button_2')``s

3. **Open and Visit Categories**
    Edeka does not show the prices for all its products, just for those with discounts.  

4. **Pagination (Show all results)**
    No pagination available for Angebote
5. **Extract features**
    Extract =>
    Access individual items with container ``.o-core-teaser-wall__teaser`` and extract the following:
    - Image => ``document.querySelector(".o-core-teaser-wall__teaser .a-core-image").src``
    - Brand
    - Product Title => ``document.querySelector(".m-core-m104-single-offer-teaser__content .a-core-headline").innerText`` This field could be cut off due to long description
    - Content/Quantity => ``document.querySelector(".o-core-teaser-wall__teaser p.a-core-copy").innerText`` 
    - Price per Unit => Included in the previouos field (Content/Quantity)
    - Discount (Optional) => ``document.querySelector(".a-core-offer-discount-badge__discount-inner").innerText`` 
    - Old Price (Optional) => ``document.querySelector(".price_before").innerText`` 
    - Offer Duration (Optional) => ``document.querySelector(".o-offers-offer-categories__store-information-item").innerText``
    - Current Price => ``document.querySelector(".a-core-offer-price-badge").innerText``
    - Category
    - Subcategory
    - Badges (Optional) => ``document.querySelector(".a-core-offer-discount-badge__label").innerText``   

6. **Click on item for detailed information**
    Cannot Click on any element for detailed information
    - Product title
    - Thumbnail images
    - Product Description
    - Product Properties
    - Ingredients
    - Preparation Instruction
    - Hints
    - Manufacturer
    - Nutritional Values
        
                                