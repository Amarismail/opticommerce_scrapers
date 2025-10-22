import constants
import base_json

data_dir_path = r'C:\Users\Ammar Ismail\Desktop\main\opticommerce\data'
base_json.base_json_format[0]["$iSupplier"] = constants.website_name
base_json.base_json_format[0]["$iBrandURL"] = constants.website_url
base_json.base_json_format[0]["$iCountry"] = constants.country
base_json_format = base_json.base_json_format
unique_prod_key = '$iModelURL'

prod_materials = {'Titanium' : 'Titanium', 'Stainless Steel' : 'Matel', 'Acetate' : 'Acetate'}
prod_types = {'clip-on': 'Clip-on', 'sun': 'Sun'}
key_words = {'RX- able': ['$iFrame_Rx_Able'], 'Polarized': ['$iPolarized', '$iLens_Properties']}