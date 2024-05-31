"""
en: Module for Create actions with SQLite database
ru: Модуль для создания действий с базой данных SQLite
"""
import sqlite3
import json

import config


def create_table(name, columns):
    """
    en: Create a table in a SQLite database
    ru: Создать таблицу в базе данных SQLite
    """
    columns = ', '.join(columns)
    # Connect to the database
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # Create a table with columns
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({columns})")

    # Commit changes and close connection
    conn.commit()
    conn.close()


def insert_into_db(table_name, data_dict):
    """
    en: Insert data into a SQLite database
    ru: Вставить данные в базу данных SQLite
    """
    # en: Connect to the database / ru: Подключиться к базе данных
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # en: Insert data into the table / ru: Вставить данные в таблицу
    keys = ', '.join(data_dict.keys())
    values = ', '.join([f"'{value}'" for value in data_dict.values()])
    cursor.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({values})")

    # en: Commit changes and close connection / ru: Зафиксировать изменения и закрыть соединение
    conn.commit()
    conn.close()


def update_value(table_name, column_name, value, where_column, where_value):
    """
    en: Update a value in a SQLite database
    ru: Обновить значение в базе данных SQLite
    """
    # en: Connect to the database / ru: Подключиться к базе данных
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # en: Update the value in the table / ru: Обновить значение в таблице
    cursor.execute(f"UPDATE {table_name} SET {column_name} = '{value}' WHERE {where_column} = '{where_value}'")

    # en: Commit changes and close connection / ru: Зафиксировать изменения и закрыть соединение
    conn.commit()
    conn.close()


def insert_json_into_db(json_file_path, table_name):
    """
    en: Insert data from a json file into a SQLite database
    ru: Вставить данные из файла json в базу данных SQLite
    """
    with open(json_file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)

    # en: Connect to the database / ru: Подключиться к базе данных
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # en: Create table with keys as columns / ru: Создать таблицу с ключами в качестве столбцов
    columns = ', '.join(data[0].keys())
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    # en: Insert values into the table / ru: Вставить значения в таблицу
    for item in data:
        keys = ', '.join(item.keys())
        values = ', '.join([f"'{value}'" for value in item.values()])
        cursor.execute(f"INSERT INTO {table_name} ({keys}) VALUES ({values})")

    # en: Commit changes and close connection / ru: Зафиксировать изменения и закрыть соединение
    conn.commit()
    conn.close()


def get_data_from_db(table_dict, column_name=None, value=None):
    """
    en: Get data from a SQLite database
    ru: Получить данные из базы данных SQLite
    """
    table_name = table_dict['name']
    columns = [c.split()[0] for c in table_dict['columns']]
    # Connect to the database
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # en: Get data from the table / ru: Получить данные из таблицы
    if not (column_name and value):
        cursor.execute(f"SELECT * FROM {table_name}")
    else:
        cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = '{value}'")

    data = cursor.fetchall()
    data = [dict(zip(columns, item)) for item in data]

    conn.commit()
    conn.close()
    return data


def clear_table(table_name):
    """
    en: Clear a table in a SQLite database
    ru: Очистить таблицу в базе данных SQLite
    """
    # en: Connect to the database / ru: Подключиться к базе данных
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # en: Clear the table / ru: Очистить таблицу
    cursor.execute(f"DELETE FROM {table_name}")

    # en: Commit changes and close connection / ru: Зафиксировать изменения и закрыть соединение
    conn.commit()
    conn.close()


def delete_table(table_name):
    """
    en: Delete a table from a SQLite database
    ru: Удалить таблицу из базы данных SQLite
    """
    # en: Connect to the database / ru: Подключиться к базе данных
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # en: Delete the table / ru: Удалить таблицу
    cursor.execute(f"DROP TABLE {table_name}")

    # en: Commit changes and close connection / ru: Зафиксировать изменения и закрыть соединение
    conn.commit()
    conn.close()
