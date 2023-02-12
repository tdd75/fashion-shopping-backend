import base64

def convert_to_base64(image_field_file):
    with open(image_field_file.path, 'rb') as f:
        encoded_string = base64.b64encode(f.read()).decode('utf-8')
    return encoded_string