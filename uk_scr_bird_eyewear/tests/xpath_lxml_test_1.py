from lxml import etree

# Sample HTML content
html_content = """
<div>
  <span>Highlighted Text 1</span>
</div>
<div class="highlight">
  <span>Highlighted Text 2</span>
</div>

"""
    # <li>Third item</li>

# Parse HTML content
tree = etree.HTML(html_content)

# Define XPath expression to select the second li if it exists, otherwise the first one
result = tree.xpath('//div[not(@class="highlight")]/span | //div[@class="highlight"]/span' )
print(result)

# Print result
if result:
    print("Selected li:", result[0].text)
else:
    print("No matching li found")
