import requests

cookies = {
    '_ga': 'GA1.2.2097204350.1731932651',
    '_gid': 'GA1.2.1222156745.1734908731',
    '_gat': '1',
    '_ga_B2GRLFQT71': 'GS1.2.1734954341.11.1.1734954343.0.0.0',
    'BIGipServerji-nossl-job-23.portal.webmd.com-80': '117513482.20480.0000',
    'ASP.NET_SessionId': 'g0esh5m1yn32qwll2v45eq3q',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga=GA1.2.2097204350.1731932651; _gid=GA1.2.1222156745.1734908731; _gat=1; _ga_B2GRLFQT71=GS1.2.1734954341.11.1.1734954343.0.0.0; BIGipServerji-nossl-job-23.portal.webmd.com-80=117513482.20480.0000; ASP.NET_SessionId=g0esh5m1yn32qwll2v45eq3q',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

url = 'https://www.classique-eyewear.com/laura-ashley/laura-ashley/default.aspx'
url ='https://www.classique-eyewear.com/laura-ashley/laura-ashley/vivica'

response = requests.get(
    url,
    # cookies=cookies,
    headers=headers,
)

print(response.status_code)
print(response.text)

import os, sys
if getattr(sys, 'frozen', False):
    curDir = os.path.dirname(sys.executable)
elif __file__:
    curDir = os.path.dirname(__file__)


with open('requests_test_1.html', 'w', encoding='utf-8') as f:
    f.write(response.text)