from utils.utils import (
    initialize_master_json,
    initialize_browser,
    exists_in_master_json,
    delay,
    get_current_time_iso,
    setup_folder,
    normalize_url)
from utils.scraper_utils import (
    browser_login_to_website,
    visit_browser_page,
    visit_html_page, 
    request_website_api, 
    get_frame_size, 
    is_currency_symbol,
    scraper_run_details,
    get_product_type)
from scraper_fn import (
    get_prod_final_image,
    map_variants_info_tags,
    extract_specs_using_map_keywords,
    config_variant_request,
    config_store_page_request,
    get_quatre_img)
from utils.logging_utils import setup_logging
from random import randint
import requests
import urllib.parse
import config
import json
import logging
import constants
import mappings
import re

def get_categories(in_page):
    categories = {}
    categories_tags = in_page.select(constants.categories_selector)
    for categories_tag in categories_tags:
        category_link = constants.website_url
        if categories_tag.has_attr('href'):
            is_external_link, normalized_url = normalize_url(constants.website_url, categories_tag['href'])
            if is_external_link:
                logging.warning(f'Got external link in category: {categories_tag['href']}')
                continue
            category_link = normalized_url
        category_text = categories_tag.text.strip()
        if not category_text or category_text == '':
            category_text = category_link.split('/')[-1].replace('-', ' ')
        categories[category_text] = category_link

    return categories

def get_categories_prod_url(session, context, categories_dict):
    total_products = 0
    in_myproduct_urls_dict = {}
    for category_name, category_link in categories_dict.items():
        logging.info(f'scraping category: {category_name}....')
        logging.info(f'scraping category: {category_link}....')
        in_myproduct_urls = get_prod_urls(
            session,
            context,
            category_name,
            category_link,
            in_myproduct_urls = [],
            )
        in_myproduct_urls = list(set(in_myproduct_urls))
        in_myproduct_urls_dict[category_name] = in_myproduct_urls
        total_products = total_products + len(in_myproduct_urls)
    
    return in_myproduct_urls_dict, total_products

def get_prod_urls(session, context, category_name, category_link,in_myproduct_urls, page_num = 1):
    
    category_prod_page_link, params = config_store_page_request(category_name, category_link, page_num)
    print('-------------------------------')
    print(category_prod_page_link)
    print(params)
    resp_status_code, in_page = visit_html_page(session, category_prod_page_link, config.headers, params=params)
    logging.info(f'response status: {resp_status_code}')

    prod_url_tags = in_page.select(constants.prod_link_selector)
    if not prod_url_tags and page_num == 1:
        in_page = visit_browser_page(context, category_link)
        prod_url_tags = in_page.select(constants.prod_link_selector)

    if not prod_url_tags:
        return in_myproduct_urls
    
    for prod_url_tag in prod_url_tags:
        tag_name = prod_url_tag.name
        prod_url = prod_url_tag.get('href') if tag_name == 'a' else prod_url_tag.get('value') if tag_name == 'input' else None
        prod_normalize_url = re.sub(r'^~', '', prod_url)
        is_external_link, prod_normalize_url  = normalize_url(constants.website_url, prod_normalize_url, include_query=False)
        if prod_normalize_url:
            in_myproduct_urls.append(prod_normalize_url)

    if not config.website_prod_store_url_navigation:
        return in_myproduct_urls

    milliseconds = randint(1, 3) * 1000
    delay(milliseconds)

    page_num = page_num + 1
    # if page_num >= 2:
    #     return in_myproduct_urls
    in_myproduct_urls = get_prod_urls(session, context, category_name, category_link, in_myproduct_urls, page_num)

    return in_myproduct_urls

def get_variants(in_page, json_var_obj, session, prod_item_num, prod_color_tag, prod_size_tag, variant_url_tag): # added in_page for offview need to review
    from functools import reduce
    from operator   import getitem

    print('get_variants')
    variant_color = prod_color_tag.get_text(strip=True).strip() if prod_color_tag else None
    variant_size = prod_size_tag.get_text(strip=True).strip() if prod_size_tag else None
    variant_url = variant_url_tag

    if config.imbedded_variants_json_data:
        variant_url = reduce(getitem, constants.variant_page_img_url_selector, variant_url_tag) # used to navigate and extract value from a json obj based on keys in selector
        if constants.variant_color_selector:
            variant_color = reduce(getitem, constants.variant_color_selector, variant_url_tag)
            variant_sku = reduce(getitem, constants.variant_sku_selector, variant_url_tag)
            json_var_obj['$iProduct_SKU'] = variant_sku

    if 'woodys' in constants.website_url: #implemented for woodys
        variant_url = variant_url
        pattern = r'(https://woodyseyewear\.com/)(\d+)-home_default(/.+)'
        match = re.match(pattern, variant_url)
        if match:
            base = match.group(1)
            number = int(match.group(2)) + 1
            rest = match.group(3)
            new_url = f"{base}{number}{rest}"
            variant_url = new_url

        variant_code = variant_color.replace('.', '')
        # variant_color = ""
        variant_color = variant_code

    if config.imbedded_variants_json_data:
        variant_color = variant_url['attributes']['attribute_pa_colore-montatura']
        variant_color = get_prod_color(variant_color, mappings.extended_color_names, translate=False)
        json_var_obj['$iProduct_SKU'] = variant_url['sku']
        variant_url = variant_url['image']['src']
        try:
            variant_lens_color = variant_url['attributes']['attribute_pa_colore-lenti']
            json_var_obj['$iLens_Color'] = translate_word(variant_lens_color, source_lang='italian', target_lang='english')
            print(variant_url['attributes']['attribute_pa_colore-lenti'])
        except:
            pass

    if config.request_variants_data:
        if config.variant_api_base_url:
            requests_data_value_list = []
            requests_data_value_list.append(variant_color)
            requests_data_value_list.append(variant_size)

            requests_data = config_variant_request(prod_item_num, requests_data_value_list, requests_data)
            response_status, json_data = request_website_api(
                session,
                constants.website_api_url,
                requests_data=requests_data)

            logging.info(f"variant api response_status: {response_status}")
            variant_url = json_data['fullImage']
            json_var_obj = get_prod_final_image(json_var_obj, variant_url, constants.website_url, constants.no_prod_img_url_key)
            json_var_obj['$iProduct_SKU'] = json_data['itemNumber']
            json_var_obj['suggested_price'] = json_data['suggestedPrice']
            json_var_obj['$iFrame_Retail'] = json_data['suggestedPrice']
            json_var_obj['$iProduct_Name'] = json_data['description']
            json_var_obj['sub_description'] = json_data['subDescription']

        in_page = visit_html_page(session, variant_url)
        variant_color = in_page.select_one(constants.variant_color_selector).get_text(strip=True).strip().lower()
        variant_code = in_page.select_one(constants.variant_color_code_selector).get_text(strip=True).strip().lower()
        variant_url = in_page.select_one(constants.variant_page_img_url_selector)
        variant_url = variant_url.get('href') or variant_url.get('src')
        json_var_obj['$iFrame_Code'] = variant_code.replace('.', '')

    if constants.variant_page_img_url_selector: # added these lines of code for offview need to review in_page
        variant_img_url_tags = in_page.select(constants.variant_page_img_url_selector)
        variant_url = get_quatre_img(variant_img_url_tags)

    if variant_url:
        # variant_url = normalize_url(constants.website_url, variant_url)
        json_var_obj = get_prod_final_image(json_var_obj, variant_url, constants.website_url, constants.no_prod_img_url_key)
    
    if variant_size:
        json_var_obj = get_frame_size(json_var_obj, variant_size, current_size=None)

    if not json_var_obj['$iFrame_Color'] or json_var_obj['$iFrame_Color'] == '':
        json_var_obj['$iFrame_Color'] = variant_color or '' 
    # json_var_obj['$iFrame_Code'] = variant_code.replace('.', '') or ''
    json_var_obj['$iFrame_Code'] = json_var_obj['$iModelURL'].split('/')[-1]

    return json_var_obj

def basic_product_details(in_page, json_prod_obj, prod_category):

    prod_name = in_page.select_one(constants.prod_name_selector)
    prod_item_num = prod_name
    if prod_name:
        json_prod_obj['$iProduct_Name'] = prod_name.get_text(strip=True)
        logging.info(f"Scraped {prod_name.get_text(strip=True)}")
    
    # if not constants.brand_name:
    #     brand_name = in_page.select_one(
    #             '.product-category-bc a'
    #             ).get_text(strip=True)
    # else:
    #     brand_name = constants.brand_name
    json_prod_obj['$iBrand'] = prod_category.strip()
    prod_category = prod_category.strip()
    if 'optical' or 'sun' in prod_category.lower():
        json_prod_obj['$iBrand'] = constants.website_name

    prod_price = in_page.select_one(constants.prod_price_selector)
    if prod_price:
        prod_price = prod_price.get_text(strip=True)
        json_prod_obj['org_Price'] = prod_price
        
        if is_currency_symbol(prod_price[-1]):
            currency_symbol = prod_price[-1]
            prod_price = prod_price[:-1].replace(',', '.').strip()
        elif is_currency_symbol(prod_price[0]):
            currency_symbol = prod_price[0]
            prod_price = prod_price[1:].replace(',', '.').strip()

        json_prod_obj['$iFrame_Retail'] = prod_price
        json_prod_obj['currency_symbol'] = currency_symbol

    prod_price = in_page.select_one(
        constants.prod_discounted_price_selector
        )
    if prod_price:
        prod_price = prod_price.get_text(strip=True)
        prod_price = prod_price[:-1].replace(',', '.').strip()
        json_prod_obj['iFrame_Retail_Discounted'] = prod_price

    # prod_price = in_page.select_one(constants.prod_price_selector)
    # if prod_price:
    #     prod_price = prod_price.get_text(strip=True)
    #     match = re.match(r"([^\d\s,.\-]+)?\s*([\d,\.]+)\s*([^\d\s,.\-]+)?", prod_price)
    #     if match:
    #         currency = (match.group(1) or match.group(3) or "").strip()
    #         price = match.group(2)
    #     json_prod_obj['$iFrame_Price'] = price
    #     json_prod_obj['currency_symbol'] = currency

    json_prod_obj = get_product_type(json_prod_obj, constants.website_name, prod_category)

    if 'woodys' in constants.website_url:
        # pattern = r'Material&quot;,&quot;value&quot;:&quot;(.*?)&quot;,&quot;id_feature'
        pattern = r'Material","value":"(.*?)","id_feature'
        match = re.search(pattern, in_page.prettify())
        if not match:
            pattern = r'Material&quot;,&quot;value&quot;:&quot;(.*?)&quot;,&quot;id_feature'
            match = re.search(pattern, in_page.prettify())

        if match:
            json_prod_obj["$iProduct_Material"] = match.group(1)
        pattern = r'"Gender","value":"(.*?)","id_feature'
        match = re.search(pattern, in_page.prettify())
        if not match:
            pattern = r'&quot;Gender&quot;,&quot;value&quot;:&quot;(.*?)&quot;,&quot;id_feature'
            match = re.search(pattern, in_page.prettify())
        if match:
            json_prod_obj["$iProduct_Gender"] = match.group(1)
    
    json_prod_obj["$iProduct_Gender"] = prod_category # added for offview

    return json_prod_obj, prod_item_num


def get_product_details(session, in_page, in_product_url, master_json, prod_category): 
    from lxml import etree

    json_prod_obj = config.base_json_format[0].copy()
    if master_json[0]['$iProduct_Name'] == '':
        master_json = []

    json_prod_obj['updated_ts'] = get_current_time_iso()
    json_prod_obj['$iModelURL'] = in_product_url

    json_prod_obj, prod_item_num = basic_product_details(in_page, json_prod_obj, prod_category)
    logging.info(f"Scraped {in_product_url}")
    
    prod_all_specs = in_page.select(constants.prod_all_specs_selector)
    json_prod_obj = extract_specs_using_map_keywords(json_prod_obj, prod_all_specs, mappings.website_keyword_to_json_mapping, mappings.shapes)
    print(json_prod_obj)
    # return

    # variant_url_tags = in_page.select(constants.variant_urls_selector)
    tree = etree.HTML(in_page.prettify())
    variant_url_tags = tree.xpath(constants.variant_urls_selector)
    prod_variant_colors = in_page.select(constants.all_variant_colors_selector)
    prod_variant_sizes = in_page.select(constants.all_variant_sizes_selector)

    if config.imbedded_variants_json_data:
        variant_url_tags = json.loads(variant_url_tags[0])

    variant_info_tags_map = map_variants_info_tags(variant_url_tags, prod_variant_colors)
    print(list(variant_info_tags_map))

    logging.info("Getting variants data......")
    for variant_color_tag, variant_url_tag in variant_info_tags_map:
        # prod_variant_sizes = prod_variant_sizes if prod_variant_sizes is not None else [None] # this will allow to loop through prod_variant_sizes once even if it is None
        prod_variant_sizes = prod_variant_sizes if prod_variant_sizes else [None] # this will allow to loop through prod_variant_sizes once even if it is empty list
        for prod_size_tag in prod_variant_sizes:
            json_variant_obj = json_prod_obj.copy()
            json_variant_obj = get_variants(
                in_page,
                json_variant_obj,
                session,
                prod_item_num,
                variant_color_tag,
                prod_size_tag,
                variant_url_tag)

            master_json.append(json_variant_obj)

    return master_json

def start():
    in_master_json_file_path, all_scraper_run_details = setup_folder(constants.website_name, config.data_dir_path)
    setup_logging()
    master_json = initialize_master_json(in_master_json_file_path, config.base_json_format)
    session = requests.Session()

    context = None
    if config.login_url:
        # playwright, browser, context, in_page = initialize_browser(constants.website_url, headless=False, localhost=False)
        playwright, browser, context, in_page = initialize_browser(constants.website_url, headless=False, localhost=True)
    # if config.login_url:
    #     logging.info('Logging in to the website.....')
        in_page, session = browser_login_to_website(in_page, session)
    #     logging.info(f"Login successful")
    #     logging.info(f"Cookies: { session.cookies}")

    # return
    delay(2000)
    # if config.login_url:
    #     in_page = visit_browser_page(context, constants.website_url)
    # else:
    # resp_status_code, in_page = visit_html_page(session, config.website_prod_store_url, config.headers)
    # logging.info(f"Categories page resp: {resp_status_code}")
    # categories_dict = get_categories(in_page)
    categories_dict = {'optical_woman': 'https://offview.com/en-uk/collections/optical-woman', 'optical_men': 'https://offview.com/en-uk/collections/optical-men', 'optical_unisex': 'https://offview.com/en-uk/collections/optical-unisex',
                       'sun_woman': 'https://offview.com/en-uk/collections/sun-woman', 'sun_men': 'https://offview.com/en-uk/collections/sun-man', 'sun_unisex': 'https://offview.com/en-uk/collections/sun-unisex'}
    # categories_dict = {'sun_woman': 'https://offview.com/en-uk/collections/sun-woman'}
    logging.info(f'Categories dict: {categories_dict}')
    in_myproduct_urls_dict, total_products = get_categories_prod_url(session, context, categories_dict)
    logging.info(f"in_myproduct_urls_dict: {in_myproduct_urls_dict}")
    logging.info(f"Total product url {total_products}")

    for prod_category, in_myproduct_urls in in_myproduct_urls_dict.items():
        # for prod_sub_category, in_myproduct_urls in prod_sub_category_dict.items():
        try:
            logging.info(f"Scraping {prod_category}.....")
            in_myproduct_urls = in_myproduct_urls if in_myproduct_urls else [None]
            for in_product_url in in_myproduct_urls:
                in_product_url = urllib.parse.unquote(in_product_url)
                logging.info(f'in_product_url: {in_product_url}')
                if exists_in_master_json(master_json, in_product_url):
                    logging.info('Frame already exists in master json')
                    continue
                try:
                    resp_status_code, in_page = visit_html_page(session, in_product_url, config.headers)
                except requests.exceptions.ConnectionError:
                    logging.error(f'Got error requesting data:', exc_info=True)
                    logging.info('Creating new session....')
                    session = requests.Session()
                    resp_status_code, in_page = visit_html_page(session, in_product_url, config.headers)
                try:
                    master_json = get_product_details(session, in_page, in_product_url, master_json, prod_category)
                except:
                    logging.error(f'Got error in product details:', exc_info=True)
                logging.info('saving file....')
                with open(in_master_json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(master_json, file, indent=4, ensure_ascii=False)

                milliseconds = randint(2, 5) * 1000
                delay(milliseconds)
        except:
            logging.error(f'Error:', exc_info=True)

    if context:
        playwright.stop()
    current_run_detail = scraper_run_details(all_scraper_run_details, total_products, master_json)
    print(current_run_detail)

if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        logging.error(f'Error: {str(e)}', exc_info=True)
    logging.shutdown()