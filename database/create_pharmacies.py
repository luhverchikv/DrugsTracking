# database/create_pharmacies.py
import time
import requests
from bs4 import BeautifulSoup
from config import headers_103, cookies_103, region_dict_103
from db import execute_query
from loguru import logger


def pharmacy_103_exists(pharm_id):
    query = "SELECT 1 FROM pharmacies_103 WHERE item_id = %s LIMIT 1"
    try:
        result = execute_query(query, 'pharma_tracker', (pharm_id,))
        return len(result) > 0  # Возвращаем True, если запись найдена
    except Exception as e:
        logger.error(f"Ошибка при проверке существования аптеки с id '{pharm_id}': {e}")
        return False


# Функция для сохранения аптеки в таблицу pharmacies_103
def save_pharmacy_103(pharm_id, group_id, name, address, phone, coordinates, region):
    # SQL-запрос для вставки данных в таблицу
    query = """
    INSERT INTO pharmacies_103 (item_id, group_id, name, address, phone, coordinates, region, district, pharmacy_chain, is_active, count_drugs)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Параметры для вставки
    params = (
        pharm_id,  # item_id
        group_id,  # group_id
        name,  # name
        address,  # address
        phone,  # phone
        coordinates,  # coordinates
        region,  # region
        None,  # district (по умолчанию None)
        None,  # pharmacy_chain (по умолчанию None)
        0,  # is_active (по умолчанию 0)
        0  # count_drugs (по умолчанию 0)
    )
    # Выполнение SQL-запроса
    try:
        execute_query(query, 'pharma_tracker', params)
    except Exception as e:
        logger.error(f"Ошибка при добавлении аптеки '{name}': {e}")


def get_drugs_list(url, cookies, headers):
    response = requests.get(url=url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def create_list_pharmacy(region, region_url):
    for page in range(1, 250):
        url = f'https://apteka.103.by/apteki/{region_url}/?sort=name:asc&page={page}'
        data = get_drugs_list(url, cookies_103, headers_103).find_all("div", class_="drugStore__item")
        time.sleep(6)  # Задержка для избежания блокировки
        if data:
            for i in data:
                try:
                    name = i.find("span", class_="drugStore__name").text.strip()
                    address = i.find("span", class_="drugStore__address").text.strip()
                    coordinates = f"{i['data-lat']}, {i['data-lon']}"
                    phone = i.find("div", class_="drugStore__buttonList").find('span').text.strip()
                    pharm_id = i['data-id']
                    group_id = i['data-group-id']

                    # Проверяем, существует ли аптека в базе данных
                    if not pharmacy_103_exists(pharm_id):
                        save_pharmacy_103(pharm_id, group_id, name, address, phone, coordinates, region)
                except Exception as e:
                    logger.error(f"Ошибка при обработке аптеки: {e}")
        else:
            break


def create_pharmacies_103():
    for region, region_url in region_dict_103.items():
        create_list_pharmacy(region, region_url)
