# # my_dict = {'Unisex': 'https://www.dunelmoptical.com', 'Male': 'https://www.dunelmoptical.com', 'Female': 'https://www.dunelmoptical.com', 'Kids': 'https://www.dunelmoptical.com'}

# # for key, value in reversed(list(my_dict.items())):
# #     print(key, value)



# import re

# # Example prices
# prices = ["£7,95", "7,95 £", "1,234.56 £", "€1.234,56"]

# for price_str in prices:
#     # Match currency and price, preserving commas in the price
#     match = re.match(r"([^\d\s,.\-]+)?\s*([\d,\.]+)\s*([^\d\s,.\-]+)?", price_str)
#     if match:
#         currency = (match.group(1) or match.group(3) or "").strip()
#         price = match.group(2)
#         print(f"Currency: {currency}")
#         print(f"Price: {price}")


# a_list = [2,4,6,8]

# for ele in a_list:
#     if ele % 2 == 0:
#         continue
#     print(ele)


print(isinstance('16', int))