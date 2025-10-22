import requests

# cookies = {
#     'PHPSESSID': '9cpijf20b2jkqecacb7i2vhmr7',
# }

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'PHPSESSID=9cpijf20b2jkqecacb7i2vhmr7',
    'Origin': 'https://www.dunelmoptical.com',
    'Referer': 'https://www.dunelmoptical.com/login',
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

data = {
    'token': 'STmWOANLKVDZ9UOkHOdImdV3ubpsfag7',
    'next': 'paul-costelloe-5193',
    'username': 'Jo@diblow.co.uk',
    'password': 'Portland',
    'login': 'Sign in',
}

session = requests.Session()
response = session.get(
    'https://www.dunelmoptical.com/',
    cookies=session.cookies,
    headers=headers,
    verify=False)
response = session.post(
    'https://www.dunelmoptical.com/login',
    cookies=session.cookies,
    headers=headers,
    data=data,
    verify=False)
print(response.status_code)

if response.cookies:
    print("Cookies are set:", response.cookies)

for cookie_name, cookie_value in response.cookies.items():
    print(f"{cookie_name}: {cookie_value}")

print('----------------------------------------')
# Check if the session has cookies set
if session.cookies:
    print("Session cookies are set:")
    for cookie in session.cookies:
        print(f"{cookie.name}: {cookie.value}")
else:
    print("No cookies set in the session.")

import os, sys
if getattr(sys, 'frozen', False):
    curDir = os.path.dirname(sys.executable)
elif __file__:
    curDir = os.path.dirname(__file__)

# cookies = {
#     # 'PHPSESSID': '9cpijf20b2jkqecacb7i2vhmr7',
#     'username': 'jo%40diblow.co.uk',
#     'usertoken': '6b2df5941409b17fa636b9bd0884656b',
# }

# response = session.get(
#     'https://www.dunelmoptical.com/paul-costelloe-5193',
#     cookies=session.cookies,
#     headers=headers,
#     verify=False)
# print(response.status_code)

with open('requests_test_1.html', 'w') as f:
    f.write(response.text)