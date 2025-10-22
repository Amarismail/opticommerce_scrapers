from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.dunelmoptical.com/")  # Replace with your target URL

    # Get cookies for the current page
    cookies = page.context.cookies()
    print("Cookies:", cookies)

    browser.close()
