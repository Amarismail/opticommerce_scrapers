from utils.utils import (
    initialize_master_json,
    exists_in_master_json,
    delay,
    get_current_time_iso,
    setup_folder,
    normalize_url)
from utils.scraper_utils import (
    visit_html_page, 
    request_website_api, 
    check_image_url, 
    get_frame_size, 
    clean_up_shape)
from utils.logging_utils import setup_logging
from bs4 import BeautifulSoup
from random import randint
import requests
import urllib.parse
import config
import json
import logging
import constants
import mappings

def get_categories(in_page):
    categories = {}
    categories_tags = in_page.select(constants.categories_selector)
    for categories_tag in categories_tags:
        category_link = constants.website_url + categories_tag['href']
        category_text = categories_tag.text.strip()
        categories[category_text] = category_link

    return categories

def get_catagories_prod_url(session, categories_dict):
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

    config.params[list(config.params.keys())[0]] = str(page_num)
    if config.catagories_id_map:
        config.params['coll'] = config.catagories_id_map[category_name.lower()]
    if config.prod_store_api_base_url:
        category_link = config.prod_store_api_base_url
    category_prod_page_link = category_link
    resp_status_code, in_page = visit_html_page(session, category_prod_page_link, config.headers, params=config.params)
    logging.info(f'response status: {resp_status_code}')

    prod_url_tags = in_page.select(constants.prod_link_selector)
    if not prod_url_tags:
        return in_myproduct_urls
    for prod_url_tag in prod_url_tags:
        prod_url = prod_url_tag.get('href')
        prod_normalize_url = prod_url
        prod_normalize_url = normalize_url(constants.website_url, prod_url)
        if prod_normalize_url:
            in_myproduct_urls.append(prod_normalize_url)

    if not config.website_prod_store_url_navigation:
        return in_myproduct_urls

    milliseconds = randint(1, 3) * 1000
    delay(milliseconds)

    page_num = page_num + 1
    in_myproduct_urls = get_prod_urls(session, category_name, category_link, in_myproduct_urls,  page_num)

    return in_myproduct_urls

def config_request_params(prod_item_num, requests_data_value_list):
    requests_data = config.requests_data
    requests_data['styleItemNumber'] = prod_item_num
    requests_data['styleVariantList'] = json.dumps(requests_data_value_list, separators=(',', ':'))
    return requests_data

def get_prod_final_image(json_obj, variant_img_url):
    from urllib.parse import urlparse, urlunparse

    if not variant_img_url or variant_img_url == "" or constants.no_prod_img_url_key.lower() in variant_img_url:
        return json_obj

    # variant_img_url = urlunparse(urlparse(variant_img_url)._replace(query=""))
    if constants.website_img_base_url not in variant_img_url:
        variant_img_url = constants.website_img_base_url + variant_img_url
    variant_img_url = normalize_url(constants.website_url, variant_img_url)
    check = check_image_url(variant_img_url)
    if not check:
        return json_obj

    json_obj['$iFrame_IMAGE'] = variant_img_url
    json_obj['$iFrame_IMG_Mark'] = "1"

    return json_obj

def get_product_type(json_prod_object, prod_name, prod_category, prod_material=None):

    if prod_material:
        json_prod_object['$iProduct_Material'] = prod_material

    for prod_type_key, keyword_to_update in mappings.prod_types.items():
        if prod_type_key in prod_category.lower() or prod_type_key in prod_name.lower():
            json_prod_object['$iProduct_Type'] = keyword_to_update
            break

    return json_prod_object

def map_website_keywords_to_json(json_obj, prod_all_specs):
    key_mapping = mappings.website_keyword_to_json_mapping
    for spec in prod_all_specs:
        if ':' in spec.get_text(strip=True):
            spec_key = spec.get_text(strip=True).split(':')[0].lower()
            spec_value = spec.get_text(strip=True).split(':')[1].lower()
        else:
            spec_key = spec.select_one('.specs--label').get_text(strip=True).lower()
            spec_value = spec.select_one('.specs--value').get_text(strip=True)
        
        if spec_key in key_mapping.keys():
            json_obj_key = key_mapping[spec_key]
            json_obj[json_obj_key] = spec_value.replace(' mm', '')

            if json_obj_key == '$iProduct_Shape':
                clean_prod_shape = clean_up_shape(spec_value, mappings.shapes)
                json_obj[json_obj_key] = clean_prod_shape

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

def get_temple_fold_img(in_page):
    variant_img_urls = in_page.select(constants.variant_page_img_url_selector)
    variant_url = variant_img_urls[0]['src']
    if len(variant_img_urls) > 1:
        # variant_url = (variant_img_url for variant_img_url in variant_img_urls if 'TF' in variant_img_url)
        variant_url = next((tag['src'] for tag in variant_img_urls if 'TF' in tag.get('src', '')),  variant_url)

    return variant_url


def get_variants(in_page, json_variant_obj, session, prod_item_num, prod_color_tag, prod_size_tag, variant_url_tag):

    variant_color = prod_color_tag.get_text(strip=True).strip() if prod_color_tag else None
    variant_size = prod_size_tag.get_text(strip=True).strip() if prod_size_tag else None
    variant_url = variant_url_tag.get('href') or variant_url_tag.get('src')

    if config.request_variants_data:
        if config.variant_api_base_url:
            requests_data_value_list = []
            requests_data_value_list.append(variant_color)
            requests_data_value_list.append(variant_size)

            requests_data = config_request_params(prod_item_num, requests_data_value_list)
            response_status, json_data = request_website_api(
                session,
                constants.website_api_url,
                requests_data=requests_data)

            logging.info(f"variant api response_status: {response_status}")
            variant_url = json_data['fullImage']
            json_variant_obj = get_prod_final_image(json_variant_obj, variant_url)
            json_variant_obj['$iProduct_SKU'] = json_data['itemNumber']
            json_variant_obj['suggested_price'] = json_data['suggestedPrice']
            json_variant_obj['$iFrame_Retail'] = json_data['suggestedPrice']
            json_variant_obj['$iProduct_Name'] = json_data['description']
            json_variant_obj['sub_description'] = json_data['subDescription']

        in_page = visit_html_page(session, variant_url)
        variant_color = in_page.select_one(constants.variant_color_selector).get_text(strip=True).strip().lower()
        variant_code = in_page.select_one(constants.variant_color_code_selector).get_text(strip=True).strip().lower()
        variant_url = in_page.select_one(constants.variant_page_img_url_selector)
        variant_url = variant_url.get('href') or variant_url.get('src')
        json_variant_obj['$iFrame_Code'] = variant_code

    if variant_url:
        if constants.variant_page_img_url_selector:
            variant_url = get_temple_fold_img(in_page)
        # variant_url = normalize_url(constants.website_url, variant_url)
        json_variant_obj = get_prod_final_image(json_variant_obj, variant_url)
        
    json_variant_obj = get_frame_size(json_variant_obj, variant_size, current_size=None)
    json_variant_obj['$iFrame_Color'] = variant_color or '' 
    # json_variant_obj['$iFrame_Code'] = variant_code

    return json_variant_obj

def get_product_details(session, in_page, in_product_url, master_json, prod_category): 

    json_prod_object = config.base_json_format[0].copy()
    if master_json[0]['$iProduct_Name'] == '':
        master_json = []

    json_prod_object['updated_ts'] = get_current_time_iso()
    json_prod_object['$iModelURL'] = in_product_url
    
    prod_item_num = in_page.select_one(
        constants.prod_name_selector
        ).get_text(strip=True)
    json_prod_object['product_item_num'] = prod_item_num

    prod_name = in_page.select_one(constants.prod_name_selector).get_text(strip=True)
    if not config.brand_name:
        brand_name = in_page.select_one(
                '.product-category-bc a'
                ).get_text(strip=True)
    else:
        brand_name = config.brand_name
    logging.info(f"Scraped {prod_name}")
    logging.info(f"Scraped {in_product_url}")

    prod_all_specs = in_page.select(constants.prod_all_specs_selector)
    json_prod_object = map_website_keywords_to_json(json_prod_object, prod_all_specs)
    # json_prod_object = get_product_type(json_prod_object, brand_name, prod_category)
    
    json_prod_object['$iProduct_Name'] = prod_item_num
    json_prod_object['$iBrand'] = brand_name

    variant_url_tags = in_page.select(constants.variant_urls_selector)
    variant_url_tags = variant_url_tags[:1]
    prod_variant_colors = in_page.select(constants.main_variant_colors_selector)
    prod_variant_sizes = in_page.select(constants.main_variant_sizes_selector)
    variant_info_tags_map = map_variants_info_tags(variant_url_tags, prod_variant_colors)

    logging.info("Getting variants data......")
    for variant_color_tag, variant_url_tag in variant_info_tags_map:
        # prod_variant_sizes = prod_variant_sizes if prod_variant_sizes is not None else [None] # this will allow to loop through prod_variant_sizes once even if it is None
        prod_variant_sizes = prod_variant_sizes if prod_variant_sizes else [None] # this will allow to loop through prod_variant_sizes once even if it is empty list
        for prod_size_tag in prod_variant_sizes:
            json_variant_obj = json_prod_object.copy()
            json_variant_obj = get_variants(
                in_page,
                json_variant_obj,
                session,
                prod_item_num,
                variant_color_tag,
                prod_size_tag,
                variant_url_tag)

            master_json.append(json_variant_obj)
    # logging.info(master_json)
    return master_json

def start():
    in_master_json_filename = config.in_master_json_filename.lower().replace(" ", '')
    in_master_json_file_path, logging_file_path = setup_folder(in_master_json_filename)
    setup_logging()
    master_json = initialize_master_json(in_master_json_file_path, config.base_json_format)
    session = requests.Session()

    resp_status_code, in_page = visit_html_page(session, config.website_prod_store_url, config.headers)
    logging.info(f"Catagories page resp: {resp_status_code}")
    categories_dict = get_categories(in_page)
    in_myproduct_urls_dict, total_products = get_catagories_prod_url(session, categories_dict)
    logging.info(f"{in_myproduct_urls_dict}")
    logging.info(f"Total product url {total_products}")

    for prod_category, in_myproduct_urls in in_myproduct_urls_dict.items():
        try:
            logging.info(f"Scraping {prod_category} .....")
            in_myproduct_urls = in_myproduct_urls if in_myproduct_urls else [None]
            for in_product_url in in_myproduct_urls:
                in_product_url = urllib.parse.unquote(in_product_url)
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
                    json.dump(master_json, file, indent=4)

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