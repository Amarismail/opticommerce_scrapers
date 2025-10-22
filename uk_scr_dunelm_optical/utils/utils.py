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

def initialize_browser(website_url, localhost=False, headless=False):

    from playwright.sync_api import sync_playwright
    import time
    playwright = sync_playwright().start()

    context = None
    if localhost:
        chrome_process = open_debugger_port_browser()
        time.sleep(4)
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

    return playwright, browser, context, in_page

def normalize_url(website_url, url, include_query=True):

    # try:
    from urllib.parse import urlparse, urlunparse

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
    
    normalized_url =  urlunparse((scheme, netloc, path, '', query, ''))
    if not include_query:
        normalized_url =  urlunparse((scheme, netloc, path, '', '', ''))

    return normalized_url

    # except:
    #     return None