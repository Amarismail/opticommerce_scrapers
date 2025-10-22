import requests

cookies = {
    'PHPSESSID': '22dj80471er375q45lhg3q08g4',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=22dj80471er375q45lhg3q08g4',
    'Referer': 'https://www.dunelmoptical.com/framesearch?daisnotspam=1&token=VVGN6cLYjtaBmuOT3O5NrrxwihjX4UlZ&search=1&parentnode=22&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_gender%5B%5D=unisex&search_gender%5B%5D=&search_gender%5B%5D=&search_children%5B%5D=&search_rimtype%5B%5D=&search_rimtype%5B%5D=&search_rimtype%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_eye=&search_dbl=&search_ed=&search_sl=&search_lensdepth=&price_from=&price_to=',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'daisnotspam': '1',
    # 'token': 'VVGN6cLYjtaBmuOT3O5NrrxwihjX4UlZ',
    'search': '1',
    'page': '2',
    'parentnode': '22',
    'search_range[]': [],
    'search_gender[]': 'unisex',
    'search_children[]': '',
    'search_rimtype[]': [],
    'search_material[]': [],
    'search_colour[]': [],
    'search_eye': '',
    'search_dbl': '',
    'search_ed': '',
    'search_sl': '',
    'search_lensdepth': '',
    'price_from': '',
    'price_to': '',
}

url = 'https://www.dunelmoptical.com/framesearch'
# url = 'https://www.dunelmoptical.com/framesearch?daisnotspam=1&token=VVGN6cLYjtaBmuOT3O5NrrxwihjX4UlZ&search=1&parentnode=22&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_range%5B%5D=&search_gender%5B%5D=unisex&search_gender%5B%5D=&search_gender%5B%5D=&search_children%5B%5D=&search_rimtype%5B%5D=&search_rimtype%5B%5D=&search_rimtype%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_material%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_colour%5B%5D=&search_eye=&search_dbl=&search_ed=&search_sl=&search_lensdepth=&price_from=&price_to='


# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
response = requests.get(
    url, 
    params=params, 
    # cookies=cookies,
    headers=headers,
    verify=False)

print(response.status_code)
print(response.text)

import os, sys
if getattr(sys, 'frozen', False):
    curDir = os.path.dirname(sys.executable)
elif __file__:
    curDir = os.path.dirname(__file__)


with open('requests_test_1.html', 'w') as f:
    f.write(response.text)