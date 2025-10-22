country = 'UK'
website_name = 'Bird Eyewear'
brand_name = 'Bird Eyewear'
website_url = 'https://www.birdeyewear.co.uk'
website_img_base_url = ''
no_prod_img_url_key = '__None__'

# fix brand name in json next time
#Css selectors
categories_selector = '#HeaderMenu-eyewear'
prod_link_selector = 'h3.card__heading.h5 .full-unstyled-link'
prod_name_selector = '.product__title h1'
prod_all_specs_selector = '__None__'
# variant_urls_selector = '(//variant-radios//script | //div[contains(@class, "product__media")]/img)[1])'
variant_urls_selector = 'variant-radios script, .product__media img'
# variant_urls_selector = 'variant-radios script'
# variant_urls_selector = '.product__media img'
variant_page_img_url_selector = ['featured_image', 'src']
main_variant_colors_selector = '__None__'
main_variant_sizes_selector = ':is(.product_description, .product__description, .product-description)'
variant_sku_selector = ['sku']
variant_color_selector = ['title']
variant_color_code_selector = '__None__'
variant_size_selector = '__None__'