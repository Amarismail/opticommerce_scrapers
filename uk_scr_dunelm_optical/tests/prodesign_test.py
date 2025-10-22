from bs4 import BeautifulSoup

html_content = '''
<div class="specs__container">
    <span class="specs--label">Name</span>
    <span class="specs--value">cleo 1</span>
</div>
'''

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the text of the span with class "specs--value"
spec_value = soup.select_one('.specs__container').text
print('\n' in spec_value)
print(spec_value)  # Output: cleo 1
