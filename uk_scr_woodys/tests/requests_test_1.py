import requests

headers = {
    # 'Cookie': 'PrestaShop-c01261a537466c4012b3b24e6b64e9ec=def50200b2bbedbaac06cf335bb5942730fe7979ebd692c82c16ef9f3b84c91ff1e00ba2fe32709f087f93b075addefef22d7d9bfb9ff597d23c2b97fd2b34550271a28e41898c34e8fff80235b50289ccd473ccc6e726c77834e9df1cf8d94831a8425cc46a2647c87faed07c8ab137980537441af64a650278bc80068a0b79371e6d5bfa18ca321b48cdc08431e39994a2955256972b2be51f6f0051f7feb860e9e170b0f86b0d6fa6b7ee49b06d237467edd3783a7532ce4922da6961bb88bfc13f6fe2462331effe50e45d058c81bae611a3c666692f88b83021c6f7c11ca47e1fc4c928715c639cae4746ea32b92077eed54f3e3cb5f66077aca1e429fd3a7592e6a47397d6b163e046106d5a3495941f4f75a75680718e86fee9aa7715210f3649b57eaf6aad0501d5a81a847bedbc4368ca6182f18059b020bd3b645459da; PHPSESSID=csq5unap7tlqt8eqk0746h5eq9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://woodyseyewear.com/en/gafas-de-ver',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'content_only': '1',
    'page': '10',
}

url = 'https://woodyseyewear.com/en/gafas-de-ver'
# url = 'https://woodyseyewear.com/en/kanso/ash'
url = 'https://woodyseyewear.com/en/petite/fito'

response = requests.get(
    url, 
    # params=params,
    headers=headers)
print(response.status_code)
# print(response.text)

import re
import json
import html
from bs4 import BeautifulSoup

in_page = BeautifulSoup(response.text, "html.parser")
page_text = in_page.prettify()
pattern = r'id="product-details-disabled" data-product="(\{.*?\})">'
# match = re.search(pattern, page_text)
# if match:
#     imbedded_json_text = html.unescape(match.group(1))
# prod_json_detail = json.loads(imbedded_json_text)
# print(prod_json_detail)

pattern = r'Material&quot;,&quot;value&quot;:&quot;(.*?)&quot;,&quot;id_feature'
# pattern = r'Material","value":"(.*?)","id_feature'
match = re.search(pattern, page_text)
if match:
    imbedded_json_text = match.group(1)
print(match.group(1))

pattern = r'&quot;Gender&quot;,&quot;value&quot;:&quot;(.*?)&quot;,&quot;id_feature'
# pattern = r'"Gender","value":"(.*?)","id_feature'
match = re.search(pattern, page_text)
print(match.group(1))

import os, sys
if getattr(sys, 'frozen', False):
    curDir = os.path.dirname(sys.executable)
elif __file__:
    curDir = os.path.dirname(__file__)


with open('requests_test_1.html', 'w', encoding='utf-8') as f:
    f.write(response.text)