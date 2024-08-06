import requests
from bs4 import BeautifulSoup
import json
import re

# URL для поиска вакансий Python в Москве и Санкт-Петербурге
base_url = "https://hh.ru/search/vacancy?enable_snippets=true&order_by=publication_time&ored_clusters=true&search_period=7&area=1&area=2&search_field=name&search_field=company_name&search_field=description&text=Python&L_save_area=true"

# Заголовки для запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/92.0.4515.159 Safari/537.36"
}

# Список для хранения информации о вакансиях
vacancy_list = []
link_list = []
status = True


# Получение всех вакансий со страницы
def fetch_description(link):
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        vacancy_soup = BeautifulSoup(response.text, 'html.parser')
        description_link = vacancy_soup.find_all('a', {'data-qa': 'serp-item__title'})
        if description_link:
            for link in description_link:
                link_list.append(link['href'])
            return link_list
    else:
        status = False
        return status


# Перебор найденных вакансий и отбор по параметрам
for link in fetch_description(base_url):
    response = requests.get(link, headers=headers)
    vacancy_info = BeautifulSoup(response.text, 'html.parser')
    description_vacancy = vacancy_info.find('div', class_='vacancy-branded-user-content')
    try:
        if 'Django' or 'Flask' or 'django' or 'flask' in description_vacancy.get_text():
            title = vacancy_info.find('h1', {'data-qa': 'vacancy-title'}).text.strip()
            company = vacancy_info.find('a', {'data-qa': 'vacancy-company-name'}).text.strip()
            location = vacancy_info.find('p', {'data-qa': 'vacancy-view-location'}).text.strip()
            if vacancy_info.find('div', {'data-qa': 'vacancy-salary'}):
                price = vacancy_info.find('div', {'data-qa': 'vacancy-salary'}).text.strip()
                price = re.sub(r'\D', ' ', price).strip()
            else:
                price = "По з/п надо уточнять..."
            vacancy_list.append({
                "Название": title,
                "Компания": company,
                "Город": location,
                "Ссылка": link,
                "Зарплата": price,
            })
    except AttributeError:
        continue

# Запись в JSON файл
with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancy_list, f, ensure_ascii=False, indent=4)

print(f"Найдено {len(vacancy_list)} вакансий, соответствующих критериям.")
