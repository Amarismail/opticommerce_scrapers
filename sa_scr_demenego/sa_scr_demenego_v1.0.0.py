from utils.utils import (
    initialize_master_json,
    exists_in_master_json,
    delay,
    get_current_time_iso,
    setup_folder,
    normalize_url,
    translate_word)
from utils.scraper_utils import (
    visit_html_page, 
    request_website_api, 
    check_image_url,
    get_prod_color, 
    get_frame_size, 
    clean_up_shape,
    get_product_type,
    is_currency_symbol)
from utils.logging_utils import setup_logging
from random import randint
import requests
import urllib.parse
import config
import json
import logging
import constants
import mappings

def config_variant_request(prod_item_num, requests_data_value_list):
    requests_data = config.requests_data
    requests_data['styleItemNumber'] = prod_item_num
    requests_data['styleVariantList'] = json.dumps(requests_data_value_list, separators=(',', ':'))
    return requests_data

def config_store_page_request(category_name, category_link, page_num):

    if config.prod_store_api_base_url:
            category_link = config.prod_store_api_base_url

    if config.params:
        params = config.params
        params[list(params.keys())[0]] = str(page_num)
        if config.categories_id_map:
            for key, value in config.categories_id_map.items():
                if key == category_name.lower():
                    for key, value in value.items():
                        params[key] = value

        return category_link, params
    
    # added this for https://www.demenego.it/
    if not config.params and config.website_prod_store_url_navigation:
        category_link = config.prod_store_api_base_url + str(page_num)

    return category_link, None

def get_categories(in_page):
    categories = {}
    categories_tags = in_page.select(constants.categories_selector)
    for categories_tag in categories_tags:
        category_link = constants.website_url
        if categories_tag.has_attr('href'):
            category_link = category_link + categories_tag['href']
        category_text = categories_tag.text.strip()
        categories[category_text] = category_link

    return categories

def get_categories_prod_url(session, categories_dict):
    total_products = 0
    in_myproduct_urls_dict = {}
    logging.info(categories_dict)
    for category_name, category_link in categories_dict.items():
        logging.info(f'scraping category: {category_name}....')
        logging.info(f'scraping category: {category_link}....')
        in_myproduct_urls = get_prod_urls(
            session,
            category_name,
            category_link,
            in_myproduct_urls = [],
            )
        
        in_myproduct_urls = list(set(in_myproduct_urls))
        in_myproduct_urls_dict[category_name] = in_myproduct_urls
        total_products = total_products + len(in_myproduct_urls)
    
    return in_myproduct_urls_dict, total_products

def get_prod_urls(session, category_name, category_link, in_myproduct_urls, page_num = 1):
    
    category_prod_page_link, params = config_store_page_request(category_name, category_link, page_num)
    resp_status_code, in_page = visit_html_page(session, category_prod_page_link, config.headers, params=params)
    logging.info(f'response status: {resp_status_code}')

    prod_url_tags = in_page.select(constants.prod_link_selector)
    if not prod_url_tags:
        return in_myproduct_urls
    
    for prod_url_tag in prod_url_tags:
        prod_url = prod_url_tag.get('href')
        prod_normalize_url = prod_url
        prod_normalize_url = normalize_url(constants.website_url, prod_url, include_query=False)
        if prod_normalize_url:
            in_myproduct_urls.append(prod_normalize_url)

    if not config.website_prod_store_url_navigation:
        return in_myproduct_urls

    milliseconds = randint(1, 3) * 1000
    delay(milliseconds)

    page_num = page_num + 1
    # if page_num >= 3:
    #     return in_myproduct_urls
    in_myproduct_urls = get_prod_urls(session, category_name, category_link, in_myproduct_urls,  page_num)

    return in_myproduct_urls

def get_prod_final_image(json_obj, variant_img_url):
    from urllib.parse import urlparse, urlunparse

    if not variant_img_url or variant_img_url == "" or constants.no_prod_img_url_key.lower() in variant_img_url:
        return json_obj

    # variant_img_url = urlunparse(urlparse(variant_img_url)._replace(query=""))
    if config.website_img_base_url not in variant_img_url:
        variant_img_url = config.website_img_base_url + variant_img_url

    variant_img_url = normalize_url(constants.website_url, variant_img_url)
    check = check_image_url(variant_img_url)
    if not check:
        return json_obj

    json_obj['$iFrame_IMAGE'] = variant_img_url
    json_obj['$iFrame_IMG_Mark'] = "1"

    return json_obj

def map_website_keywords_to_json(json_obj, prod_all_specs):
    key_mapping = mappings.website_keyword_to_json_mapping
    splitters = [':', '\n']
    spec_key = None
    for spec in prod_all_specs:
        spec = spec.text.strip()
        # print('-----------------------')
        # print(spec)
        # implemented ':' for eyeqeyewear.com and '\n' for dunelmoptical.com
        # used .text to keep all the sting special cheaters like \n
        for splitter in splitters:
            # below lineRemove extra blank lines by replacing multiple newlines with a single newline
            cleaned_spec = "\n".join(filter(None, spec.split("\n")))
            if splitter in cleaned_spec:
                spec_key = cleaned_spec.split(splitter)[0].strip().lower()
                spec_value = cleaned_spec.split(splitter)[1].strip().lower()

        if spec_key in key_mapping.keys():
            json_obj_key = key_mapping[spec_key]
            json_obj[json_obj_key] = spec_value.replace(' mm', '')

            if json_obj_key == '$iProduct_Shape':
                clean_prod_shape = clean_up_shape(spec_value, mappings.shapes)
                json_obj[json_obj_key] = clean_prod_shape
            
        if not spec_key:
            get_product_type(json_obj, keyword=spec)

    return json_obj

def map_variants_info_tags(variant_url_tags, prod_variant_colors):
    from itertools import zip_longest

    if len(variant_url_tags) == len(prod_variant_colors):
        variant_info_tags_map = zip(prod_variant_colors, variant_url_tags)
        return variant_info_tags_map

    if not variant_url_tags or not prod_variant_colors:
        variant_info_tags_map = list(zip_longest(prod_variant_colors, variant_url_tags))
        return variant_info_tags_map

    img_url_map = {img_tag.get('href').lower(): img_tag for img_tag in variant_url_tags}
    variant_info_tags_map = [
    (color_tag, next((img_url_map[url] for url in img_url_map.keys() if color_tag.get_text(strip=True).lower() in url), None))
    for color_tag in prod_variant_colors
]
    return variant_info_tags_map

def get_variants(json_var_obj, session, prod_item_num, prod_color_tag, prod_size_tag, variant_url_tag):

    variant_color = prod_color_tag.get_text(strip=True).strip() if prod_color_tag else None
    variant_size = prod_size_tag.get_text(strip=True).strip() if prod_size_tag else None
    # variant_url = variant_url_tag.get('data-zoomimg') or variant_url_tag.get('href') or variant_url_tag.get('src')
    variant_url = variant_url_tag

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

            requests_data = config_variant_request(prod_item_num, requests_data_value_list)
            response_status, json_data = request_website_api(
                session,
                constants.website_api_url,
                requests_data=requests_data)

            logging.info(f"variant api response_status: {response_status}")
            variant_url = json_data['fullImage']
            json_var_obj = get_prod_final_image(json_var_obj, variant_url)
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
        json_var_obj['$iFrame_Code'] = variant_code

    if variant_url:
        # variant_url = normalize_url(constants.website_url, variant_url)
        json_var_obj = get_prod_final_image(json_var_obj, variant_url)
    
    if variant_size:
        json_var_obj = get_frame_size(json_var_obj, variant_size, current_size=None)
    json_var_obj['$iFrame_Color'] = variant_color or '' 

    return json_var_obj

def basic_product_details(in_page, json_prod_obj):

    import re

    prod_item_num = in_page.select_one(
        constants.prod_name_selector
        ).get_text(strip=True)
    json_prod_obj['product_item_num'] = prod_item_num
    prod_price = in_page.select_one(
        constants.prod_price_selector
        ).get_text(strip=True)
    json_prod_obj['org_Price'] = prod_price
    
    # prod_price = in_page.select_one(constants.prod_price_selector)
    # if prod_price:
    #     prod_price = prod_price.get_text(strip=True)
    #     match = re.match(r"([^\d\s,.\-]+)?\s*([\d,\.]+)\s*([^\d\s,.\-]+)?", prod_price)
    #     if match:
    #         currency = (match.group(1) or match.group(3) or "").strip()
    #         price = match.group(2)
    #     json_prod_obj['$iFrame_Price'] = price
    #     json_prod_obj['currency_symbol'] = currency

    if is_currency_symbol(prod_price[-1]):
        currency_symbol = prod_price[-1]
        prod_price = prod_price[:-1].replace(',', '.').strip()

    json_prod_obj['$iFrame_Retail'] = prod_price
    json_prod_obj['currency_symbol'] = currency_symbol

    prod_price = in_page.select_one(
        constants.prod_discounted_price_selector
        ).get_text(strip=True)
    prod_price = prod_price[:-1].replace(',', '.').strip()
    json_prod_obj['iFrame_Retail_Discounted'] = prod_price

    prod_name = in_page.select_one(constants.prod_name_selector).get_text(strip=True)
    if not constants.brand_name:
        brand_name = in_page.select_one(
                '.product-category-bc a'
                ).get_text(strip=True)
    else:
        brand_name = constants.brand_name
    logging.info(f"Scraped {prod_name}")

    json_prod_obj['$iProduct_Name'] = prod_item_num
    json_prod_obj['$iBrand'] = brand_name

    return json_prod_obj, prod_item_num

def get_product_details(session, in_page, in_product_url, master_json, prod_category): 
    from lxml import etree

    json_prod_obj = config.base_json_format[0].copy()
    if master_json[0]['$iProduct_Name'] == '':
        master_json = []

    json_prod_obj['updated_ts'] = get_current_time_iso()
    json_prod_obj['$iModelURL'] = in_product_url
    json_prod_obj, prod_item_num = basic_product_details(in_page, json_prod_obj)
    logging.info(f"Scraped {in_product_url}")
    
    prod_all_specs = in_page.select(constants.prod_all_specs_selector)
    json_prod_obj = map_website_keywords_to_json(json_prod_obj, prod_all_specs)
    # json_prod_obj = get_product_type(json_prod_obj, brand_name, prod_category)

    # variant_url_tags = in_page.select(constants.variant_urls_selector)
    tree = etree.HTML(in_page.prettify())
    variant_url_tags = tree.xpath(constants.variant_urls_selector)
    prod_variant_colors = in_page.select(constants.all_variant_colors_selector)
    prod_variant_sizes = in_page.select(constants.all_variant_sizes_selector)

    if config.imbedded_variants_json_data:
        variant_url_tags = json.loads(variant_url_tags[0])

    variant_info_tags_map = map_variants_info_tags(variant_url_tags, prod_variant_colors)

    logging.info("Getting variants data......")
    for variant_color_tag, variant_url_tag in variant_info_tags_map:
        # prod_variant_sizes = prod_variant_sizes if prod_variant_sizes is not None else [None] # this will allow to loop through prod_variant_sizes once even if it is None
        prod_variant_sizes = prod_variant_sizes if prod_variant_sizes else [None] # this will allow to loop through prod_variant_sizes once even if it is empty list
        for prod_size_tag in prod_variant_sizes:
            json_variant_obj = json_prod_obj.copy()
            json_variant_obj = get_variants(
                json_variant_obj,
                session,
                prod_item_num,
                variant_color_tag,
                prod_size_tag,
                variant_url_tag)

            master_json.append(json_variant_obj)

    return master_json

def start():
    in_master_json_filename = config.in_master_json_filename.lower().replace(" ", '_')
    in_master_json_file_path, logging_file_path = setup_folder(in_master_json_filename)
    setup_logging()
    master_json = initialize_master_json(in_master_json_file_path, config.base_json_format)
    session = requests.Session()

    resp_status_code, in_page = visit_html_page(session, config.website_prod_store_url, config.headers)
    logging.info(f"Categories page resp: {resp_status_code}")
    categories_dict = get_categories(in_page)
    print(categories_dict)
    in_myproduct_urls_dict, total_products = get_categories_prod_url(session, categories_dict)
    logging.info(f"{in_myproduct_urls_dict}")
    logging.info(f"Total product url {total_products}")

    for prod_category, in_myproduct_urls in in_myproduct_urls_dict.items():
        try:
            logging.info(f"Scraping {prod_category} .....")
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

if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        logging.error(f'Error: {str(e)}', exc_info=True)
    logging.shutdown()