
from django.core.files.base import File

import os
from urllib.parse import urljoin
from tqdm import tqdm
import random
import pandas as pd

from product_variants.models import ProductVariant
from products.models import Product
from product_categories.models import ProductCategory
from fashion_shopping_backend.celery import update_product_vector

style_df = pd.read_csv('api/management/commands/seeder/styles.csv', on_bad_lines='skip')

def create_product_categories():
    ProductCategory.objects.all().delete()
    categories = style_df['subCategory'].unique()
    for category in categories:
        ProductCategory.objects.create(name=category)


def create_products():
    create_product_categories()
    Product.objects.all().delete()

    data_path = 'api/management/commands/seeder/data/products/'

    for file_name in tqdm(os.listdir(data_path)[:]):
        matched_row = style_df[style_df['id'] == int(file_name.split('.')[0])].iloc[0]
        print(File(open(urljoin(data_path, file_name), 'rb'), name=file_name))
        product_dict = {
            'name': matched_row['productDisplayName'],
            'description': f'''
            {matched_row['productDisplayName']}.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam imperdiet tortor nec turpis aliquet vehicula. Nullam at volutpat metus, non efficitur turpis. Curabitur scelerisque quam a lectus volutpat, et aliquam neque condimentum. Maecenas eget scelerisque eros, eu vestibulum sapien. Ut quis lacus id arcu aliquam lobortis non ut justo. Nunc aliquam lorem non dictum congue. Ut cursus malesuada ipsum nec sollicitudin.
            Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec a condimentum quam. Aenean quis tristique erat. Pellentesque blandit diam vel magna eleifend scelerisque. Fusce molestie ultrices libero nec bibendum. Fusce semper justo sit amet arcu lacinia egestas eget quis eros. Duis egestas arcu sed magna aliquet posuere. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur elementum lobortis vulputate. Quisque in ante blandit, tempus magna ut, luctus nulla.
            Quisque mollis purus non urna aliquam dictum. Pellentesque maximus ultrices diam eu luctus. Etiam vel euismod velit, vitae eleifend elit. Donec bibendum ut elit imperdiet convallis. Mauris pharetra tempus blandit. Aenean bibendum at augue eu rutrum. Praesent a sollicitudin justo, eget malesuada neque. Aenean quis rutrum neque, vel fermentum quam. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer convallis feugiat diam eu sodales. Nam pharetra non risus at pulvinar. Cras quis lacus vitae tellus porttitor viverra.
            Phasellus tortor enim, sollicitudin molestie arcu in, scelerisque commodo ante. Maecenas quis dapibus sapien. Nunc ornare nulla sed ex molestie convallis eget interdum libero. Ut ornare urna quis varius iaculis. Donec quis eros faucibus, consectetur urna vitae, rhoncus purus. Quisque ac lacus ultricies, feugiat ante vel, suscipit mi. Etiam suscipit eu ipsum eget accumsan. Duis ultrices nulla sit amet dui congue, et scelerisque mi vestibulum. Phasellus congue est a tortor lacinia, nec vehicula ex vulputate. Praesent nec sem mauris. Vivamus sit amet leo eget lacus suscipit accumsan sit amet ut diam.
            Aenean laoreet massa eu condimentum pulvinar.
            ''',
            'image': File(open(urljoin(data_path, file_name), 'rb'), name=file_name),
            'category': ProductCategory.objects.filter(name=matched_row['subCategory']).first(),
        }

        created_product = Product.objects.create(**product_dict)
        product_variant_dict = {
            'color': matched_row['baseColour'],
            'size': random.choice(['XS', 'S', 'M', 'L', 'XL', 'XXL']),
            'stocks': random.randint(0, 100),
            'price': random.randint(400, 40000) / 100,
            'product_id': created_product.id,
        }
        ProductVariant.objects.create(**product_variant_dict)

    update_product_vector()
    update_product_vector()