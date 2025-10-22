country = 'UK'
website_name = 'Gigi Studios'
website_url = 'https://offview.com'
no_prod_img_url_key = '__None__'
# this iss custom scraper

user_name = 'kiran.insight@gmail.com'
password = 'Insight@247!'

#Css selectors
login_email_selector = '.customer-layout-login input#CustomerEmail'
login_pass_selector = '.customer-layout-login input#CustomerPassword'

categories_selector = '.gigi-blocks-banner__media a'
# prod_link_selector = '#ctl00_MainContent_ucCollectionList_rptFrameList'
# prod_link_selector = "//li/div[1]/a[contains(@class, 'product-thumb-link')]"
prod_link_selector = 'li.item-product-add-cart .swiper-slide > a'
prod_name_selector = '.title h1'
prod_price_selector = '.price__container s.price-item--regular'
prod_discounted_price_selector = '.price__container .price-item--sale'
# prod_all_specs_selector = '.woocommerce-product-attributes-item, #theCodeSpan'
prod_all_specs_selector = '.variant-info li, .collapsible_tab-body p'
variant_urls_selector = '//*[@id="product-main-related"]//li[contains(@class, "active")]/a/@href'
variant_page_img_url_selector = 'slider-component  .image-magnify-lightbox'
all_variant_colors_selector = '__None__'
all_variant_sizes_selector = '__None__'
variant_page_color_selector = '__None__'
variant_page_size_selector = '__None__'
# variant_color_code_selector = '//*[@class="product-variants"]//li/span/span'


# Eye = lens width
# DBL = bridge
# ED = Effective diameter
# SL = Temple length