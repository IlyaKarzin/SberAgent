from langchain.tools import tool
from database import database
from typing import Dict
from post.post import init_post


conn, cursor = database.init_db()
post = init_post()
barcode_database = database.get_all_barcodes(cursor)

@tool
def get_all_barcode() -> list:
    """Возвращает все добавленные номера отслеживания"""
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + "Bot requested get_all_barcode()" + "\033[0m")
    barcode_database = database.get_all_barcodes(cursor)
    return barcode_database

@tool
def get_barcode_data(barcode: str) -> Dict:
    """
    Возвращает информацию по отслеживанию
    """
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested get_phone_data_by_name({barcode})" + "\033[0m")
    history = post.get_history(barcode)
    return history[len(history)-1]

@tool
def add_barcode(barcode: str) -> None:
    """
    Находит информацию по номеру отслеживания и добавляет её в базу.
    Args:
        barcode: Номер отправления для добавления
    """

    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested add_barcode({barcode})" + "\033[0m")

    # Получение истории отправления
    history = post.get_history(barcode)

    # Извлечение имени получателя и адреса
    recipient = history[0]['UserParameters']['Rcpn']
    index = history[0]['AddressParameters']['DestinationAddress']['Index']
    description = history[0]['AddressParameters']['DestinationAddress']['Description']
    address = f"{index} {description}"  # Упрощённое форматирование адреса

    # Добавление данных в базу
    database.add_barcode_to_db(cursor, conn, barcode, recipient, address)
    barcode_database.append({"barcode": barcode, "recipient": recipient, "address": address})