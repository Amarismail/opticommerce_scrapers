def is_currency_symbol(char):
    import unicodedata

    return unicodedata.category(char) == 'Sc'

def visit_html_page(session, url, headers, cookies=None, params=None, requests_data=None, verify=True):
    
    import requests
    from bs4 import BeautifulSoup
    import urllib3
    import logging

    try:
        response = session.get(
            url,
            cookies=session.cookies,
            headers=headers,
            params=params,
            data=requests_data,
            verify=verify
            )

        in_page = BeautifulSoup(response.text, "html.parser")

    except requests.exceptions.SSLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            logging.error("Certificate verification failed. Unable to get local issuer certificate.")
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            return visit_html_page(
                session,
                url,
                headers,
                cookies=cookies,
                params=params,
                requests_data=requests_data,
                verify=False)

    return response.status_code, in_page

def request_website_api(session, url, headers, cookies=None, params=None, requests_data=None, verify=False):
    import json

    response = session.post(
        url,
        cookies=session.cookies,
        headers=headers,
        params=params,
        data=requests_data,
        verify=verify
        )
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

def get_frame_size(json_obj, str_with_size, current_size):

    import re

    size_json_keys = ['$iLens_Size_w', '$iFrame_Bridge', '$iFrame_Temple']
    str_with_size = re.sub(r"mm", "", str_with_size)
    pattern = r'(\d{2})\b\s*(?:[-–/¤]\s*\d{2}(?:\.\d{2})?)?\s*[-–/¤]\s*(\d{2})\b(?:\s*[-–/¤]\s*(\d{3}))?'
    matches = re.findall(pattern, str_with_size)
    for match in matches:
        for index, size_json_key in enumerate(size_json_keys):
            if json_obj[size_json_key] == '':
                json_obj[size_json_key] = match[index]

        if current_size and json_obj['$iLens_Size_w'] == current_size:
            break
        
    return json_obj

def is_color_name(name):

    import webcolors

    try:
        webcolors.name_to_hex(name)
        return True
    except ValueError:
        return False
    
def get_prod_color(keyword, extended_color_names, translate=False):

    from utils import translate_word
    import re

    if translate:
        words = re.findall(r'\b\w+\b', keyword)
        org_color_words_len = len(keyword)
        translated_words = translate_word(keyword, source_lang='italian', target_lang='english')
        for synonym in translated_words:
            words = re.findall(r'\b\w+\b', synonym)  # Finds words ignoring punctuation
            if len(words) <= org_color_words_len:
                prod_color = synonym
                if is_color_name(prod_color) or prod_color in extended_color_names:
                    print(f'{prod_color}: {is_color_name(prod_color)}')
                    return prod_color

        return prod_color

    if 'palladium' in keyword.lower():
        prod_color = 'Silver'
        return prod_color

    if is_color_name(keyword):
        prod_color = keyword
        return prod_color
    
    if keyword in extended_color_names:
        prod_color = keyword
        return prod_color
    
    return None

def check_image_url(url, verify=False):

    import requests
    import logging
    import config
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.head(url, headers=config.headers, timeout=20, verify=verify, allow_redirects=True)
        rsp_status_code = response.status_code

        if rsp_status_code == 200:
            return True
        else:
            logging.error(f"Failed to retrieve the image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking the URL: {e}")

    return False

def clean_up_shape(prod_shape, shapes):
    import re

    pattern = r'\s*-\s*\d+'
    clean_shape = re.sub(pattern, '', prod_shape.lower())
    clean_shape = clean_shape.replace('modified', '').replace('soft', '')
    clean_shape = clean_shape.strip()
    
    for shape in shapes:
        if shape in clean_shape:
            return shape
        
    return clean_shape

def get_product_type(json_obj, keyword, keyword_2=None , prod_material=None):

    import mappings

    if prod_material:
        json_obj['$iProduct_Material'] = prod_material

    if keyword_2:
        keyword_2 = keyword_2.lower()

    for prod_type_key, keyword_to_update in mappings.prod_types.items():
        if prod_type_key in keyword.lower() or (keyword_2 and prod_type_key in keyword_2):
            json_obj['$iProduct_Type'] = keyword_to_update
            break

    return json_obj