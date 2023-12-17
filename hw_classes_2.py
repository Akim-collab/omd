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

    def __init_subclass__(cls, repr_color_code, **kwargs):
        """
        Инициализация подкласса. Устанавливает код цвета для объекта.

        :param repr_color_code: Код цвета ANSI.
        :param kwargs: Дополнительные аргументы.
        """
        super().__init_subclass__(**kwargs)
        cls.repr_color_code = repr_color_code

    def colorize_text(self, text):
        """
        Применяет код цвета к тексту.

        :param text: Текст для применения цвета.
        :return: Текст с примененным цветом.
        """
        return f"\033[{self.repr_color_code}m{text}\033[0m"


class Advert(ColorizeMixin, JSONConverter, repr_color_code=33):
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
        self.content = f"{self.title.value} | {self.price.value} ₽"
        return self.colorize_text(self.content)

    def _validate_price(self) -> None:
        """
        Валидация цены. Если цены нет, устанавливается
        значение по умолчанию (0).
        Если цена отрицательная, вызывается исключение ValueError.
        """
        if not hasattr(self, "price"):
            setattr(self, "price", JSONConverter(0))
        elif self.price.value < 0:
            raise ValueError("Price must be >= 0")


if __name__ == "__main__":
    pass
