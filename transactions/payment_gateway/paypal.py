import os
import base64
import requests


class PaypalPayment:
    def __init__(self) -> None:
        self.token = self.get_token()
        self.session = requests.session()
        # assign headers to session
        self.session.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

    def get_token(self):
        client_id = os.getenv('PAYPAL_CLIENT_ID')
        client_secret = os.getenv('PAYPAL_CLIENT_SECRET')
        if not client_id or not client_secret:
            raise Exception('Error when load paypal keys')

        url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic {0}'.format(base64.b64encode((client_id + ':' + client_secret).encode()).decode())
        }
        res = requests.post(url, data, headers=headers)
        if res.ok:
            return res.json()['access_token']

    def request_order(self, order_items):
        '''Create paypal order

        Args:
            order_items (
                List[dict]: [{
                    'reference_id': str,
                    'description': str,
                    'soft_descriptor': str,
                    'amount': {
                        'currency_code': str,
                        'value': str
                    },
                }]
            ): order item list

        Returns:
            dict: dict with `payment_link` and `check_payment_link`
        '''
        json_data = {
            'intent': 'CAPTURE',
            'application_context': {
                'brand_name': 'Fashion Shopping',
                'landing_page': 'BILLING',
                'shipping_preference': 'NO_SHIPPING',
                'user_action': 'PAY_NOW'
            },
            'purchase_units': order_items
        }
        res = self.session.post(
            'https://api-m.sandbox.paypal.com/v2/checkout/orders', json=json_data)
        if res.ok:
            order_data = res.json()
            return {
                'payment_link': order_data['links'][1]['href'],
                'check_payment_link': order_data['links'][3]['href'],
            }

    def check_order_completed(self, order_id):
        res = self.session.post(
            f'https://api.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture')
        if res.ok:
            return res.json().get('status') == 'COMPLETED'


paypal_payment = PaypalPayment()
