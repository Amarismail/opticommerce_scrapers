import requests

cookies = {
    'localization': 'GB',
    '_shopify_y': '729d3afa-ffec-4ed2-90f6-eb2d630a5fc1',
    '_orig_referrer': 'https%3A%2F%2Fopticommerce.atlassian.net%2F',
    '_landing_page': '%2Fen-sx%2FESP%2Flogin',
    'swym-pid': '"/W21uYdX+cEF3b0CLrMXOqm6sI7nFh4Dbn9faLwWi5c="',
    '__kla_id': 'eyJjaWQiOiJOV1ptWkdRMVlUWXRPRGszWkMwME1tSXhMV0UxT0RNdE56WXhPVGhsTTJFM1ltUmsifQ==',
    '_ga': 'GA1.1.1221910679.1759202118',
    'localization': 'ES',
    '_ga_Q0CJYFSN41': 'GS2.1.s1759202117$o1$g1$t1759202313$j60$l0$h0',
    'swym-email': '"kiran.insight@gmail.com"',
    'swym-swymRegid': '"DM8bz238eFiFqSNbj0WIc9EVxxLpyzo1rdCtZF397LSxicX2UTDgZFDEC437EiHCxdrM5GjNaTSGmcqcu7ImOk6aiN0_mPraHYb329tE-EahRjkvVoKXc8QWSy5gpdT-1MRMhkQwg5gaJGp0TpkUixD4ukFwyI1jCLCl4AQb4boHjOxPUTGw5n2TQBGEMhH7nwDMfcVTK5jc5WVneLoyaA"',
    'cookiefirst-consent': '%7B%22necessary%22%3Atrue%2C%22performance%22%3Afalse%2C%22functional%22%3Afalse%2C%22advertising%22%3Afalse%2C%22timestamp%22%3A1759202312%2C%22type%22%3A%22category%22%2C%22version%22%3A%22d2aef5ff-25a7-4f74-afa1-ca3d63357949%22%7D',
    'swym-session-id': '"hechh5m0xni4n8ovgtefqq9amezbrepfyc2kwwqqsuy716ha34aqroxnz6m7ooqe"',
    '_tracking_consent': '3.AMPS_PKPB_f_f_GcZlesjyRnCuR0yJ-d3XdQ',
    'cart': 'hWN3vvA4XR5tnUChvDLFxd0j%3Fkey%3Dbb2ad04ad578f11e42beee21d73eeac1',
    'cart_currency': 'GBP',
    '_shopify_essential': ':AZmYnf0UAAH_VxNz01gJUwmEnqCfBDYGMAQAVa6ev8Wj6gvJR0RprTLam8yxxUGU8FGOnGRsjUus3fWUUO7ezrwd4Rn191fVcINFXjx06_FLo42jGzzfdMo-CnaZ1UVfcpwBt38xvarXsMbob4Zog_mBUGClgpHRr6duF5HPVSIWRPN1HNErmKfD5wzoYd05owfF2u05FRpw3TZ9dWdDsLIk66HdzPq4-RhDanRMvblw5RbpvRtO35RNn9Y5LKD4W3q-WueXyiNS8JpWFy1jekclVPPfWgl7N8wcO0VhVO_cuYzjttMMoHeXA0qMK_3btO0qxWre2mvCeH2IqT8eaUShfSV2X8jkUbbnDc5QkcRriCA-WSgVrtorQJqC0_RqCwkXJI3V3gRl2904-bEkbm6si6zQBDoMfPU0rtA6awI_2yhdS09_u2Iq-iVq:',
    'shopify_recently_viewed': '8122-2%206865-7%206957-7%20garantia%206865-6%20gs1019-20s%20gs1019-23s%20gs1019-25s%206865-1%206865-0',
    'swym-v-ckd': '1',
    'swym-o_s': '{"wishlist-app_app-embed_170079715521":"2025-10-10T04:08:48.335Z","mktenabled":false}',
    '_shopify_s': 'e56bf988-a6ab-4692-9f51-503af5fb717f',
    'swym-nf_svd': '1',
    'keep_alive': 'eyJ2IjoyLCJ0cyI6MTc2MDA2OTYwNTAwNiwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoxNCwiY2EiOjAsImthIjowLCJzYSI6MCwia2JhIjowLCJ0YSI6MCwidCI6NDEsIm5tIjoxLCJtcyI6MC4zOCwibWoiOjAuNzIsIm1zcCI6MC43NywidmMiOjAsImNwIjowLCJyYyI6MCwia2oiOjAsImtpIjowLCJzcyI6MCwic2oiOjAsInNzbSI6MCwic3AiOjAsInRzIjowLCJ0aiI6MCwidHAiOjAsInRzbSI6MH0sInNlcyI6eyJwIjozMywicyI6MTc1OTc1OTQ4ODE0NiwiZCI6MzA4MzEzfX0%3D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'if-none-match': '"cacheable:ac2b5842acf570855992f9ea9617b06a"',
    'priority': 'u=1, i',
    'referer': 'https://offview.com/en-uk/collections/gigi-studios-all?sort_by=best-selling&filter.p.m.product.genero=Women',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': 'localization=GB; _shopify_y=729d3afa-ffec-4ed2-90f6-eb2d630a5fc1; _orig_referrer=https%3A%2F%2Fopticommerce.atlassian.net%2F; _landing_page=%2Fen-sx%2FESP%2Flogin; swym-pid="/W21uYdX+cEF3b0CLrMXOqm6sI7nFh4Dbn9faLwWi5c="; __kla_id=eyJjaWQiOiJOV1ptWkdRMVlUWXRPRGszWkMwME1tSXhMV0UxT0RNdE56WXhPVGhsTTJFM1ltUmsifQ==; _ga=GA1.1.1221910679.1759202118; localization=ES; _ga_Q0CJYFSN41=GS2.1.s1759202117$o1$g1$t1759202313$j60$l0$h0; swym-email="kiran.insight@gmail.com"; swym-swymRegid="DM8bz238eFiFqSNbj0WIc9EVxxLpyzo1rdCtZF397LSxicX2UTDgZFDEC437EiHCxdrM5GjNaTSGmcqcu7ImOk6aiN0_mPraHYb329tE-EahRjkvVoKXc8QWSy5gpdT-1MRMhkQwg5gaJGp0TpkUixD4ukFwyI1jCLCl4AQb4boHjOxPUTGw5n2TQBGEMhH7nwDMfcVTK5jc5WVneLoyaA"; cookiefirst-consent=%7B%22necessary%22%3Atrue%2C%22performance%22%3Afalse%2C%22functional%22%3Afalse%2C%22advertising%22%3Afalse%2C%22timestamp%22%3A1759202312%2C%22type%22%3A%22category%22%2C%22version%22%3A%22d2aef5ff-25a7-4f74-afa1-ca3d63357949%22%7D; swym-session-id="hechh5m0xni4n8ovgtefqq9amezbrepfyc2kwwqqsuy716ha34aqroxnz6m7ooqe"; _tracking_consent=3.AMPS_PKPB_f_f_GcZlesjyRnCuR0yJ-d3XdQ; cart=hWN3vvA4XR5tnUChvDLFxd0j%3Fkey%3Dbb2ad04ad578f11e42beee21d73eeac1; cart_currency=GBP; _shopify_essential=:AZmYnf0UAAH_VxNz01gJUwmEnqCfBDYGMAQAVa6ev8Wj6gvJR0RprTLam8yxxUGU8FGOnGRsjUus3fWUUO7ezrwd4Rn191fVcINFXjx06_FLo42jGzzfdMo-CnaZ1UVfcpwBt38xvarXsMbob4Zog_mBUGClgpHRr6duF5HPVSIWRPN1HNErmKfD5wzoYd05owfF2u05FRpw3TZ9dWdDsLIk66HdzPq4-RhDanRMvblw5RbpvRtO35RNn9Y5LKD4W3q-WueXyiNS8JpWFy1jekclVPPfWgl7N8wcO0VhVO_cuYzjttMMoHeXA0qMK_3btO0qxWre2mvCeH2IqT8eaUShfSV2X8jkUbbnDc5QkcRriCA-WSgVrtorQJqC0_RqCwkXJI3V3gRl2904-bEkbm6si6zQBDoMfPU0rtA6awI_2yhdS09_u2Iq-iVq:; shopify_recently_viewed=8122-2%206865-7%206957-7%20garantia%206865-6%20gs1019-20s%20gs1019-23s%20gs1019-25s%206865-1%206865-0; swym-v-ckd=1; swym-o_s={"wishlist-app_app-embed_170079715521":"2025-10-10T04:08:48.335Z","mktenabled":false}; _shopify_s=e56bf988-a6ab-4692-9f51-503af5fb717f; swym-nf_svd=1; keep_alive=eyJ2IjoyLCJ0cyI6MTc2MDA2OTYwNTAwNiwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjoxNCwiY2EiOjAsImthIjowLCJzYSI6MCwia2JhIjowLCJ0YSI6MCwidCI6NDEsIm5tIjoxLCJtcyI6MC4zOCwibWoiOjAuNzIsIm1zcCI6MC43NywidmMiOjAsImNwIjowLCJyYyI6MCwia2oiOjAsImtpIjowLCJzcyI6MCwic2oiOjAsInNzbSI6MCwic3AiOjAsInRzIjowLCJ0aiI6MCwidHAiOjAsInRzbSI6MH0sInNlcyI6eyJwIjozMywicyI6MTc1OTc1OTQ4ODE0NiwiZCI6MzA4MzEzfX0%3D',
}

params = {
    'filter.p.m.product.genero': 'women',
    'page': '2',
    # 'sort_by': 'best-selling',
}

response = requests.get('https://offview.com/en-uk/collections/gigi-studios-all', params=params, cookies=cookies, headers=headers)


print(response.status_code)
print(response.text)

with open('./uk_scr_offview/tests/request_gender_test_1.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
