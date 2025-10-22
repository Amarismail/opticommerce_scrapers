url_list = ['https://woodyseyewear.com/128920-home_default/tolix.jpg', 'https://woodyseyewear.com/128916-home_default/tolix.jpg', 'https://woodyseyewear.com/128925-home_default/tolix.jpg', 'https://woodyseyewear.com/128911-home_default/tolix.jpg', 'https://woodyseyewear.com/128920-home_default/tolix.jpg']
size_list = ['<span class="sr-only">02</span>', '<span class="sr-only">01</span>', '<span class="sr-only">03</span>', '<span class="sr-only">04</span>']


print(dict.fromkeys(url_list))

variant_info_tags_map = zip(url_list, size_list)

for url, size in variant_info_tags_map:
    print(url)
    print(size)
    print('--------------------')