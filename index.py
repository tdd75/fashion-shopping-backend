import os
import base64
import requests


# client_id = 'ASTUgwI8kOAVPRReztSOFgbILE_oiIuzXvyjF8XL5t0Daq9WWgsjdrHuxIf3rG_UxJJdmn5W-AmSXvqW'
# client_secret = 'EF392bt5eqPpj0BZ8hedq5kIKjQow6XMb9lktY5jIO4vQPf-49ChThmYORDCKvrULjOieJOdpNH1zqd8'
# if not client_id or not client_secret:
#     raise Exception('Error when load paypal keys')

# url = "https://api.sandbox.paypal.com/v1/oauth2/token"
# data = {
#     "client_id": os.getenv('PAYPAL_CLIENT_ID'),
#     "client_secret": os.getenv('PAYPAL_CLIENT_SECRET'),
#     "grant_type": "client_credentials"
# }
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Authorization": "Basic {0}".format(base64.b64encode((client_id + ":" + client_secret).encode()).decode())
# }
# token = requests.post(url, data, headers=headers)
# print(token.json()['access_token'])


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + 'A21AALVc6DZtIYroJsnxE4UqQig-kz8ZecZ1dcU8VmoRNoKjQPVh138OTUkoWSPjZQK6gsvKovF9NQ7wGPaIDf3BrbTYJQKOQ',
}
json_data = {
    "intent": "CAPTURE",
    "application_context": {
        "brand_name": "Fashion Shopping",
        "landing_page": "BILLING",
        "shipping_preference": "NO_SHIPPING",
        "user_action": "PAY_NOW"
    },
    "purchase_units": [
        {
            "reference_id": "294375635",
            "description": "African Art and Collectibles",
            "soft_descriptor": "AfricanFashions",
            "amount": {
                "currency_code": "USD",
                "value": "1"
            },
        },
        {
            "reference_id": "2131",
            "description": "African Art and Collectibles",
            "soft_descriptor": "AfricanFashions",
            "amount": {
                "currency_code": "USD",
                "value": "1"
            },
        }
    ]
}
response = requests.post(
    'https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=json_data)
print(response)
order_id = response.json()['id']
linkForPayment = response.json()['links'][1]['href']
print(response.json())
# response = requests.post(
#     'https://api.sandbox.paypal.com/v2/checkout/orders/8RX00047W09047911/capture', headers=headers)
# print(response.json())
