import sqlite3
from classfolder.class_name import States

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_new_user(user_id: int, user_name: str, user_surname: str, username: str):
    try:
        cursor.execute(
            'INSERT INTO userdata (user_id, user_name, user_surname, username, state) VALUES (?, ?, ?, ?, ?)',
            (user_id, user_name, user_surname, username, States.S_START))
    except sqlite3.Error as error:
        cursor.execute('UPDATE userdata SET user_name = ?, user_surname = ?, username = ?, state = ? WHERE user_id=?',
                       (user_name, user_surname, username, States.S_START, user_id))
    conn.commit()


def db_table_set_link(user_id: int, name_recipe: str, link_recipe: str):
    try:
        cursor.execute('INSERT INTO recipe_of_dishes (user, link_recipe, name_recipe) VALUES (?, ?, ?)',
                       (user_id, link_recipe, name_recipe.lower()))
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    conn.commit()


def db_table_setstate(user_id: int, state: int):
    try:
        cursor.execute('UPDATE userdata SET state = ? WHERE user_id = ?',
                       (state, user_id))
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    conn.commit()


def db_table_getstate(user_id: int):
    try:
        cursor.execute('SELECT state FROM userdata WHERE user_id = ?', (user_id,))
        records = cursor.fetchall()
        conn.commit()
        return records[0][0]
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        conn.commit()
        return States.S_START


def get_all_recipe(user_id: int):
    try:
        cursor.execute('SELECT name_recipe, link_recipe FROM recipe_of_dishes WHERE user = ?', (user_id,))
        records = cursor.fetchall()
        conn.commit()
        return records
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return 'error'


def db_table_set_all_tag(recipe_id: int, tag: str):
    try:
        cursor.execute('INSERT INTO tag_table (ID_recipe, tag_name) VALUES (?, ?)',
                       (recipe_id, tag))
        conn.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def db_table_get_article_from_tag(user_id: int, tag: str):
    try:
        cursor.execute('SELECT DISTINCT name_recipe, link_recipe '
                       'FROM recipe_of_dishes '
                       'INNER JOIN tag_table '
                       'ON (tag_table.ID_recipe = recipe_of_dishes.id_recipe)'
                       'WHERE tag_name LIKE ? OR tag_name LIKE ? OR tag_name LIKE ? OR tag_name LIKE ? AND user = ?',
                       ("%" + tag + "%", tag + "%", "%" + tag, tag, user_id))
        records = cursor.fetchall()
        return records
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


# Поиск с начала и с конца !1!
def db_table_get_article_from_name(user_id: int, name: str):
    try:
        cursor.execute('SELECT DISTINCT name_recipe, link_recipe '
                       'FROM recipe_of_dishes '
                       'WHERE name_recipe LIKE ? '
                       'OR name_recipe LIKE ? '
                       'OR name_recipe LIKE ? OR name_recipe LIKE ? AND user = ?',
                       ("%" + name + "%", "%" + name, name + "%", name, user_id))
        records = cursor.fetchall()
        return records
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def db_table_get_last_index(link: str, user_id: int):
    try:
        cursor.execute('SELECT id_recipe '
                       'FROM recipe_of_dishes '
                       'WHERE link_recipe = ? AND user = ?', (link,user_id))
        records = cursor.fetchall()
        return records[0][0]
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
