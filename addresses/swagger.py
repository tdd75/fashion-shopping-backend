from drf_spectacular.utils import OpenApiExample

ADDRESS_EXAMPLES = [
    OpenApiExample(
        'Admin account',
        value={
            'full_name': 'Trần Đức Duy',
            'phone': '0834275110',
            'city': 'Hanoi',
            'district': 'Nam Tu Liem district',
            'ward': 'Trung Van ward',
            'street': 'Trung Van street',
            'detail': 'Lane Trung Van',
        },
    ),

]
