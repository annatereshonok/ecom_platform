import pytest

from src.main import Category, CategoryIterator, LawnGrass, Product, Smartphone


def test_product_positive(product_fixture_positive):
    product, prod_name, prod_desc, prod_price, prod_quantity = product_fixture_positive
    assert product.name == prod_name
    assert product.description == prod_desc
    assert product.price == prod_price
    assert product.quantity == prod_quantity


def test_category_positive(category_fixture_positive):
    category_data, cat_name, cat_desc, cat_num_prod, cat_num_cat = category_fixture_positive
    category = Category(**category_data)
    assert category.name == cat_name
    assert category.description == cat_desc
    assert Category.product_count == cat_num_prod
    assert Category.category_count == cat_num_cat


def test_price_getter(sample_product):
    assert sample_product.price == 210000


def test_price_setter(sample_product, monkeypatch):
    sample_product.price = 220000
    assert sample_product.price == 220000
    sample_product.price = -1000
    assert sample_product.price == 220000
    monkeypatch.setattr("builtins.input", lambda _: "y")
    sample_product.price = 200000
    assert sample_product.price == 200000
    monkeypatch.setattr("builtins.input", lambda _: "n")
    sample_product.price = 190000
    assert sample_product.price == 200000


def test_new_product_without_list():
    product_data = {
        "name": "Xiaomi Redmi",
        "description": "128GB, Blue",
        "price": 31000,
        "quantity": 10,
    }
    new_product = Product.new_product(product_data)
    assert new_product.name == "Xiaomi Redmi"
    assert new_product.price == 31000
    assert new_product.quantity == 10


def test_new_product_with_existing(product_list):
    duplicate_data = {
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 200000,
        "quantity": 3,
    }
    new_product = Product.new_product(duplicate_data, product_list)
    assert new_product.name == "Iphone 15"
    assert new_product.price == 210000
    assert new_product.quantity == 8


def test_category_add_product(category_fixture_positive):
    category_data, cat_name, cat_desc, cat_num_prod, cat_num_cat = category_fixture_positive
    new_product = Product("Товар 3", "Описание 3", 300, 2)
    category = Category(**category_data)
    category.add_product(new_product)
    assert Category.product_count == cat_num_prod + 1


def test_products_property(one_category_fixture):
    product_info = one_category_fixture.products
    assert "Iphone 15, 210000 руб. Остаток: 5 шт." in product_info
    assert "Samsung Galaxy, 180000 руб. Остаток: 3 шт." in product_info


def test_products_str(product_str_fixture):
    product, exp_str = product_str_fixture
    assert str(product) == exp_str


def test_products_add(sample_product, another_product):
    product_sum = sample_product + another_product
    assert product_sum == 1590000


def test_category_str(one_category_fixture):
    category = one_category_fixture
    assert str(category) == "Электроника, количество продуктов: 8 шт."


def test_iteration_over_products(one_category_fixture):
    iterator = CategoryIterator(one_category_fixture)
    products = list(iterator)
    assert products[0].name == "Iphone 15"
    assert products[1].name == "Samsung Galaxy"


def test_smartphone_creation():
    phone = Smartphone(
        name="iPhone",
        description="Флагманский смартфон",
        price=120000,
        quantity=5,
        model="15 Pro Max",
        memory=256,
        color="black",
        efficiency=0.92,
    )

    assert phone.name == "iPhone"
    assert phone.model == "15 Pro Max"
    assert phone.memory == 256
    assert phone.color == "black"
    assert phone.efficiency == 0.92


def test_lawngrass_creation():
    grass = LawnGrass(
        name="Зелёная трава",
        description="Для газонов",
        price=500,
        quantity=20,
        country="Россия",
        germination_period=14.0,
        color="зелёный",
    )

    assert grass.name == "Зелёная трава"
    assert grass.country == "Россия"
    assert grass.germination_period == 14.0
    assert grass.color == "зелёный"


def test_add_invalid_product_raises():
    not_a_product = object()
    cat = Category("Техника", "Электроника", [])

    with pytest.raises(TypeError, match="Можно добавлять только объекты Product"):
        cat.add_product(not_a_product)


def test_add_different_type_products_raises():
    phone = Smartphone("iPhone", "смартфон", 100000, 2, "15 Pro", 256, "чёрный", 0.9)
    grass = LawnGrass("Трава", "газон", 500, 4, "Россия", 14.0, "зелёный")

    with pytest.raises(TypeError, match="Нельзя складывать Smartphone и LawnGrass"):
        _ = phone + grass


def test_mixin_log_output_on_product_creation(capsys):
    _ = Product("Товар", "Описание", 1500, 3)
    captured = capsys.readouterr()

    assert "[LOG] Создан объект класса Product" in captured.out
    assert "Товар" in captured.out
    assert "1500" in captured.out
    assert "3" in captured.out
