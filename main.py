import csv
from typing import List, Dict, Tuple


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Читает csv-файл и возвращает список словарей с данными о сотрудниках.
    Каждый словарь содержит поля "ФИО полностью", "Департамент", "Отдел",
    "Должность", "Оценка", "Оклад".
    :param file_path: путь к csv-файлу
    :return: список словарей с данными о сотрудниках
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            employee = dict(zip(header, row))
            data.append(employee)
        return data


def get_department_hierarchy(
        data: List[Dict[str, str]]
) -> Dict[str, List[str]]:
    """
    Возвращает словарь, в котором ключами являются названия отделов,
    а значениями - списки команд, принадлежащих этим департаментам.
    :param data: список словарей с данными о сотрудниках
    :return: словарь с иерархией департаментов и команд
    """
    hierarchy = {}
    for employee in data:
        department = employee['Департамент']
        team = employee['Отдел']
        if department not in hierarchy:
            hierarchy[department] = [team]
        elif team not in hierarchy[department]:
            hierarchy[department].append(team)
    return hierarchy


def print_department_hierarchy(hierarchy: Dict[str, List[str]]):
    """
    Выводит на экран иерархию департаментов и команд.
    :param hierarchy: словарь с иерархией департаментов и команд
    """
    for department, teams in hierarchy.items():
        print(department)
        for team in teams:
            print(f'-- {team}')


def get_department_report(
        data: List[Dict[str, str]]
) -> List[Tuple[str, int, Tuple[int, int], float]]:
    """
    Возвращает список кортежей с данными о департаментах.
    Каждый кортеж содержит название департамента, численность,
    вилку зарплат (минимальная и максимальная), среднюю зарплату.
    :param data: список словарей с данными о сотрудниках
    :return: список кортежей с данными о департаментах
    """
    departments = {}
    for employee in data:
        department = employee['Департамент']
        if department not in departments:
            departments[department] = {
                'count': 1,
                'min_salary': int(employee['Оклад']),
                'max_salary': int(employee['Оклад']),
                'total_salary': int(employee['Оклад'])
            }
        else:
            departments[department]['count'] += 1
            salary = int(employee['Оклад'])
            departments[department]['min_salary'] = min(
                departments[department]['min_salary'],
                salary)
            departments[department]['max_salary'] = max(
                departments[department]['max_salary'],
                salary)
            departments[department]['total_salary'] += salary
    report = []
    for department, stats in departments.items():
        count = stats['count']
        min_salary = stats['min_salary']
        max_salary = stats['max_salary']
        avg_salary = stats['total_salary'] / count
        report.append((department, count, (min_salary, max_salary),
                       avg_salary))
    return report


def print_department_report(
        report: List[Tuple[str, int, Tuple[int, int], float]]
):
    """
    Выводит на экран сводный отчёт по департаментам.
    :param report: список кортежей с данными о департаментах
    """
    for department, count, (min_salary, max_salary), avg_salary in report:
        print(f'{department}:')
        print(f'-- Численность: {count}')
        print(f'-- Вилка зарплат: {min_salary} - {max_salary}')
        print(f'-- Средняя зарплата: {avg_salary}')


def save_department_report(
        report: List[Tuple[str, int, Tuple[int, int], float]],
        file_path: str):
    """
    Сохраняет сводный отчёт по департаментам в csv-файл.
    :param report: список кортежей с данными о департаментах
    :param file_path: путь к csv-файлу
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Департамент', 'Численность', 'Минимальная зарплата',
                         'Максимальная зарплата', 'Средняя зарплата'])
        for department, count, (min_salary, max_salary), avg_salary in report:
            writer.writerow([department, count, min_salary, max_salary,
                             avg_salary])


if __name__ == '__main__':
    file_path = 'Corp_Summary.csv'
    data = read_csv(file_path)
    while True:
        print('Меню:')
        print('1. Вывести иерархию департаментов')
        print('2. Вывести сводный отчёт по департаментам')
        print('3. Сохранить сводный отчёт в csv-файл')
        print('0. Выход')
        choice = input('Выберите пункт меню: ')
        if choice == '1':
            hierarchy = get_department_hierarchy(data)
            print_department_hierarchy(hierarchy)
        elif choice == '2':
            report = get_department_report(data)
            print_department_report(report)
        elif choice == '3':
            report = get_department_report(data)
            file_path = input('Введите путь к файлу для сохранения отчёта: ')
            save_department_report(report, file_path)
        elif choice == '0':
            break
        else:
            print('Некорректный выбор, попробуйте ещё раз')
