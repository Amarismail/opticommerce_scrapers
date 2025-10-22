

def get_frame_size(json_obj, str_with_size, current_size):

    import re

    size_json_keys = ['$iLens_Size_w', '$iFrame_Bridge', '$iFrame_Temple']
    pattern = r'(\d{2})\s*[-–/¤]\s*(\d{2})(?:\s*[-–/¤]\s*(\d{3}))?'
    pattern = r'(\d{2})\s*/\s*\d{2}\.\d{2}\s*/\s*(\d{2})\s*/\s*(\d{3})'
    pattern = r'(\d{2})\s*[-–/¤]\s*(?:\d{2}\.\d{2}\s*/)?(\d{2})(?:\s*[-–/¤]\s*(\d{3}))?'
    pattern = r'(\d{2})\s*[-–/¤]\s*(?:\d{2}\.\d{2})?(?:\d{2})?\s*(?:[-–/¤])?\s*(\d{2})(?:\s*[-–/¤]\s*(\d{3}))?'
    pattern = r'(\d{2})\s*[-–/¤]\s*(\d{2}(?:\.\d{2})?)?\s*(?:[-–/¤])?\s*(\d{2})(?:\s*[-–/¤]\s*(\d{3}))?'
    matches = re.findall(pattern, str_with_size)
    print(matches)
    # for match in matches:
    #     for index, size_json_key in enumerate(size_json_keys):
    #         if json_obj[size_json_key] == '':
    #             json_obj[size_json_key] = match[index]

    #     if current_size and json_obj['$iLens_Size_w'] == current_size:
    #         break
        
    return json_obj

import re
str_with_size = re.sub(r"\s+", "", '53 / 47.60 /  20 / 135')
print(str_with_size)
get_frame_size({}, str_with_size, None)
str_with_size = re.sub(r"\s+", "", '53 / /  20 / 135')
print(str_with_size)
get_frame_size({}, str_with_size, None)

get_frame_size({}, '54/40/19/140', None)
get_frame_size({}, '53/20/135', None)
get_frame_size({}, '53-20', None)