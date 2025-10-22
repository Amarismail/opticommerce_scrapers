def delay(milliseconds):
    import time
    
    time.sleep(milliseconds / 1000)

def setup_folder(in_master_json_filename):
    import os, sys

    if getattr(sys, 'frozen', False):
        curDir = os.path.dirname(sys.executable)
    elif __file__:
        # Use the current working directory of the script that called this function
        curDir = os.getcwd()
        # this will get current dir of the script where fn is
        # curDir = os.path.dirname(__file__)
    
    data_dir_path = os.path.join(curDir, 'data')
    in_master_json_file_path = os.path.join(data_dir_path, in_master_json_filename)

    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)

    logging_file_path = os.path.join(curDir, 'info.log')

    return in_master_json_file_path, logging_file_path

def get_current_time_iso():
    from datetime import datetime, timezone

    current_time_utc = datetime.now(timezone.utc)
    iso_format_time = current_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return iso_format_time

def initialize_master_json(in_master_json_filename, base_json_format):

    import os, sys
    import json

    if os.path.exists(in_master_json_filename):
        with open(in_master_json_filename, 'r') as file:
            master_json = json.load(file)

        return master_json

    master_json = base_json_format

    return master_json

def exists_in_master_json(master_json, unique_value):
    import config

    check = list(filter(lambda x:x[config.unique_prod_key]==unique_value, master_json))
    if check:
        return True
    
    return False

def initialize_browser(website_url, localhost=False, headless=False):

    from playwright.sync_api import sync_playwright
    
    playwright = sync_playwright().start()

    if localhost:
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        if context.pages:
            page = context.pages[0]
        else:
            page = browser.new_page()
    else:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_page()
    
    page.goto(website_url)
    in_page = page

    return playwright, browser, in_page

def normalize_url(website_url, url, include_query=True):

    # try:
    from urllib.parse import urlparse, urlunparse
    import config

    parsed_prod_url = urlparse(url)
    parsed_website_url = urlparse(website_url)
    netloc = parsed_prod_url.netloc
    scheme = parsed_prod_url.scheme
    path = parsed_prod_url.path
    query = parsed_prod_url.query

    # Ensure the URL has a scheme
    if not scheme:
        scheme = parsed_website_url.scheme
        
    if not netloc:
        netloc = parsed_website_url.netloc
        if not netloc.startswith('www.'):
            netloc = 'www.' + netloc.lstrip('www.')
        # path = parsed_prod_url.path.rstrip('/')   # look for more example in future scrapers

    # implemented this for www.demenego.it to check if the web page is in en. for future need to check if instead of include_query we can implement a var with img/non-img
    if not include_query and '/en' in config.website_prod_store_url and '/en' not in url:
        netloc = netloc + '/en'
    
    normalized_url =  urlunparse((scheme, netloc, path, '', query, ''))
    if not include_query:
        normalized_url =  urlunparse((scheme, netloc, path, '', '', ''))

    return normalized_url

    # except:
    #     return None


def translate_word(word, source_lang='italian', target_lang='english'):
    from deep_translator import PonsTranslator
    translated_words = PonsTranslator(source=source_lang, target=target_lang).translate(word, return_all=True)

    return translated_words