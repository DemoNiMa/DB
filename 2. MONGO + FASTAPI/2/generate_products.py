import random
from faker import Faker
import datetime

fake = Faker()

CATEGORIES = ["Электроника", "Одежда", "Косметика", "Игрушки"]

NAMES = [
    "Альфа", "Бета", "Гамма", "Дельта", "Эпсилон", "Зета", "Эта", "Тета", "Йота", "Каппа",
    "Лямбда", "Мю", "Ню", "Кси", "Омикрон", "Пи", "Ро", "Сигма", "Тау", "Упсилон",
    "Фи", "Хи", "Пси", "Омега", "Оникс", "Рубин", "Сапфир", "Топаз", "Кварц", "Опал",
    "Яшма", "Агат", "Берилл", "Жемчуг", "Корал", "Лазурит", "Малахит", "Янтарь", "Нефрит", "Турмалин"
]

def generate_random_product():
    """
    Генерирует случайный товар с характеристиками и покупателями.
    """
    product = {
        "name": random.choice(NAMES),
        "manufacturer": fake.company(),
        "price": round(random.uniform(10, 1000), 2),
        "category": random.choice(CATEGORIES),
        "characteristics": {
            "color": random.choice(["красный", "синий", "зеленый", "черный", "белый"]),
            "weight": round(random.uniform(0.1, 5), 2),
            "dimensions": f"{random.randint(10, 50)}x{random.randint(10, 50)}x{random.randint(10, 50)}",
            "material": random.choice(["пластик", "металл", "ткань", "дерево"]),
        },
        "buyers": [
            {
                "name": fake.name(),
                "purchase_date": fake.date_this_year().isoformat(),  # Преобразуем дату в строку
                "review": fake.sentence(),
                "delivery_service": random.choice(["DHL", "Boxberry", "Почта России"]),
            } for _ in range(random.randint(1, 5))
        ]
    }
    return product

def generate_products(count=20):
    """
    Генерирует указанное количество случайных товаров.
    :param count: Количество товаров для генерации.
    :return: Список товаров.
    """
    return [generate_random_product() for _ in range(count)]
