from lxml import html
from bs4 import BeautifulSoup

# Sample HTML
html_content = """
<div class="product__media-item"><img src="image1.jpg"></div>
<div class="product__media-item"><img src="image2.jpg"></div>
"""

in_page = BeautifulSoup(html_content, 'lxml')
# print(in_page.find_all("(//div[contains(@class, 'product__media-item')][2]//img[@src] | //div[contains(@class, 'product__media-item')][1]//img[@src])[1]"))
# Parse the HTML content with lxml's html module
# tree = html.fromstring(html_content)
tree = html.fromstring(str(in_page.prettify()))

# Use XPath to select the second child if it exists, otherwise the first child
img_element = tree.xpath(
    "(//div[contains(@class, 'product__media-item')][1]//img[@src] | //div[contains(@class, 'product__media-item')][2]//img[@src])"
)

# Output the src attribute of the found img element if it exists
if img_element:
    print(img_element[0].get("src"))
