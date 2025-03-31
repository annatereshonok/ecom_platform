from typing import Any, Dict, Hashable, List, Union


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
        self.__price = price
        self.quantity = quantity

        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            confirm = (
                input(f"Вы уверены, что х" f"отите снизить цену с {self.__price} до {new_price}? (y/n): ")
                .strip()
                .lower()
            )
            if confirm == "y":
                self.__price = new_price
                print("Цена изменена.")
            else:
                print("Изменение цены отменено.")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_dict: Dict[Hashable, Any], products_list: List = None):
        """Создаёт новый объект Product из словаря"""
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
    products_count (int): Общее количество товаров во всех категориях. Автоматически обновляется при добавлении новой категории.
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

    @property
    def products(self):
        products = [
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products
        ]
        return "\n".join(products)

    def add_product(self, product: Product):
        self.__products.append(product)
        Category.product_count += 1


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.products)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(category1.product_count)

    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)
