# check if the request for getting product is switching pages based on request data for next run

country = 'UK'
website_name = 'Avalon Eyewear'
brand_name = 'Parade'
# website_url = 'http://www.avaloneyewear.com/'
website_url = 'http://www.avaloneyewear.com/collections/parade/'
website_img_base_url = 'http://www.avaloneyewear.com/showimage.aspx?img='
no_prod_img_url_key = '__None__'

# fix brand name in json next time
#Css selectors
categories_selector = 'ul.brandNav_PR > li:not(:first-child):not(:last-child) a'
prod_link_selector = '.detailNav'
prod_name_selector = '#ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_ctrFrameDetail_lblFrameName'
prod_all_specs_selector = '__None__'
variant_urls_selector = '#ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_ctrFrameDetail_rptColors a'
variant_page_img_url_selector = '#ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_ctrFrameDetail_rptColors a'
main_variant_colors_selector = '#ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_ctrFrameDetail_rptColors a'
main_variant_sizes_selector = '.detailSize_PR span'
variant_color_selector = '__None__'
variant_color_code_selector = '__None__'
variant_size_selector = '__None__'