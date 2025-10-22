def visit_html_page(session, url):
    import config
    from bs4 import BeautifulSoup

    response = session.get(url, headers=config.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    in_page = soup

    return in_page

def request_website_api(session, url, cookies=None, params=None, requests_data=None):
    import config
    import json

    response = session.post(
        url,
        cookies=session.cookies,
        headers=config.headers,
        data=requests_data,)
    response_status = int(response.status_code)
    if response_status == 200:
        json_data = json.loads(response.text.replace("'", '"'))
        return response_status, json_data

    return response_status, None

def slow_scroll_to_bottom(page, scroll_step=60, scroll_delay=0.05):
    import time

    current_height = 0
    total_height = page.evaluate("document.body.scrollHeight")
    
    while current_height < total_height:
        # Scroll down by small steps
        page.evaluate(f"window.scrollBy(0, {scroll_step});")
        
        # Wait for the dynamic content to load
        time.sleep(scroll_delay)  # Adjust the delay based on content load speed
        
        # Update current height and total height to handle dynamic content loading
        current_height = page.evaluate("window.scrollY + window.innerHeight")
        total_height = page.evaluate("document.body.scrollHeight")

def get_lens_size(json_obj, str_with_size, current_size):

    import re

    pattern = r'(\d{2})\s*[-–/]\s*(\d{2})\s*[-–/]\s*(\d{3})'
    matchs = re.findall(pattern, str_with_size)
    for match in matchs:
        try:
            lens_Size_w = match[0]
            frame_bridge = match[1]
            frame_temple = match[2]
        except:
            lens_Size_w = '0'
            frame_bridge = '0'
            frame_temple = '0'
        
        json_obj['$iLens_Size_w'] = lens_Size_w
        json_obj['$iFrame_Bridge'] = frame_bridge
        json_obj['$iFrame_Temple'] = frame_temple

        if current_size and lens_Size_w == current_size:
            break

    return json_obj

def is_color_name(name):

    import webcolors

    try:
        webcolors.name_to_hex(name)
        return True
    except ValueError:
        return False
    
def get_prod_color(product_tags, extended_color_names):
    product_tags = product_tags.split(',')
    for prod_tag in product_tags:
        if 'palladium' in prod_tag.lower():
            prod_color = 'Silver'
            return prod_color

        if is_color_name(prod_tag):
            prod_color = prod_tag
            return prod_color
        
        if prod_tag in extended_color_names:
            prod_color = prod_tag
            return prod_color
    
    return None

def check_image_url(url):

    import requests
    import logging

    try:
        response = requests.head(url, timeout=5)
        rsp_status_code = response.status_code

        if rsp_status_code == 200:
            return True
        else:
            logging.error(f"Failed to retrieve the image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking the URL: {e}")

    return False

def scraper_run_details(all_scraper_run_details, total_products, master_json):
    from utils.utils import get_current_time_iso
    import pandas as pd
    import constants

    # run_details_df = pd.read_csv(all_scraper_run_details, index=False)
    master_df = pd.json_normalize(master_json)
    count_condition = master_df["$iFrame_IMAGE"].isna() | (master_df["$iFrame_IMAGE"] == "") | (master_df["$iFrame_IMAGE"] == "https://masterdb.co.uk/images/awaiting.jpg")
    
    current_run_detail = pd.DataFrame([{
        "supplier": master_json[0]["$iSupplier"],
        "brand_name": master_json[0]["$iBrand"],
        "country": constants.country,
        "website_url": constants.website_url,
        "website_name": constants.website_name,
        "run_total_products": total_products,
        "run_total_variant": len(master_json),
        "new_products_count": 0,
        "new_variant_count": 0,
        "run_total_img_count": (~count_condition).sum(),
        "new_img_count": 0,
        "no_img_variants_count": count_condition.sum(),
        "status": "unknown",
        "updated_ts": get_current_time_iso(),
        }])
    
    current_run_detail.to_csv(all_scraper_run_details, mode='a', header=False, index=False)

    return current_run_detail