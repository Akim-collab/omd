import json
from hw_classes_2 import Advert


if __name__ == "__main__":
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
