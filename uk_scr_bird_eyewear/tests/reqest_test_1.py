import requests

cookies = {
    'secure_customer_sig': '',
    'localization': 'GB',
    '_shopify_y': 'd074a6a9-ff91-4519-8fd1-548f8e4fdfbc',
    '_orig_referrer': 'https%3A%2F%2Fopticommerce.atlassian.net%2F',
    '_landing_page': '%2Fcollections%2Fall-eyewear',
    '_ga': 'GA1.1.449042189.1730443654',
    'hubspotutk': 'b14cc54b91f7983f591e9ac0b9186146',
    '_tracking_consent': '%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22PKPB%22%2C%22reg%22%3A%22%22%2C%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%2C%22consent_id%22%3A%22625AC885-bee4-4194-aa0f-887763bc0712%22%7D',
    '_cmp_a': '%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D',
    '_hjSessionUser_5194921': 'eyJpZCI6ImIzYTBiZjczLTE4OGUtNThkNC1hNzY1LWQwMGM3NzNmOWVlOCIsImNyZWF0ZWQiOjE3MzA5NTkzNzk2MDYsImV4aXN0aW5nIjp0cnVlfQ==',
    '__hssrc': '1',
    '_hjSession_5194921': 'eyJpZCI6IjliYTcwYjM1LWU0ZDAtNDBiMS1iNWY1LTBmZWM0MmUwZGYyMCIsImMiOjE3MzA5ODM0NTgwNDUsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    'keep_alive': 'e4e36d16-d0bb-402e-b38e-dec11fcb7308',
    '_shopify_s': '04613ed3-1a9c-4e89-a776-4514b3267c61',
    '_shopify_sa_t': '2024-11-07T12%3A58%3A25.675Z',
    '_shopify_sa_p': '',
    '__hstc': '102379230.b14cc54b91f7983f591e9ac0b9186146.1730443657541.1730981097255.1730984307601.5',
    '__hssc': '102379230.1.1730984307601',
    '_ga_GPQB303KNC': 'GS1.1.1730984304.7.1.1730984343.0.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'cookie': 'secure_customer_sig=; localization=GB; _shopify_y=d074a6a9-ff91-4519-8fd1-548f8e4fdfbc; _orig_referrer=https%3A%2F%2Fopticommerce.atlassian.net%2F; _landing_page=%2Fcollections%2Fall-eyewear; _ga=GA1.1.449042189.1730443654; hubspotutk=b14cc54b91f7983f591e9ac0b9186146; _tracking_consent=%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22PKPB%22%2C%22reg%22%3A%22%22%2C%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%2C%22consent_id%22%3A%22625AC885-bee4-4194-aa0f-887763bc0712%22%7D; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D; _hjSessionUser_5194921=eyJpZCI6ImIzYTBiZjczLTE4OGUtNThkNC1hNzY1LWQwMGM3NzNmOWVlOCIsImNyZWF0ZWQiOjE3MzA5NTkzNzk2MDYsImV4aXN0aW5nIjp0cnVlfQ==; __hssrc=1; _hjSession_5194921=eyJpZCI6IjliYTcwYjM1LWU0ZDAtNDBiMS1iNWY1LTBmZWM0MmUwZGYyMCIsImMiOjE3MzA5ODM0NTgwNDUsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; keep_alive=e4e36d16-d0bb-402e-b38e-dec11fcb7308; _shopify_s=04613ed3-1a9c-4e89-a776-4514b3267c61; _shopify_sa_t=2024-11-07T12%3A58%3A25.675Z; _shopify_sa_p=; __hstc=102379230.b14cc54b91f7983f591e9ac0b9186146.1730443657541.1730981097255.1730984307601.5; __hssc=102379230.1.1730984307601; _ga_GPQB303KNC=GS1.1.1730984304.7.1.1730984343.0.0.0',
    'priority': 'u=0, i',
    'referer': 'https://birdeyewear.co.uk/collections/all-eyewear',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

params = {
    'page': '10',
}

params = {'page': '10'}

session = requests.Session()
response = session.get(
    # 'https://birdeyewear.co.uk/collections/all-eyewear',
    'https://birdeyewear.co.uk/collections/all-eyewear',
    params=params,
    # cookies=cookies,
    headers=headers)

print(response.status_code)
print(response.text)

# json_data = response.text.split('webPixelsManagerAPI.publish("collection_viewed",', ');},')


import re
pattern = r'webPixelsManagerAPI\.publish\("collection_viewed",\s*(.*?)\s*\);},'

# Search for the pattern
match = re.search(pattern, response.text)

# Extract the text if a match is found
if match:
    extracted_text = match.group(1)
    print("Extracted text:", extracted_text)
else:
    print("Pattern not found")



with open('request_test_1.html', "w", encoding='utf-8') as f:
    f.write(response.text)