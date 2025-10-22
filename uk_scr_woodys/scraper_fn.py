from utils.utils import normalize_url
from utils.scraper_utils import check_image_url, clean_up_shape, get_product_type
import json

def config_variant_request(prod_item_num, requests_data_value_list, requests_data):
    requests_data = requests_data
    requests_data['styleItemNumber'] = prod_item_num
    requests_data['styleVariantList'] = json.dumps(requests_data_value_list, separators=(',', ':'))
    return requests_data

def config_store_page_request(category_name, category_link, page_num):

    import config
    if config.prod_store_api_base_url:
            category_link = config.prod_store_api_base_url

    if config.params:
        params = config.params
        params[list(params.keys())[0]] = str(page_num)
        if config.categories_id_map:
            for key, value in config.categories_id_map.items():
                if key == category_name.lower():
                    for key, value in value.items():
                        params[key] = value

        return category_link, params
    
    # added this for https://www.demenego.it/
    if not config.params and config.website_prod_store_url_navigation:
        category_link = config.prod_store_api_base_url + str(page_num)

    return category_link, None

def get_prod_final_image(json_obj, variant_img_url, website_url, no_prod_img_url_key):
    from urllib.parse import urlparse, urlunparse

    if not variant_img_url or variant_img_url == "" or no_prod_img_url_key.lower() in variant_img_url:
        return json_obj

    # variant_img_url = urlunparse(urlparse(variant_img_url)._replace(query=""))
    # if config.website_img_base_url not in variant_img_url:
    #     variant_img_url = config.website_img_base_url + variant_img_url

    is_external_link, variant_img_url = normalize_url(website_url, variant_img_url)
    check = check_image_url(variant_img_url)
    if not check:
        return json_obj

    json_obj['$iFrame_IMAGE'] = variant_img_url
    json_obj['$iFrame_IMG_Mark'] = "1"

    return json_obj


def map_variants_info_tags(variant_url_tags, prod_variant_colors):
    from itertools import zip_longest

    variant_url_tags = list(dict.fromkeys(variant_url_tags))
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

def map_website_keywords_to_json(json_obj, prod_all_specs, website_keyword_to_json_mapping, shapes):
    key_mapping = website_keyword_to_json_mapping
    splitters = [':', '\n']
    spec_key = None
    for spec in prod_all_specs:
        spec = spec.text.strip()
        # print('-----------------------')
        # print(spec)
        # implemented ':' for eyeqeyewear.com and '\n' for dunelmoptical.com
        # used .text to keep all the sting special cheaters like \n
        for splitter in splitters:
            # below lineRemove extra blank lines by replacing multiple newlines with a single newline
            cleaned_spec = "\n".join(filter(None, spec.split("\n")))
            if splitter in cleaned_spec:
                spec_key = cleaned_spec.split(splitter)[0].strip().lower()
                spec_value = cleaned_spec.split(splitter)[1].strip().lower()

        if spec_key in key_mapping.keys():
            json_obj_key = key_mapping[spec_key]
            json_obj[json_obj_key] = spec_value.replace(' mm', '')

            if json_obj_key == '$iProduct_Shape':
                clean_prod_shape = clean_up_shape(spec_value, shapes)
                json_obj[json_obj_key] = clean_prod_shape
            
        if not spec_key:
            get_product_type(json_obj, keyword=spec)

    return json_obj