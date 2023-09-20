def step2_umbrella():
    print(
        'Утка-маляр взяла зонтик и пошла в бар. '
        'Но на улице оказалось слишком жарко, '
        'и она решила спрятать зонтик и идти без него. '
        'Куда она спрятала зонтик?'
    )
    option = ''
    options = {'Закопала в землю': False, 'Положила на крышу': False, 'Оставила у входа в бар': True}
    while option not in options:
        print('Выберите: {}, {} или {}'.format(*options))
        option = input()

    if options[option]:
        return 'Утка-маляр успешно провела время в баре!'
    return 'К сожалению, утка-маляр потеряла зонтик и была вынуждена вернуться домой.'


def step2_no_umbrella():
    print(
        'Утка-маляр не взяла зонтик и пошла в бар. '
        'Но на улице начался ливень, '
        'и она решила вернуться домой. '
        'Как она вернулась домой?'
    )
    option = ''
    options = {'Промокла до нитки': False, 'Спряталась под крышей': True, 'Заказала такси': False}
    while option not in options:
        print('Выберите: {}, {} или {}'.format(*options))
        option = input()

    if options[option]:
        return 'Утка-маляр благополучно вернулась домой!'
    return 'К сожалению, утка-маляр промокла до нитки и была принуждена провести остаток дня в постели.'


def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


if __name__ == '__main__':
    step1()
