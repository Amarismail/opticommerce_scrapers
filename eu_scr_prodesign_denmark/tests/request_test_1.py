# import requests

# cookies = {
#     'ARRAffinity': '63b6bed011f5251ba7b28917d65b0d83a0f4dab42316ed51891c85df00b35710',
#     'ARRAffinitySameSite': '63b6bed011f5251ba7b28917d65b0d83a0f4dab42316ed51891c85df00b35710',
#     'ai_user': 'YhuYa8M5x0qdOCAkeepD6L|2024-10-22T14:08:12.547Z',
#     'ai_session': 'IRcbAYArDg5myKeyU45U/Q|1729663187323|1729663233540',
# }

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Referer': 'https://www.prodesigndenmark.com/optical/?CategoryId=3792&CollectionNames=Essential&PageSize=50&Page=1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

# params = {
#     'colorCode': '1614',
# }

# params = {
#     'CategoryId': '3792',
#     'PageSize': '50',
#     'Page': '1',
# }

# # params = {
# #     'product-page': '5'
# # }

# # url = 'https://eyeqeyewear.com/all-collections'
# # url = 'https://www.prodesigndenmark.com/optical/essential/fill/fill-4838/'
# url = 'https://www.prodesigndenmark.com/umbraco/surface/CategoryPage/Search'

# response = requests.get(
#     url,
#     params=params,
#     # cookies=cookies,
#     headers=headers,
# )

# print(response.status_code)

# import os, sys

# if getattr(sys, 'frozen', False):
#     curDir = os.path.dirname(sys.executable)
# elif __file__:
#     # Use the current working directory of the script that called this function
#     curDir = os.path.dirname(__file__)
#     # curDir = os.getcwd()
#         # this will get current dir of the script where fn is

# with open(f'{curDir}/test_request_1.html', 'w') as f:
#     f.write(response.text)


print(len(None))