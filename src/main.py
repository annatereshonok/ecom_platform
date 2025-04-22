from abc import ABC
from typing import Dict, Hashable, List, Union


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.

    Атрибуты:
    name (str): Название товара.
    description (str): Описание товара.
    quantity (int): Количество на складе.
    _price (Union[int, float]): Приватная цена товара.
    """

    name: str
    description: str
    quantity: int
    _price: Union[int, float]

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

    @property
    def price(self) -> Union[int, float]:
        return self._price

    @price.setter
    def price(self, new_price: Union[int, float]):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self._price:
            confirm = (
                input(f"Вы уверены, что хотите снизить цену с {self._price} до {new_price}? (y/n): ").strip().lower()
            )
            if confirm == "y":
                self._price = new_price
                print("Цена изменена.")
            else:
                print("Изменение цены отменено.")
        else:
            self._price = new_price


class MixinLog:
    def __init__(self, *args, **kwargs):
        print(f"[LOG] Создан объект класса {self.__class__.__name__} с аргументами: {args}, {kwargs}")
        super().__init__(*args, **kwargs)


class Product(MixinLog, BaseProduct):
    """
    Конкретный продукт. Расширяет базовый функционал.
    """

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError(
                "Продукты должны быть из одного класса. "
                f"Нельзя складывать {type(self).__name__} и {type(other).__name__}"
            )
        return self.quantity * self.price + other.quantity * other.price

    @classmethod
    def new_product(cls, product_dict: Dict[Hashable, Union[str, int, float]], products_list: List = None):
        product = cls(
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            quantity=product_dict["quantity"],
        )
        if products_list:
            for item in products_list:
                if product.name == item.name:
                    product.quantity += item.quantity
                    product.price = max(product.price, item.price)
        return product


class Category:
    """
    Класс для представления категории товаров.

    Атрибуты:
    name (str): Название категории.
    description (str): Описание категории.
    products (List[Product]): Список товаров, относящихся к категории.
    category_count (int): Количество созданных категорий. Автоматически увеличивается при добавлении новой категории.
    products_count (int): Общее количество товаров во всех категориях.
    Автоматически обновляется при добавлении новой категории.
    """

    name: str
    description: str
    products: List[Product]
    category_count: int = 0
    product_count: int = 0

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
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self):
        products_sum = 0
        for product in self.__products:
            products_sum += product.quantity
        return f"{self.name}, количество продуктов: {products_sum} шт."

    @property
    def products(self):
        return "\n".join([str(product) for product in self.__products])

    @property
    def product_list(self):
        return self.__products

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты Product или его наследников, а не {type(product).__name__}"
            )
        self.__products.append(product)
        Category.product_count += 1


class CategoryIterator:
    def __init__(self, category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._category.product_list):
            product = self._category.product_list[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration


class Smartphone(Product):
    """
    Класс для представления смартфона как продукта.

    Наследует все атрибуты базового класса Product и добавляет специфичные для смартфонов поля:
    model (str): Модель смартфона.
    memory (int): Объём памяти в гигабайтах.
    color (str): Цвет устройства.
    efficiency (float): Энергоэффективность устройства.

    Используется для описания и хранения характеристик смартфонов в системе товаров.
    """

    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(self, name, description, price, quantity, model, memory, color, efficiency):
        super().__init__(name, description, price, quantity)
        self.model = model
        self.memory = memory
        self.color = color
        self.efficiency = efficiency


class LawnGrass(Product):
    """
    Класс для представления газонной травы как продукта.

    Наследует все атрибуты базового класса Product и добавляет уникальные поля:
    country (str): Страна-производитель.
    germination_period (float): Период прорастания в днях.
    color (str): Цвет травы.

    Используется для описания семян газонной травы в системе товаров.
    """

    country: str
    germination_period: float
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


# if __name__ == "__main__":
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     print(product1.name)
#     print(product1.description)
#     print(product1.price)
#     print(product1.quantity)
#
#     print(product2.name)
#     print(product2.description)
#     print(product2.price)
#     print(product2.quantity)
#
#     print(product3.name)
#     print(product3.description)
#     print(product3.price)
#     print(product3.quantity)
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3],
#     )
#
#     print(category1.name == "Смартфоны")
#     print(category1.description)
#     print(len(category1.products))
#     print(category1.category_count)
#     print(category1.product_count)
#
#     product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
#     category2 = Category(
#         "Телевизоры",
#         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
#         [product4],
#     )
#
#     print(category2.name)
#     print(category2.description)
#     print(len(category2.products))
#     print(category2.products)
#
#     print(Category.category_count)
#     print(Category.product_count)
