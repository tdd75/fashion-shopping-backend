a = {
    'id': '8RX00047W09047911',
    'status': 'COMPLETED',
    'payment_source': {
        'paypal': {
            'email_address': 'sb-i7rth14170242@personal.example.com',
            'account_id': '98E2CY9K9K936',
            'name': {'given_name': 'John', 'surname': 'Doe'},
            'address': {'country_code': 'US'}
        }
    }, 'purchase_units': [
        {'reference_id': '294375635',
         'payments': {
             'captures': [
                 {'id': '58K33461PG121092N', 'status': 'COMPLETED', 'amount': {'currency_code': 'USD', 'value': '1.00'}, 'final_capture': True, 'seller_protection': {'status': 'ELIGIBLE', 'dispute_categories': ['ITEM_NOT_RECEIVED', 'UNAUTHORIZED_TRANSACTION']}, 'seller_receivable_breakdown': {'gross_amount': {'currency_code': 'USD', 'value': '1.00'}, 'paypal_fee': {'currency_code': 'USD', 'value': '0.52'}, 'net_amount': {'currency_code': 'USD', 'value': '0.48'}}, 'links': [
                     {
                         'href': 'https://api.sandbox.paypal.com/v2/payments/captures/58K33461PG121092N',
                         'rel': 'self', 'method': 'GET'
                     },
                     {'href': 'https://api.sandbox.paypal.com/v2/payments/captures/58K33461PG121092N/refund',
                      'rel': 'refund', 'method': 'POST'
                      },
                     {
                         'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/8RX00047W09047911', 'rel': 'up', 'method': 'GET'
                     }
                 ], 'create_time': '2023-02-06T15:44:47Z', 'update_time': '2023-02-06T15:44:47Z'}
             ]
         }
         }], 'payer': {'name': {'given_name': 'John', 'surname': 'Doe'}, 'email_address': 'sb-i7rth14170242@personal.example.com', 'payer_id': '98E2CY9K9K936', 'address': {'country_code': 'US'}}, 'links': [{'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/8RX00047W09047911', 'rel': 'self', 'method': 'GET'}
                                                                                                                                                                                                              ]
}
