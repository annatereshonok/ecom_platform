import json
import os
from typing import List

from src.main import Category, Product

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = "data"


def load_data_from_json(filename: str) -> List[Category]:
    """
    Загружает данные о категориях и продуктах из JSON файла и создает соответствующие объекты классов.
    :param filename: Имя JSON файла, который нужно загрузить.
    Файл должен содержать информацию о категориях и продуктах.
    :return: Список объектов категории, где каждый объект содержит список продуктов.
    """

    file_path = os.path.join(BASE_DIR, DATA_FOLDER, filename)
    with open(file_path, "r") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        product_list = [Product(**product) for product in category_data["products"]]
        category_data["products"] = product_list
        category = Category(**category_data)
        categories.append(category)

    return categories


if __name__ == "__main__":
    file_name = "products.json"
    data_file = load_data_from_json(file_name)
    print(data_file)
