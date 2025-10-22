def delay(milliseconds):
    import time
    
    time.sleep(milliseconds / 1000)

def setup_folder(website_name, data_dir_path):
    import os, sys
    import shutil
    
    website_name = website_name.lower().replace(" ", '_')
    in_master_json_filename = website_name + '_master.json'
    website_dir_path = os.path.join(data_dir_path, website_name.lower().replace(" ", '_'))
    backup_dir_path = os.path.join(website_dir_path, 'backup')
    in_master_json_file_path = os.path.join(website_dir_path, in_master_json_filename)
    in_master_json_backup_file = os.path.join(backup_dir_path, in_master_json_filename)

    all_scraper_run_details = os.path.join(data_dir_path, 'all_scraper_run_details.csv')

    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)

    if not os.path.exists(website_dir_path):
        os.makedirs(website_dir_path)

    if not os.path.exists(backup_dir_path):
        os.makedirs(backup_dir_path)
    
    if os.path.exists(in_master_json_file_path):
        shutil.copy(in_master_json_file_path, in_master_json_backup_file)
        os.remove(in_master_json_file_path)

    return in_master_json_file_path, all_scraper_run_details

def get_current_time_iso():
    from datetime import datetime, timezone

    current_time_utc = datetime.now(timezone.utc)
    iso_format_time = current_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return iso_format_time

def initialize_master_json(in_master_json_filename, base_json_format):

    import os, sys
    import json

    if os.path.exists(in_master_json_filename):
        with open(in_master_json_filename, 'r', encoding='utf-8') as file:
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

def open_debugger_port_browser():
    import subprocess

    PORT = 9222
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    # Launch Chrome with remote debugging enabled
    chrome_process = subprocess.Popen([
        chrome_path,  # Change to "chrome" or "chrome.exe" on Windows if needed
        f"--remote-debugging-port={PORT}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        "--user-data-dir=C:/localhost"
        # "--new-window"
    ])

    return chrome_process

def initialize_browser(
    website_url: str,
    localhost: bool = False,
    headless: bool = False):

    from playwright.sync_api import sync_playwright
    from playwright._impl._errors import Error  
    import time
    playwright = sync_playwright().start()

    if localhost:
        try:
            browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        except Error as e:
            print(e)
            if "BrowserType.connect_over_cdp" in str(e):
                chrome_process = open_debugger_port_browser()
                time.sleep(4)
                browser = playwright.chromium.connect_over_cdp("http://localhost:9222")

        if browser.contexts:
            context = browser.contexts[0]
        else:
            context = browser.new_context()

        page = context.pages[0] if context.pages else context.new_page()
    else:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
    
    page.goto(website_url)
    in_page = page

    return playwright, browser, context, in_page

def check_external_link(parsed_website_url, parsed_url):
    netloc = parsed_url.netloc
    website_netloc = parsed_website_url.netloc

    if netloc:
        if not netloc.startswith('www.') and website_netloc.startswith('www.'): 
            netloc = 'www.' + netloc.lstrip('www.')

        if website_netloc not in netloc:
            return True
        
    return False

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
    
    is_external_link = check_external_link(parsed_website_url, parsed_prod_url)
    if is_external_link:
        return is_external_link, None 
        
    if not netloc:
        netloc = parsed_website_url.netloc
        if not netloc.startswith('www.') and parsed_website_url.netloc.startswith('www.'):
            netloc = 'www.' + netloc.lstrip('www.')
        # path = parsed_prod_url.path.rstrip('/')   # look for more example in future scrapers

    # implemented this for www.demenego.it to check if the web page is in en. for future need to check if instead of include_query we can implement a var with img/non-img
    if not include_query and '/en' in config.website_prod_store_url and '/en' not in url:
        netloc = netloc + '/en'
    
    normalized_url =  urlunparse((scheme, netloc, path, '', query, ''))
    if not include_query:
        normalized_url =  urlunparse((scheme, netloc, path, '', '', ''))

    return is_external_link, normalized_url 

    # except:
    #     return None


def translate_word(word, source_lang='italian', target_lang='english'):
    from deep_translator import PonsTranslator
    translated_words = PonsTranslator(source=source_lang, target=target_lang).translate(word, return_all=True)

    return translated_words