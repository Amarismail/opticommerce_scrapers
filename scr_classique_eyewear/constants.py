country = 'NA'
website_name = 'classique_eyewear'
website_url = 'https://www.classique-eyewear.com'
no_prod_img_url_key = '__None__'

#Css selectors
categories_selector = '#collectionsDropdown ul>li a'
# prod_link_selector = '#ctl00_MainContent_ucCollectionList_rptFrameList'
prod_link_selector = '[id^="ctl00_MainContent_ucCollectionList_rptFrameList"][id*="hdnFrameURL"]'
prod_name_selector = '#ctl00_MainContent_ucFrameViewer_lblStyleName'
prod_price_selector = '__None__'
prod_discounted_price_selector = '__None__'
# prod_all_specs_selector = '.woocommerce-product-attributes-item, #theCodeSpan'
prod_all_specs_selector = '#divFrameInfoText p'
variant_urls_selector = '//*[@id="portfolio-fullwidth"]//*[contains(@class, "linkModels")]/img/@src'
variant_page_img_url_selector = '#portfolio-fullwidth .linkModels > img'
all_variant_colors_selector = '#portfolio-fullwidth .linkModels'
all_variant_sizes_selector = '#divFrameInfoText p:nth-child(12)'
variant_page_color_selector = '__None__'
variant_page_size_selector = '__None__'
# variant_color_code_selector = '__None__'


# Eye = lens width
# DBL = bridge
# ED = Effective diameter
# SL = Temple length