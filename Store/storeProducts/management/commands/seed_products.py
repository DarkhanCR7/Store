from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed sample products into the database'

    def handle(self, *args, **options):
        from storeProducts.models import Product

        samples = [
            {
                'name': 'Красивый стул',
                'description': 'Удобный и стильный стул для дома и офиса.',
                'price': '12500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Chair',
            },
            {
                'name': 'Компактный стол',
                'description': 'Маленький стол для работы и хобби.',
                'price': '18500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Table',
            },
            {
                'name': 'Настольная лампа',
                'description': 'Регулируемая лампа с мягким светом.',
                'price': '4500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Lamp',
            },
        ]

        created = 0
        for s in samples:
            obj, _ = Product.objects.get_or_create(name=s['name'], defaults=s)
            if _:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Products ensured. Created: {created}'))
