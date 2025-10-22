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

def initialize_browser(playwright, website_url):

    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    if context.pages:
        page = context.pages[0]
    else:
        page = browser.new_page()
    page.goto(website_url)
    in_page = page

    return browser, in_page

def normalize_url(website_url, url):

    try:
        from urllib.parse import urlparse, urlunparse

        parsed_prod_url = urlparse(url)
        parsed_website_url = urlparse(website_url)

        # Ensure the URL has a scheme
        if not parsed_prod_url.scheme:
            scheme = parsed_website_url.scheme
            netloc = parsed_prod_url.netloc
            path = parsed_prod_url.path
            query = parsed_prod_url.query
            
        if not netloc:
            netloc = parsed_website_url.netloc
            if not netloc.startswith('www.'):
                netloc = 'www.' + netloc.lstrip('www.')
            # path = parsed_prod_url.path.rstrip('/')   # look for more example in future scrapers
        
        normalized_url = urlunparse((scheme, netloc, path, '', query, ''))

        return normalized_url

    except:
        return None