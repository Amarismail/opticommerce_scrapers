import requests

cookies = {
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2024-11-25%2013%3A41%3A58%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.demenego.it%2Fen%2Fprodotto%2Ftom-ford-ft0711%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2024-11-25%2013%3A41%3A58%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.demenego.it%2Fen%2Fprodotto%2Ftom-ford-ft0711%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29',
    'wt_consent': 'consentid:V0Z1MW9jS2NEREZuSDJ0eWR0eHJ1TVdwVDVaUFFTQTc,consent:yes,action:yes,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,others:yes,consent_time:1732606388862',
    '_gcl_au': '1.1.1516392503.1732606389',
    '_ga': 'GA1.1.1408289573.1732606387',
    '_fbp': 'fb.1.1732606389259.583146333750252780',
    'sbjs_udata': 'vst%3D5%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F131.0.0.0%20Safari%2F537.36',
    'sbjs_session': 'pgs%3D20%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.demenego.it%2Fen%2Fbrand%2Fopera-chic%2F',
    '_ga_0WYYYHZTW7': 'GS1.1.1732687377.6.1.1732689003.0.0.0',
}

headers = {
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2024-11-25%2013%3A41%3A58%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.demenego.it%2Fen%2Fprodotto%2Ftom-ford-ft0711%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2024-11-25%2013%3A41%3A58%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.demenego.it%2Fen%2Fprodotto%2Ftom-ford-ft0711%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29; wt_consent=consentid:V0Z1MW9jS2NEREZuSDJ0eWR0eHJ1TVdwVDVaUFFTQTc,consent:yes,action:yes,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,others:yes,consent_time:1732606388862; _gcl_au=1.1.1516392503.1732606389; _ga=GA1.1.1408289573.1732606387; _fbp=fb.1.1732606389259.583146333750252780; sbjs_udata=vst%3D5%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F131.0.0.0%20Safari%2F537.36; sbjs_session=pgs%3D20%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.demenego.it%2Fen%2Fbrand%2Fopera-chic%2F; _ga_0WYYYHZTW7=GS1.1.1732687377.6.1.1732689003.0.0.0',
    'if-modified-since': 'Wed, 27 Nov 2024 06:19:01 GMT',
    'priority': 'u=1, i',
    'referer': 'https://www.demenego.it/en/brand/opera-chic/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'page': '3'
}
url = 'https://www.demenego.it/en/brand/opera-chic/page/8'
# url = 'https://www.demenego.it/en/prodotto/opera-chic-ch1068/'
response = requests.get(
    url, 
    # params=params, 
    # cookies=cookies,
    headers=headers,
    # verify=False
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