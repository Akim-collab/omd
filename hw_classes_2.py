import json
from typing import Union
import keyword


class JSONConverter:
    """
    Класс для преобразования JSON-объектов в Python-объекты
    с доступом к атрибутам через точку.
    """

    def __init__(self, data: Union[dict, list, int, str]):
        """
        Инициализация объекта класса JSONConverter.

        :param data: JSON-объект или значение простого типа для конвертации.
        """
        self._convert(data)

    def _convert(self, data: Union[dict, list, int, str]):
        """
        Рекурсивное преобразование JSON-объекта в атрибуты текущего объекта.

        :param data: JSON-объект или значение простого типа для конвертации.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                key = key + "_" if keyword.iskeyword(key) else key
                setattr(self, key, JSONConverter(value))
        elif isinstance(data, list):
            setattr(self, "items", [JSONConverter(item) for item in data])
        else:
            setattr(self, "value", data)


class ColorizeMixin:
    """
    Миксин для изменения цвета текста при выводе на консоль.
    """

    repr_color_code: int = 0
    """
    Код цвета ANSI для изменения цвета текста при выводе.
    0 - стандартный цвет.
    """

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта с учетом цвета.

        :return: Строковое представление объекта с применением цвета.
        """
        return f"\033[{self.repr_color_code}m{super().__repr__()}\033[0m"


class Advert(JSONConverter, ColorizeMixin):
    """
    Класс для представления объявлений с дополнительной валидацией цены.
    """

    def __init__(self, data: dict):
        """
        Инициализация объекта класса Advert.

        :param data: JSON-объект с данными объявления.
        """
        super().__init__(data)
        self._validate_price()

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объявления.

        :return: Строковое представление объявления.
        """
        return f"{self.title.value} | {self.price.value} ₽"

    def _validate_price(self) -> None:
        """
        Валидация цены. Если цены нет, устанавливается
        значение по умолчанию (0).
        Если цена отрицательная, вызывается исключение ValueError.
        """
        if not hasattr(self, 'price'):
            setattr(self, 'price', JSONConverter(0))
        elif self.price.value < 0:
            raise ValueError("Price must be >= 0")


if __name__ == '__main__':

    lesson_str = """
    {
        "title": "python",
        "price": 0,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        }
    }
    """
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)

    # Обращаемся к атрибуту location.address
    print(lesson_ad.location.address.value)
    # Out: 'город Москва, Лесная, 7'

    # Создаем экземпляр класса Advert из JSON без атрибута price
    dog_str = '{"title": "Вельш-корги", "class": "dogs"}'
    dog = json.loads(dog_str)
    dog_ad = Advert(dog)

    # Обращаемся к атрибуту `dog_ad.class_` вместо `dog_ad.class`
    print(dog_ad.class_.value)
    # Out: 'dogs'

    # Проверка валидации цены
    try:
        invalid_price_str = '{"title": "python", "price": -1}'
        invalid_price = json.loads(invalid_price_str)
        invalid_price_ad = Advert(invalid_price)
    except ValueError as e:
        print(str(e))
    # Out: ValueError: Price must be >= 0

    # Пример использования
    iphone_ad_str = '{"title": "iPhone X", "price": 100}'
    iphone_ad_data = json.loads(iphone_ad_str)
    iphone_ad = Advert(iphone_ad_data)

    print(iphone_ad)
    # Out: iPhone X | 100 ₽

    # Создаем экземпляр класса Advert из JSON без атрибута price
    corgi_str = '{"title": "Вельш-корги", "price": 1000, "class": "dogs"}'
    corgi_data = json.loads(corgi_str)
    corgi = Advert(corgi_data)

    print(corgi)
    # Out: Вельш-корги | 1000 ₽ (желтым цветом, если всё настроено правильно)
