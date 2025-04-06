from pytest import fixture

from src.main import Category, Product


@fixture
def product_fixture():
    product_list = [
        {
            "name": "Samsung Galaxy C23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        },
        {"name": "Iphone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
        {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14},
    ]
    return product_list


@fixture(
    params=[
        (
            {"name": "Xiaomi Redmi", "description": "Красный", "price": -100, "quantity": 14},
            "Price cannot be negative",
        ),
        (
            {"name": "Xiaomi Redmi", "description": "Красный", "price": 31000, "quantity": -14},
            "Quantity cannot be negative",
        ),
    ]
)
def product_fixture_negative(request):
    return request.param


@fixture(params=[0, 1, 2])
def product_fixture_positive(request, product_fixture):
    data = []
    for product in product_fixture:
        data.append(
            (Product(**product), product["name"], product["description"], product["price"], product["quantity"])
        )
    return data[request.param]


@fixture
def category_fixture():
    category_list = [
        {
            "name": "Смартфоны",
            "description": """Смартфоны, как средство не только коммуникации,
            но и получение дополнительных функций для удобства жизни""",
            "products": [
                {
                    "name": "Samsung Galaxy C23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5,
                },
                {"name": "Iphone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
                {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14},
            ],
        },
        {
            "name": "Телевизоры",
            "description": """Современный телевизор, который позволяет наслаждаться просмотром,
            станет вашим другом и помощником""",
            "products": [
                {"name": '55" QLED 4K', "description": "Фоновая подсветка", "price": 123000.0, "quantity": 7}
            ],
        },
    ]
    return category_list


@fixture(params=[0, 1], autouse=True)
def category_fixture_positive(request, category_fixture):
    Category.category_count = 0
    Category.product_count = 0

    data = []
    for ind, category_dict in enumerate(category_fixture, start=1):
        original_name = category_dict["name"]
        original_description = category_dict["description"]
        original_product_count = len(category_dict["products"])

        product_list = [Product(**product) for product in category_dict["products"]]
        category_dict["products"] = product_list

        data.append((category_dict, original_name, original_description, original_product_count, 1))

    return data[request.param]


@fixture
def sample_product():
    return Product("Iphone 15", "512GB, Gray space", 210000, 5)


@fixture
def another_product():
    return Product("Samsung Galaxy", "256GB, Black", 180000, 3)


@fixture
def product_list(sample_product, another_product):
    return [sample_product, another_product]


@fixture
def one_category_fixture(product_list):
    return Category("Электроника", "Описание электроники", product_list)


@fixture(params=[0, 1])
def product_str_fixture(request, product_list):
    data = [
        (product_list[0], "Iphone 15, 210000 руб. Остаток: 5 шт."),
        (product_list[1], "Samsung Galaxy, 180000 руб. Остаток: 3 шт."),
    ]
    return data[request.param]
