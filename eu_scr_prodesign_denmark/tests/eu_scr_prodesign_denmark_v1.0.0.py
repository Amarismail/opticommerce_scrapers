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
    get_lens_size, 
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
        in_myproduct_urls = get_prod_urls(
            session,
            category_name,
            category_link,
            in_myproduct_urls = [],
            )
        
        in_myproduct_urls = list(set(in_myproduct_urls))
        in_myproduct_urls_dict[category_name] = in_myproduct_urls
        total_products = total_products + len(in_myproduct_urls)
        print(len(in_myproduct_urls))
    
    return in_myproduct_urls_dict, total_products

def get_prod_urls(session, category_name, category_link, in_myproduct_urls,   page_num = 1):

    config.params['Page'] = str(page_num)
    config.params['CategoryId'] = config.catagories_id_map[category_name.lower()]
    if config.prod_store_api_base_url:
        category_link = config.prod_store_api_base_url
    # category_prod_page_link = category_link + config.prod_page_url_params
    category_prod_page_link = category_link
    response = session.get(
        category_prod_page_link,
        params=config.params,
        headers=config.headers)

    logging.info(f'response status: {response.status_code}')

    soup = BeautifulSoup(response.text, "html.parser")
    in_page = soup
    
    prod_url_tags = in_page.select(constants.prod_link_selector)
    if not prod_url_tags:
        return in_myproduct_urls
    for prod_url_tag in prod_url_tags:
        prod_url = prod_url_tag.get('href')
        prod_normalize_url = prod_url
        prod_normalize_url = normalize_url(constants.website_url, prod_url)
        if prod_normalize_url:
            in_myproduct_urls.append(prod_normalize_url)

    milliseconds = randint(1, 3) * 1000
    delay(milliseconds)

    page_num = page_num + 1
    # if page_num >= 3:
    #     return in_myproduct_urls
    in_myproduct_urls = get_prod_urls(session, category_name, category_link, in_myproduct_urls,  page_num)

    return in_myproduct_urls

def config_request_params(prod_item_num, requests_data_value_list):
    requests_data = config.requests_data
    requests_data['styleItemNumber'] = prod_item_num
    requests_data['styleVariantList'] = json.dumps(requests_data_value_list, separators=(',', ':'))
    return requests_data

def get_prod_final_image(json_obj, variant_img_url):
    if variant_img_url == "" or constants.no_prod_img_url_key.lower() in variant_img_url:
        json_obj['$iFrame_IMAGE'] = ""
        json_obj['$iFrame_IMG_Mark'] = "0"

        return json_obj

    if constants.website_img_base_url not in variant_img_url:
        variant_img_url = constants.website_img_base_url + variant_img_url
    variant_img_url = normalize_url(constants.website_url, variant_img_url)
    check = check_image_url(variant_img_url)
    if not check:
        json_obj['$iFrame_IMAGE'] = ""
        json_obj['$iFrame_IMG_Mark'] = "0"

        return json_obj

    json_obj['$iFrame_IMAGE'] = variant_img_url
    json_obj['$iFrame_IMG_Mark'] = "1"

    return json_obj

def get_variants(json_variant_obj, session, prod_item_num, prod_color_tag, prod_size_tag, variant_img_url):

    variant_color = prod_color_tag.get_text(strip=True)
    variant_size = prod_size_tag.get_text(strip=True)

    if config.request_variants_data:
        requests_data_value_list = []
        variant_color_value = prod_color_tag.strip()
        requests_data_value_list.append(variant_color_value)
        variant_size_value = prod_size_tag.strip()
        requests_data_value_list.append(variant_size_value)

        requests_data = config_request_params(prod_item_num, requests_data_value_list)
        response_status, json_data = request_website_api(
            session,
            constants.website_api_url,
            requests_data=requests_data)

        logging.info(f"variant api response_status: {response_status}")
        variant_img_url = json_data['fullImage']
        json_variant_obj = get_prod_final_image(json_variant_obj, variant_img_url)
        json_variant_obj['$iProduct_SKU'] = json_data['itemNumber']
        json_variant_obj['suggested_price'] = json_data['suggestedPrice']
        json_variant_obj['$iFrame_Retail'] = json_data['suggestedPrice']
        json_variant_obj['$iProduct_Name'] = json_data['description']
        json_variant_obj['sub_description'] = json_data['subDescription']
    else:
        if variant_img_url:
            variant_img_url = variant_img_url.get('href')
            json_variant_obj = get_prod_final_image(json_variant_obj, variant_img_url)
        
    json_variant_obj = get_lens_size(json_variant_obj, variant_size, current_size=None)
    json_variant_obj['$iProduct_Type'] = variant_color

    return json_variant_obj

def get_product_type(json_prod_object, prod_name, prod_category, prod_material=None):

    if prod_material:
        json_prod_object['$iProduct_Material'] = prod_material

    for prod_type_key, keyword_to_update in constants.prod_types.items():
        if prod_type_key in prod_category.lower() or prod_type_key in prod_name.lower():
            json_prod_object['$iProduct_Type'] = keyword_to_update
            break

    return json_prod_object

def map_website_keywords_to_json(json_obj, prod_all_specs):
    key_mapping = mappings.website_keyword_to_json_mapping
    for spec in prod_all_specs:
        spec_key = spec.get_text(strip=True).split(':')[0].lower()
        spec_value = spec.get_text(strip=True).split(':')[1].lower()
        if spec_key in key_mapping.keys():
            json_obj_key = key_mapping[spec_key]
            json_obj[json_obj_key] = spec_value

            if json_obj_key == '$iProduct_Shape':
                clean_prod_shape = clean_up_shape(spec_value, mappings.shapes)
                json_obj[json_obj_key] = clean_prod_shape

    return json_obj

def map_variants_with_images(variant_img_urls, prod_variant_colors):
    if len(variant_img_urls) == len(prod_variant_colors):
        variant_img_color_map = zip(prod_variant_colors, variant_img_urls)
    else:
        img_url_map = {img_tag.get('href').lower(): img_tag for img_tag in variant_img_urls}
        variant_img_color_map = [
        (color_tag, next((img_url_map[url] for url in img_url_map.keys() if color_tag.get_text(strip=True).lower() in url), None))
        for color_tag in prod_variant_colors
    ]

    return variant_img_color_map

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

    prod_all_specs = in_page.select(
        "specs__container"
        )
    json_prod_object = map_website_keywords_to_json(json_prod_object, prod_all_specs)
    json_prod_object = get_product_type(json_prod_object, brand_name, prod_category)
    
    json_prod_object['$iProduct_Name'] = prod_item_num
    json_prod_object['$iBrand'] = brand_name
    variant_img_tag = in_page.select(
        constants.variant_img_url_selector
    )

    prod_variant_colors = in_page.select(
    '#pa_color option:not(:first-child)'
    )
    prod_variant_sizes = in_page.select(
    '#pa_size option:not(:first-child)'
    )
    variant_img_color_map = map_variants_with_images(variant_img_urls, prod_variant_colors)
    print(variant_img_color_map)

    logging.info("Getting variants data......")
    for variant_color_tag, variant_img_tag in variant_img_color_map:
        for prod_size_tag in prod_variant_sizes:
            json_variant_obj = json_prod_object.copy()
            json_variant_obj = get_variants(
                json_variant_obj,
                session,
                prod_item_num,
                variant_color_tag,
                prod_size_tag,
                variant_img_tag)

            master_json.append(json_variant_obj)
    logging.info(master_json)
    return master_json

def start():
    in_master_json_file_path, logging_file_path = setup_folder(config.in_master_json_filename)
    setup_logging()
    master_json = initialize_master_json(in_master_json_file_path, config.base_json_format)
    session = requests.Session()

    in_page = visit_html_page(session, config.website_prod_store_url)
    categories_dict = get_categories(in_page)
    in_myproduct_urls_dict, total_products = get_catagories_prod_url(session, categories_dict)
    logging.info(f"{in_myproduct_urls_dict}")
    logging.info(f"Total product url {total_products}")

    for prod_category, in_myproduct_urls in in_myproduct_urls_dict.items():
        try:
            logging.info(f"Scraping {prod_category} .....")
            for in_product_url in in_myproduct_urls:
                in_product_url = urllib.parse.unquote(in_product_url)
                if exists_in_master_json(master_json, in_product_url):
                    logging.info('Frame already exists in master json')
                    continue
                try:
                    in_page = visit_html_page(session, in_product_url)
                except requests.exceptions.ConnectionError:
                    logging.error(f'Got error requesting data:', exc_info=True)
                    logging.info('Creating new session....')
                    session = requests.Session()
                    in_page = visit_html_page(session, in_product_url)
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