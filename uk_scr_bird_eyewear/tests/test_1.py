def normalize_url(website_url, url):

    from urllib.parse import urlparse, urlunparse

    parsed_prod_url = urlparse(url)
    parsed_website_url = urlparse(website_url)
    print(parsed_prod_url)

    # Ensure the URL has a scheme
    if not parsed_prod_url.scheme:
        scheme = parsed_website_url.scheme
        netloc = parsed_prod_url.netloc
        path = parsed_prod_url.path
        query = parsed_prod_url.query
        
    if not netloc:
        netloc = parsed_website_url.netloc
        if not netloc.startswith('www.'):
            netloc = 'www.' + netloc.lstrip('www.')
        # path = parsed_prod_url.path.rstrip('/')   # look for more example in future scrapers
    
    normalized_url = urlunparse((scheme, netloc, path, '', query, ''))
    print(normalized_url)

    return normalized_url


normalize_url('https://www.birdeyewear.co.uk', '/products/alba-black')