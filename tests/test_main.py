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
    assert Category.products_count == cat_num_prod
    assert category.category_count == cat_num_cat
