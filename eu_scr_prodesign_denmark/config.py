import constants
import base_json

data_dir_path = r'C:\Users\Ammar Ismail\Desktop\main\opticommerce\data'
base_json.base_json_format[0]["$iSupplier"] = constants.website_name
base_json.base_json_format[0]["$iBrandURL"] = constants.website_url
base_json.base_json_format[0]["$iCountry"] = constants.country
base_json_format = base_json.base_json_format
brand_name = constants.website_name
in_master_json_filename = constants.website_name + '_master.json'
website_prod_store_url = constants.website_url
prod_store_api_base_url = constants.website_url + '/umbraco/surface/CategoryPage/Search'
prod_store_page_url_params = f'?product-page='

website_img_base_url = constants.website_url + '/images/items/'
variant_api_base_url = None

unique_prod_key = '$iModelURL'  # no unique key
request_variants_data = True
page_size = 250

# catagories_id_map = {
#     'optical' : '3792',
#     'sun' : '3798'
# }

catagories_id_map = {
    'optical' : '6327',
    'sun' : '6338'
}

params = {
    'CategoryId': '',
    'PageSize': page_size,
    'Page': '',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}