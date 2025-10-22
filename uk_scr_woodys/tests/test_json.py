


# a_dict = [{'abc': {'efg': 123}}]

# a_var = 'abc'

# print(a_dict[0][a_var])

import re
from lxml import etree

variant_url = "https://woodyseyewear.com/125810-home_default/verne.jpg"
pattern = r'(https://woodyseyewear\.com/)(\d+)-home_default(/.+)'
match = re.match(pattern, variant_url)
if match:
    base = match.group(1)
    number = int(match.group(2)) + 1
    rest = match.group(3)
    new_url = f"{base}{number}{rest}"
    print(new_url)