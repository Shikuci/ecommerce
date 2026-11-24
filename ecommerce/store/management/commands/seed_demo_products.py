from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from store.models import Category, Product


PRODUCTS = [
    ('Electronics', 'electronics', 'Wireless Earbuds', 'wireless-earbuds', 'Compact Bluetooth earbuds with a charging case.', 129000, 24, 'catalog/headphones.jpg'),
    ('Electronics', 'electronics', 'Portable Bluetooth Speaker', 'portable-bluetooth-speaker', 'Portable speaker for music at home or on the go.', 99000, 18, 'catalog/speaker.jpg'),
    ('Electronics', 'electronics', 'HD Webcam', 'hd-webcam', 'USB webcam for calls, classes, and streaming.', 78000, 15, 'catalog/camera.jpg'),
    ('Electronics', 'electronics', 'Portable SSD 1TB', 'portable-ssd-1tb', 'Fast external storage for files and photos.', 179000, 12, 'catalog/laptop.jpg'),
    ('Electronics', 'electronics', 'USB-C Multiport Hub', 'usb-c-multiport-hub', 'Compact hub with extra ports for a laptop.', 69000, 30, 'catalog/keyboard.jpg'),
    ('Accessories', 'accessories', 'Everyday Backpack', 'everyday-backpack', 'Roomy everyday backpack with padded laptop storage.', 145000, 13, 'catalog/backpack.jpg'),
    ('Accessories', 'accessories', 'Classic Wallet', 'classic-wallet', 'Simple compact wallet for cards and cash.', 49000, 25, 'catalog/wallet.jpg'),
    ('Accessories', 'accessories', 'Polarized Sunglasses', 'polarized-sunglasses', 'Lightweight sunglasses for everyday outdoor use.', 69000, 20, 'catalog/sunglasses.jpg'),
    ('Accessories', 'accessories', 'Wireless Charging Pad', 'wireless-charging-pad', 'Minimal charging pad for compatible devices.', 45000, 32, 'catalog/wireless-charger.svg'),
    ('Fashion', 'fashion', 'Cotton T-Shirt', 'cotton-t-shirt', 'Soft cotton everyday T-shirt.', 39000, 40, 'catalog/tshirt.jpg'),
    ('Fashion', 'fashion', 'Lightweight Hoodie', 'lightweight-hoodie', 'Comfortable layer for cool days.', 89000, 22, 'catalog/hoodie.jpg'),
    ('Fashion', 'fashion', 'Running Sneakers', 'running-sneakers', 'Everyday running shoes with a cushioned sole.', 129000, 16, 'catalog/sneakers.jpg'),
    ('Fashion', 'fashion', 'Denim Jacket', 'denim-jacket', 'Classic denim jacket for casual outfits.', 189000, 9, 'catalog/jacket.jpg'),
    ('Fashion', 'fashion', 'Summer Dress', 'summer-dress', 'Lightweight casual dress for warm weather.', 99000, 17, 'catalog/dress.jpg'),
    ('Fashion', 'fashion', 'Knit Sweater', 'knit-sweater', 'Warm knit sweater with a relaxed fit.', 119000, 11, 'catalog/sweater.jpg'),
    ('Home Appliances', 'home-appliances', 'Coffee Maker', 'coffee-maker', 'Countertop coffee maker for your morning brew.', 160000, 8, 'catalog/coffee-maker.jpg'),
    ('Home Appliances', 'home-appliances', 'Adjustable Desk Lamp', 'adjustable-desk-lamp', 'Focused light for a desk or reading corner.', 45000, 21, 'catalog/lamp.jpg'),
    ('Home Appliances', 'home-appliances', 'Electric Kettle', 'electric-kettle', 'Quick-boil kettle with a clean, simple design.', 79000, 14, 'catalog/electric-kettle.svg'),
    ('Home Appliances', 'home-appliances', 'Compact Air Purifier', 'compact-air-purifier', 'Small-room air purifier with a compact footprint.', 329000, 6, 'catalog/air-purifier.jpg'),
    ('Home Appliances', 'home-appliances', 'Personal Blender', 'personal-blender', 'Single-serve blender for smoothies and shakes.', 119000, 10, 'catalog/blender.jpg'),
    ('Home Appliances', 'home-appliances', 'Digital Kitchen Scale', 'digital-kitchen-scale', 'Small digital scale for everyday cooking.', 39000, 28, 'catalog/kitchen-scale.svg'),
    ('Sports', 'sports', 'Non-Slip Yoga Mat', 'non-slip-yoga-mat', 'Comfortable mat for stretching and floor exercises.', 45000, 26, 'catalog/yoga-mat.svg'),
    ('Sports', 'sports', 'Adjustable Dumbbell Set', 'adjustable-dumbbell-set', 'Space-saving weights for home workouts.', 169000, 7, 'catalog/dumbbells.jpg'),
    ('Sports', 'sports', 'Insulated Water Bottle', 'insulated-water-bottle', 'Reusable bottle for workouts and daily use.', 19000, 35, 'catalog/bottle.jpg'),
    ('Sports', 'sports', 'Training Football', 'training-football', 'Durable ball for practice and recreational play.', 79000, 19, 'catalog/football.jpg'),
    ('Sports', 'sports', 'Lightweight Running Jacket', 'lightweight-running-jacket', 'Breathable outer layer for outdoor runs.', 119000, 12, 'catalog/running-jacket.svg'),
    ('Sports', 'sports', 'Resistance Band Set', 'resistance-band-set', 'Set of bands for strength and mobility training.', 38000, 27, 'catalog/resistance-bands.svg'),
    ('Accessories', 'accessories', 'Canvas Tote Bag', 'canvas-tote-bag', 'Reusable canvas bag for daily errands.', 59000, 23, 'catalog/tote-bag.svg'),
]


class Command(BaseCommand):
    help = 'Add an idempotent demo catalog with locally stored product photos.'

    def handle(self, *args, **options):
        created = 0
        for category_name, category_slug, name, slug, description, price, stock, image_name in PRODUCTS:
            image_path = Path(settings.MEDIA_ROOT) / 'photos' / 'products' / image_name
            if not image_path.is_file():
                raise CommandError(f'Missing product image: {image_path}')

            category, _ = Category.objects.get_or_create(
                category_name=category_name,
                defaults={'slug': category_slug},
            )
            _, was_created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'product_name': name,
                    'description': description,
                    'price': price,
                    'stock': stock,
                    'images': f'photos/products/{image_name}',
                    'is_available': True,
                    'category': category,
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f'Added {created} sample products. Catalog total: {Product.objects.count()}.'
        ))
