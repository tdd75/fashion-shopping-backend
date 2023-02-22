
from django.core.files.base import File

import os
from urllib.parse import urljoin
from tqdm import tqdm
import random

from product_variants.models import ProductVariant
from products.models import Product
from product_categories.models import ProductCategory
from fashion_shopping_backend.celery import update_product_vector


def create_product_categories():
    ProductCategory.objects.all().delete()

    categories = ['Topwear', 'Bottomwear', 'Watches', 'Socks', 'Shoes', 'Belts', 'Flip Flops',
                  'Bags', 'Innerwear', 'Sandal', 'Shoe Accessories', 'Fragrance', 'Jewellery',
                  'Lips', 'Saree', 'Eyewear', 'Nails', 'Scarves', 'Dress',
                  'Loungewear and Nightwear', 'Wallets', 'Apparel Set', 'Headwear', 'Mufflers',
                  'Skin Care', 'Makeup', 'Free Gifts', 'Ties', 'Accessories', 'Skin',
                  'Beauty Accessories', 'Water Bottle', 'Eyes', 'Bath and Body', 'Gloves',
                  'Sports Accessories', 'Cufflinks', 'Sports Equipment', 'Stoles', 'Hair',
                  'Perfumes', 'Home Furnishing', 'Umbrellas', 'Wristbands', 'Vouchers']
    for category in categories:
        ProductCategory.objects.create(name=category)


def create_products():
    create_product_categories()
    category_ids = ProductCategory.objects.values_list('id', flat=True)
    Product.objects.all().delete()

    NUM_PRODUCT = 2000
    data_path = 'api/management/commands/seeder/data/products/'

    for file_name in tqdm(os.listdir(data_path)[:NUM_PRODUCT]):
        product_dict = {
            'name': 'Product ' + file_name.split(".")[0],
            'description': '''
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam imperdiet tortor nec turpis aliquet vehicula. Nullam at volutpat metus, non efficitur turpis. Curabitur scelerisque quam a lectus volutpat, et aliquam neque condimentum. Maecenas eget scelerisque eros, eu vestibulum sapien. Ut quis lacus id arcu aliquam lobortis non ut justo. Nunc aliquam lorem non dictum congue. Ut cursus malesuada ipsum nec sollicitudin.

                Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec a condimentum quam. Aenean quis tristique erat. Pellentesque blandit diam vel magna eleifend scelerisque. Fusce molestie ultrices libero nec bibendum. Fusce semper justo sit amet arcu lacinia egestas eget quis eros. Duis egestas arcu sed magna aliquet posuere. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur elementum lobortis vulputate. Quisque in ante blandit, tempus magna ut, luctus nulla.

                Quisque mollis purus non urna aliquam dictum. Pellentesque maximus ultrices diam eu luctus. Etiam vel euismod velit, vitae eleifend elit. Donec bibendum ut elit imperdiet convallis. Mauris pharetra tempus blandit. Aenean bibendum at augue eu rutrum. Praesent a sollicitudin justo, eget malesuada neque. Aenean quis rutrum neque, vel fermentum quam. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer convallis feugiat diam eu sodales. Nam pharetra non risus at pulvinar. Cras quis lacus vitae tellus porttitor viverra.

                Phasellus tortor enim, sollicitudin molestie arcu in, scelerisque commodo ante. Maecenas quis dapibus sapien. Nunc ornare nulla sed ex molestie convallis eget interdum libero. Ut ornare urna quis varius iaculis. Donec quis eros faucibus, consectetur urna vitae, rhoncus purus. Quisque ac lacus ultricies, feugiat ante vel, suscipit mi. Etiam suscipit eu ipsum eget accumsan. Duis ultrices nulla sit amet dui congue, et scelerisque mi vestibulum. Phasellus congue est a tortor lacinia, nec vehicula ex vulputate. Praesent nec sem mauris. Vivamus sit amet leo eget lacus suscipit accumsan sit amet ut diam.

                Aenean laoreet massa eu condimentum pulvinar. Quisque ac purus orci. Nunc gravida leo arcu, sed pulvinar massa commodo nec. Phasellus congue est hendrerit orci porttitor, vel sodales neque tristique. Cras quis sodales sapien, non pulvinar magna. Donec vitae arcu vitae diam auctor pulvinar vel id ipsum. Integer ut placerat ligula, non egestas risus. Sed non lacus semper, dignissim neque at, rutrum enim. Vivamus vel neque auctor neque ullamcorper suscipit. Proin vel tincidunt leo. Donec nisl nunc, venenatis in ex a, blandit congue ligula.

                In tincidunt nec magna vitae viverra. Duis pulvinar in risus id euismod. Quisque sagittis leo vel iaculis bibendum. Duis facilisis dictum est. Suspendisse potenti. Duis sollicitudin quam sed tortor tincidunt feugiat. Morbi semper, sapien nec lacinia maximus, orci sem venenatis ligula, non blandit neque lorem ac dolor. Duis tristique consectetur ultrices. Aenean ut mauris vel ante vestibulum aliquam. Phasellus placerat nunc sed metus luctus, at auctor mauris efficitur. Nam nec felis sollicitudin, interdum dolor vel, elementum turpis. Donec malesuada, ante eu iaculis dictum, lectus tortor cursus mauris, ut pharetra nisi magna sit amet odio. Vivamus sollicitudin placerat augue, ut accumsan tellus luctus in. Cras bibendum mi ac enim ultricies, vel gravida orci iaculis.

                Morbi quis vehicula felis. Quisque at ex lacinia nulla condimentum tempus. Suspendisse convallis malesuada purus, nec euismod orci eleifend auctor. Nam eget efficitur turpis. In cursus tincidunt enim, ut molestie ligula aliquet sed. Ut vestibulum sodales suscipit. Vestibulum ullamcorper enim vel pharetra viverra. Aenean a lobortis turpis. Sed sit amet convallis est. Donec lacinia porta dui et aliquet. Aenean consequat felis nec nibh sollicitudin molestie. Sed vel sem ultricies, congue tellus in, laoreet est.

                Donec venenatis sollicitudin placerat. Nulla eu velit ut nunc ultricies facilisis a in dolor. Etiam tristique a risus et pulvinar. Ut nec enim luctus, dictum metus id, commodo odio. Vivamus pretium purus eu dui euismod, vel auctor metus aliquam. Nunc in ante dolor. Aenean condimentum suscipit tristique. Morbi sit amet nunc ligula. Nullam ut ligula vitae sem vestibulum faucibus quis vel nisi. Quisque libero dui, blandit sit amet elit sit amet, mattis scelerisque mi. Aliquam ligula neque, scelerisque eu nulla quis, volutpat dignissim velit.

                Phasellus eget enim dui. Curabitur porta rhoncus tortor, nec feugiat velit sollicitudin sit amet. Donec ac purus eget tortor placerat dictum commodo non arcu. Integer at tortor nibh. Duis at ante ac justo volutpat auctor. Vestibulum eget condimentum nisi, ut venenatis elit. Integer venenatis nulla ante, nec molestie nulla semper in. Vestibulum luctus, augue molestie feugiat imperdiet, nulla risus bibendum nulla, at mattis ligula urna ac eros. Nunc augue turpis, placerat et odio ut, semper dapibus mi. Quisque eu mollis massa. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus venenatis elit mattis lacus dapibus, nec ullamcorper felis aliquet. Etiam fringilla libero eu arcu sagittis tempor. Pellentesque rhoncus magna eget ornare convallis.

                Donec eget tellus et odio varius euismod. Aliquam a volutpat elit. Vestibulum finibus risus et metus sollicitudin efficitur. Integer rhoncus risus id faucibus blandit. Curabitur venenatis, dui ac tempor lacinia, lorem nibh pellentesque enim, nec viverra metus urna sit amet arcu. Aenean sed turpis massa. Cras aliquam finibus metus ac tincidunt. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Quisque nibh quam, elementum porta pulvinar non, ornare vel velit. Aenean tincidunt commodo magna, vel suscipit magna ultricies eget. Sed orci elit, pulvinar interdum odio in, tincidunt vestibulum diam. Phasellus est nisl, sollicitudin quis nibh eget, aliquet ornare nunc. Donec et neque nec mauris posuere consequat id et ipsum. Cras congue tellus a sapien tincidunt, quis lobortis libero scelerisque.

                Donec vitae quam eget magna convallis aliquam. Nulla imperdiet felis sit amet massa gravida, at viverra arcu malesuada. Praesent ultricies scelerisque suscipit. Curabitur feugiat luctus lectus, quis ornare sem venenatis a. Nam blandit nisi a scelerisque tincidunt. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam condimentum cursus quam.

                Proin condimentum malesuada mauris quis posuere. Maecenas vel ante ac elit tincidunt hendrerit. In pretium vitae magna a porta. Mauris nec eros sit amet enim luctus eleifend. Aliquam pellentesque malesuada porta. Suspendisse vel augue urna. Cras hendrerit magna ac rhoncus blandit. Morbi eu suscipit sapien. Quisque.
            ''',
            'image': File(open(urljoin(data_path, file_name), "rb"), name=file_name),
            'category_id': random.choice(category_ids),
        }

        created_product = Product.objects.create(**product_dict)
        product_variant_dict = {
            'color': random.choice(['Red', 'Green', 'Blue', 'Yellow', 'Black', 'White', 'Orange', 'Purple']),
            'size': random.choice(['S', 'M', 'L', 'XL', 'XXL']),
            'stocks': random.randint(0, 100),
            'price': random.randint(150, 1000) / 100,
            'product_id': created_product.id,
        }
        ProductVariant.objects.create(**product_variant_dict)

    update_product_vector()
    update_product_vector()