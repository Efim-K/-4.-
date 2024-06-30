from src.class_api import HeadHunterAPI
from src.work_file_vacancies import WorkFileVacancies
from src.class_vacancy import Vacancy


def get_vacancies_instances(vacancies: list[dict]) -> list[Vacancy]:
    """
    Преобразование списка словарей из интернета в список класса вакансий
    """
    return [Vacancy.create_vacancy(vacancy) for vacancy in vacancies]


def to_vacancy_from_dict(vacancies: list[dict]) -> list[Vacancy]:
    """
    Преобразование измененного списка словарей обратно в список класса вакансий
    """
    return [Vacancy(*vacancy.values()) for vacancy in vacancies]


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Сортировка вакансий по зарплате выбранной валюты
    """
    vacancy_list_currency = []
    currency = input(
        'Введите валюту зарплаты для сортировки и фильтрации по валюте: RUR, KZT, BYR, UZS, USD, KGS\n').upper()
    if currency == '':
        print('Валюта не выбрана. Вакансии по зарплате и валюте не будут отсортированы')
        return vacancies
    for vacancy in vacancies:
        if currency in vacancy.currency:
            vacancy_list_currency.append(vacancy)

    if not vacancy_list_currency:
        print(f'Вакансии с введенной валютой {currency} не найдены\n'
              'Вакансии по зарплате и валюте не будут отсортированы')
        return vacancies

    return sorted(vacancy_list_currency, reverse=True)


def get_numbers_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Возвращает количество запрашиваемых numbers вакансий
    """

    try:
        numbers = int(input('Введите количество ТОП вакансий по зарплате для просмотра: \n'))
    except ValueError:
        print('Число не задано. Будут выбраны все вакансии\n')
        return vacancies

    print(f'Всего найдено {len(vacancies)} вакансий.\n'
          f'Ниже показаны {numbers} ТОП вакансий по зарплате:\n\n')

    return [(vacancies[i]) for i in range(len(vacancies)) if i < numbers]


def filtered_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Возвращает список вакансий содержащее ключевое слово
    """
    name_criterion = input('Введите ключевое слово для поиска вакансий среди выбранной профессии: \n').lower()

    filtered_vac = []

    for vacancy in vacancies:
        all_attribute_vac = (vacancy.name + vacancy.area + vacancy.responsibility + vacancy.requirement).lower()

        if name_criterion in all_attribute_vac:
            filtered_vac.append(vacancy)

    if not filtered_vac:
        print('Ключевое слово не найдено. Список вакансий не изменен\n')
        return vacancies

    return filtered_vac


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    # Удаление вакансий из предыдущих поисков
    json_file = WorkFileVacancies()
    delete_vacancy = input('Удалить историю предыдущих поисков вакансий? да/нет : \n').lower()
    if delete_vacancy in ('да', 'yes', 'y', 'д'):
        json_file.del_vacancies()

    user_vacancy = input('Введите ключевое слово  для поиска профессии на сайте hh.ru: \n').lower()
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh = HeadHunterAPI()

    # Получение вакансий с hh.ru в формате JSON
    vacancies_list = hh.load_vacancies(user_vacancy)

    # Преобразование списка словарей вакансий в список класса Вакансий
    user_vacancy_list = []
    try:
        user_vacancy_list = get_vacancies_instances(vacancies_list)
    except AttributeError:
        # Ошибка обращения к списку загруженных с сайта вакансий.
        if delete_vacancy not in ('да', 'yes', 'y', 'д'):
            print('Вакансии не найдены\n')
        else:
            return print('Вакансии не найдены\n')

    # Загрузка данных из предыдущих поисков
    if delete_vacancy not in ('да', 'yes', 'y', 'д'):
        use_history = input('Использовать историю предыдущих поисков вакансий? да/нет : \n').lower()
        if use_history in ('да', 'yes', 'y', 'д'):
            user_vacancy_list_dict = json_file.merging_lists_vacancies(user_vacancy_list)
            user_vacancy_list = to_vacancy_from_dict(user_vacancy_list_dict)

    # Применение фильтра по ключевому слову к вакансиям
    filtered_user_vacancy_list = filtered_vacancies(user_vacancy_list)
    while True:
        name_criterion = input('Хотите еще отфильтровать вакансии по ключевому слову? да/нет: \n').lower()
        if name_criterion in ('да', 'yes', 'y', 'д'):
            filtered_user_vacancy_list = filtered_vacancies(filtered_user_vacancy_list)
        else:
            break

    #  фильтрация вакансий по валюте и сортировка по величине зарплаты
    filtered_user_vacancy_list = sort_vacancies(filtered_user_vacancy_list)

    # Записываем отфильтрованные пользователем вакансии
    json_file.save_vacancies(filtered_user_vacancy_list)

    # Выводит количество вакансий для просмотра
    top_n_vacancy = get_numbers_vacancies(filtered_user_vacancy_list)
    [print(vacancy) for vacancy in top_n_vacancy]
