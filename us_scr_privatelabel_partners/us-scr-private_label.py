from utils.utils import (
    initialize_master_json,
    initialize_browser,
    delay,
    current_utc_ts_iso,
    exists_in_master_json,
    setup_folder,
    )
from utils.scraper_utils import scraper_run_details
from utils.logging_utils import setup_logging
from playwright.sync_api import sync_playwright
from random import randint
import constants
import config
import json
import re
import logging

def get_collections_urls(in_page):
    collections_link_tags = in_page.query_selector_all(
        'ul.nav.navbar-nav.nav-main > li:nth-child(1) ul.dropdown-menu.multi-level.collection-menu > li:not(:last-child) > a'
        )
    collection_urls = [tag.get_attribute('href') for tag in collections_link_tags]
    return collection_urls

def get_prod_urls(in_page, collection_urls):

    total_products = 0
    in_myproduct_urls_dict = {}
    for collection_url in collection_urls:
        in_page.goto(collection_url)
        prod_group_title_tags = in_page.query_selector_all(
            "h3.collection-product-group-title"
            )
        prod_group_divs = in_page.query_selector_all(
            ".row.collection-product-grid"
            )
        
        for prod_group_title, prod_group_div in zip(prod_group_title_tags, prod_group_divs):
            in_myproduct_urls = []
            prod_group_title = prod_group_title.text_content().strip()

            for key in in_myproduct_urls_dict:
                if prod_group_title in key:
                    prod_group_title = key
                    in_myproduct_urls = in_myproduct_urls_dict[prod_group_title]

            prod_link_tags = prod_group_div.query_selector_all(
                "a"
                )
            for prod_link_tag in prod_link_tags:
                in_myproduct_urls.append(prod_link_tag.get_attribute('href'))

            in_myproduct_urls_dict[prod_group_title] = in_myproduct_urls

        milliseconds = randint(2, 4) * 1000
        delay(milliseconds)
    in_myproduct_urls = list(set(in_myproduct_urls))
    total_products = total_products + len(in_myproduct_urls)

    return in_myproduct_urls_dict, total_products

def visit_product_page(in_page, in_product_url):
    in_page.goto(in_product_url)

    return in_page

def get_lens_size(json_prod_object, product_description):
    pattern = r'(\d{2})-(\d{2})-(\d{3})'
    match = re.findall(pattern, product_description)
    try:
        lens_Size_w = match[0][0]
        frame_bridge = match[0][1]
        frame_temple = match[0][2]
    except:
        lens_Size_w = '0'
        frame_bridge = '0'
        frame_temple = '0'

    json_prod_object['$iLens_Size_w'] = lens_Size_w
    json_prod_object['$iFrame_Bridge'] = frame_bridge
    json_prod_object['$iFrame_Temple'] = frame_temple

    return json_prod_object

def get_variants(json_variant_obj, product_name, variants_tag, stock_tag):
    variant_img = variants_tag.query_selector("img")
    if variant_img:
        variant_img_url = variant_img.get_attribute('src').replace('_s.jpg', '.jpg')
        json_variant_obj['$iFrame_IMG_Mark'] = "1"
        if variant_img_url == "" or constants.no_prod_img_url_key.lower() in variant_img_url:
            json_variant_obj['$iFrame_IMG_Mark'] = "0"
            
    frame_color = variants_tag.query_selector("span").text_content().strip()
    pattern = r'^\d+'
    match = re.match(pattern, frame_color)
    variant_color_code = match.group() if match else ""
    frame_code = f'{product_name}_{variant_color_code}'
    
    json_variant_obj['$iFrame_Code'] = frame_code
    json_variant_obj['$iFrame_Color'] = frame_color
    json_variant_obj['$iFrame_IMAGE'] = variant_img_url

    stock_tag = stock_tag.query_selector("small")
    if stock_tag:
        json_variant_obj['$iFrame_Availability'] = 'Out of stock'

    return json_variant_obj

def get_prices(in_page, json_prod_object):

    product_label_price = in_page.query_selector(
        ".product-price.sale-price span.currency-amount.price"
        )
    if product_label_price:
        product_label_price = product_label_price.text_content().strip()
        json_prod_object['$iFrame_Price'] = product_label_price
    product_list_price = in_page.query_selector(
        ".product-price.list-price span.currency-amount.price"
        )
    if product_list_price:
        product_list_price = product_list_price.text_content().strip()
        json_prod_object['$iFrame_Retail'] = product_list_price
    currency_symbol = in_page.query_selector(
        ".product-price.list-price span.currency-symbol"
        )
    if currency_symbol:
        currency_symbol = currency_symbol.text_content().strip()
        json_prod_object['currency_symbol'] = currency_symbol

    return json_prod_object

def get_product_type(json_prod_object, prod_type_title, product_description):

    prod_material = None
    for material in config.prod_materials.keys():
        if material in prod_type_title:
            prod_material = material
            break
    
    if not prod_material:
        for material in config.prod_materials.keys():
            if material in product_description:
                prod_material = material
                break

    json_prod_object['$iProduct_Material'] = material
    for prod_type_key, keyword_to_update in config.prod_types.items():
        if prod_type_key in product_description.lower() or prod_type_key in prod_type_title.lower():
            json_prod_object['$iProduct_Type'] = keyword_to_update
            break
    
    for keyword, params in config.key_words.items():
        if keyword in product_description:
            for param in params:
                json_prod_object[param] = 'yes'

    return json_prod_object

def get_product_details(in_page, in_product_url, master_json, prod_type_title):

    json_prod_object = master_json[0].copy()
    if master_json[0]['$iBrand'] == '':
        master_json = []

    json_prod_object['updated_ts'] = current_utc_ts_iso()
    json_prod_object['$iModelURL'] = in_product_url

    brand_locator = in_page.locator('div.breadcrumb > ul > li:nth-last-child(2) a')
    brand_locator.wait_for(state='attached', timeout=10000)
    brand_name = brand_locator.text_content().strip()
    brand_url = brand_locator.get_attribute('href')
    json_prod_object['$iBrand'] = brand_name
    json_prod_object['$iBrandURL'] = brand_url

    if brand_name == 'Private Label White':
        json_prod_object['$iProduct_Gender'] = 'Women'
    elif brand_name == 'Private Label Black':
        json_prod_object['$iProduct_Gender'] = 'Man'
    else:
        json_prod_object['$iProduct_Gender'] = 'Unisex'

    product_name = in_page.query_selector(
        "h1.product-model-no"
        ).text_content().strip()
    json_prod_object['$iProduct_Name'] = product_name
    logging.info(f"Scraped {product_name}")

    product_description = in_page.query_selector(
        "p.product-description"
        ).text_content().strip()
    json_prod_object['Product_description'] = product_description.replace('\n', ' ').replace('\t', ' ')
    
    json_prod_object = get_product_type(json_prod_object, prod_type_title, product_description)
    json_prod_object = get_prices(in_page, json_prod_object)
    json_prod_object = get_lens_size(json_prod_object, product_description)

    prod_variants_tags = in_page.query_selector_all(
        "ul.list-inline.product-image-list > li:not(:last-child)"
        )
    prod_variants_stock_tags = in_page.query_selector_all(
        "table.table >tbody > tr"
        )
    
    for variants_tag, stock_tag in zip(prod_variants_tags, prod_variants_stock_tags):
        json_variant_obj = json_prod_object.copy()
        json_variant_obj = get_variants(
            json_variant_obj,
            product_name,
            variants_tag,
            stock_tag)

        master_json.append(json_variant_obj)

    return master_json
        
def run(playwright, master_json, in_master_json_file_path, all_scraper_run_details):
    
    context, in_page = initialize_browser(playwright, constants.website_url)
    # context.clear_cookies()
    # in_page.goto("https://privatelabel.partners/login")
    # delay(3000)
    # in_page.click('button[type="submit"]')
    collection_urls = get_collections_urls(in_page)
    print(collection_urls)
    in_myproduct_urls_dict, total_products = get_prod_urls(in_page, collection_urls)
    logging.info(f"Total product url {total_products}")

    for prod_type_title, in_myproduct_urls in in_myproduct_urls_dict.items():
        try:
            logging.info(f"Scraping {prod_type_title}.....")
            for in_product_url in in_myproduct_urls:
                if exists_in_master_json(master_json, config.unique_prod_key, in_product_url):
                    logging.info('Frame already exists in master json')
                    continue
                in_page = visit_product_page(in_page, in_product_url)
                print('executed visit product page')
                try:
                    master_json = get_product_details(in_page, in_product_url, master_json, prod_type_title)
                except:
                    logging.error(f'Got error in product details:', exc_info=True)
                    try:
                        in_page.reload()
                        master_json = get_product_details(in_page, in_product_url, master_json, prod_type_title)
                    except:
                        context.clear_cookies()
                        in_page.goto("https://privatelabel.partners/login")
                        delay(3000)
                        in_page.click('button[type="submit"]')
                        master_json = get_product_details(in_page, in_product_url, master_json, prod_type_title)

                logging.info('saving file....')
                with open(in_master_json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(master_json, file, indent=4)

                milliseconds = randint(7, 20) * 1000
                delay(milliseconds)
        except:
            logging.error(f'Error:', exc_info=True)

    current_run_detail = scraper_run_details(all_scraper_run_details, total_products, master_json)
    print(current_run_detail)

def start():
    setup_logging()
    in_master_json_file_path, all_scraper_run_details = setup_folder(constants.website_name, config.data_dir_path)
    master_json = initialize_master_json(in_master_json_file_path, config.base_json_format)

    with sync_playwright() as playwright:
        run(playwright, master_json, in_master_json_file_path, all_scraper_run_details)

if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        logging.error(f'Error: {str(e)}', exc_info=True)
    logging.shutdown()