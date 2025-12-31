from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed sample products into the database'

    def handle(self, *args, **options):
        from storeProducts.models import Product

        samples = [
            {
                'name': 'Красивый стул',
                'description': 'Удобный и стильный стул для дома и офиса. Эргономичный дизайн.',
                'price': '12500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Chair&bg=4CAF50&text_color=fff',
            },
            {
                'name': 'Компактный стол',
                'description': 'Маленький стол для работы и хобби. Идеален для небольших помещений.',
                'price': '18500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Table&bg=2196F3&text_color=fff',
            },
            {
                'name': 'Настольная лампа',
                'description': 'Регулируемая лампа с мягким светом. Экономит электроэнергию.',
                'price': '4500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Lamp&bg=FF9800&text_color=fff',
            },
            {
                'name': 'Офисный шкаф',
                'description': 'Просторный шкаф для хранения документов и предметов.',
                'price': '25000.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Cabinet&bg=9C27B0&text_color=fff',
            },
            {
                'name': 'Компьютерный стол',
                'description': 'Специализированный стол для работы с компьютером.',
                'price': '22000.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Desk&bg=F44336&text_color=fff',
            },
            {
                'name': 'Кресло для офиса',
                'description': 'Удобное вращающееся кресло с подлокотниками.',
                'price': '15000.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Office+Chair&bg=00BCD4&text_color=fff',
            },
            {
                'name': 'Книжная полка',
                'description': 'Модульная полка для книг и декоративных предметов.',
                'price': '8500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Shelf&bg=673AB7&text_color=fff',
            },
            {
                'name': 'Прикроватная тумба',
                'description': 'Компактная тумба с выдвижными ящиками.',
                'price': '7500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Nightstand&bg=E91E63&text_color=fff',
            },
            {
                'name': 'Настенное зеркало',
                'description': 'Большое зеркало с красивой рамой для комнаты.',
                'price': '6500.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Mirror&bg=3F51B5&text_color=fff',
            },
            {
                'name': 'Диван',
                'description': 'Мягкий и просторный диван для гостиной.',
                'price': '35000.00',
                'image_url': 'https://via.placeholder.com/600x400?text=Sofa&bg=009688&text_color=fff',
            },
        ]

        created = 0
        for s in samples:
            obj, _ = Product.objects.get_or_create(name=s['name'], defaults=s)
            if _:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Products ensured. Created: {created}'))
