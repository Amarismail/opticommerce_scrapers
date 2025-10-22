# import requests

# headers = {
#     'Referer': 'https://offview.com/en-uk',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

# response = requests.get('https://offview.com/en-uk/collections/gigi-studios-all', headers=headers)


# print(response.status_code)
# print(response.text)

# with open('./uk_scr_offview/tests/request_test_1.html', 'w', encoding='utf-8') as f:
#     f.write(response.text)


import requests

headers = {
    'Referer': 'https://offview.com/en-uk/collections/gigi-studios-all',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://offview.com/en-uk/products/8123-2', headers=headers)


print(response.status_code)
print(response.text)

with open('./uk_scr_offview/tests/request_test_2.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
