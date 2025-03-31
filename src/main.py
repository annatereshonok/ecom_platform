from typing import List, Union


class Product:
    """
    Класс для представления товара.

    Атрибуты:
    name (str): Название товара.
    description (str): Описание товара.
    price (Union[int, float]): Цена товара. Не может быть отрицательной.
    quantity (int): Количество товара на складе. Не может быть отрицательным.
    """
    name: str
    description: str
    price: Union[int, float]
    quantity: int

    def __init__(self, name, description, price, quantity):
        """
        Инициализирует объект товара.

        Аргументы:
        name (str): Название товара.
        description (str): Описание товара.
        price (Union[int, float]): Цена товара.
        quantity (int): Количество товара.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")


class Category:
    """
    Класс для представления категории товаров.

    Атрибуты:
    name (str): Название категории.
    description (str): Описание категории.
    products (List[Product]): Список товаров, относящихся к категории.
    category_count (int): Количество созданных категорий. Автоматически увеличивается при добавлении новой категории.
    products_count (int): Общее количество товаров во всех категориях. Автоматически обновляется при добавлении новой категории.
    """
    name: str
    description: str
    products: List[Product]
    category_count: int = 0
    products_count: int = 0

    def __init__(self, name, description, products):
        """
        Инициализирует объект категории и обновляет статистику по категориям и товарам.

        Аргументы:
        name (str): Название категории.
        description (str): Описание категории.
        products (List[Product]): Список продуктов, относящихся к категории.
        """
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.products_count += len(self.products)
