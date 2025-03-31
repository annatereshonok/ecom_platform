import pytest

from src.main import Category, Product


def test_product_positive(product_fixture_positive):
    product, prod_name, prod_desc, prod_price, prod_quantity = product_fixture_positive
    assert product.name == prod_name
    assert product.description == prod_desc
    assert product.price == prod_price
    assert product.quantity == prod_quantity


def test_product_negative(product_fixture_negative):
    product_data, expected_error = product_fixture_negative
    with pytest.raises(ValueError, match=expected_error):
        Product(**product_data)


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
    monkeypatch.setattr('builtins.input', lambda _: "y")
    sample_product.price = 200000
    assert sample_product.price == 200000
    monkeypatch.setattr('builtins.input', lambda _: "n")
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
