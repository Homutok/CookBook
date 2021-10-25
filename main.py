import telebot
import data.messagebox as messagebox
import functions.functions as func
import random
import db.db_functions as data
import classfolder.class_name as class_name
from data.data import token

# Всякие переменные
bot = telebot.TeleBot(token)
us_id = 0
tag = []
new_text = class_name.Article("Title", "Author", "", "empty", "")
# Меню помощи
keyboardHelper = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardHelper.row('Добавить рецепт', 'Мои рецепты', 'Добавить рецепт с сайта')
# Меню во время написания статьи
keyboardCancel = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardCancel.row('Отмена')
keyboardArticle = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardArticle.row('Я закончил', 'Отмена')
# Меню взаимодействия с списком рецептов
keyboardRecipe = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardRecipe.row('Поиск по названию', 'Поиск по ингридиенту', 'Просто список')
# Меню взаимодействия с списком
keyboardList = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardList.row('Ещё', 'Спасибо')
# Сокрытие меню
hide_keyboard = telebot.types.ReplyKeyboardRemove()


# Обработчик команд
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, messagebox.msgHello, reply_markup=keyboardHelper)
    user_id = message.from_user.id
    us_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    new_text.re_name(username)
    data.db_table_new_user(user_id=user_id, user_name=us_name, user_surname=user_surname, username=username)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, messagebox.msgHelp, reply_markup=keyboardHelper)


def end_article(message):
    link = new_text.publish_article()
    bot.send_message(message.chat.id, link)
    data.db_table_set_link(message.from_user.id, new_text.A_Title, link)
    set_tags(data.db_table_get_last_index(link, message.from_user.id))
    data.db_table_setstate(message.from_user.id, data.States.S_START)
    new_text.text_erase()


def next_step(message):
    if data.db_table_getstate(message.from_user.id) < data.States.S_ENTER_TAG:
        data.db_table_setstate(message.from_user.id, data.db_table_getstate(message.from_user.id) + 1)
    else:
        end_article(message)


@bot.message_handler(commands=['cancel'])
def cancel(message):
    data.db_table_setstate(message.from_user.id, data.States.S_START)
    bot.send_message(message.chat.id, messagebox.msgOK, reply_markup=keyboardHelper)


# Обработчики событий
@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_START)
def send_text(message):
    match message.text.lower():
        case 'добавить рецепт':
            data.db_table_setstate(message.from_user.id, data.States.S_ENTER_TITLE)
            bot.send_message(message.chat.id, messagebox.msgSetTitle, reply_markup=keyboardCancel)
        case 'мои рецепты':
            bot.send_message(message.chat.id, messagebox.msgRecipeList, reply_markup=keyboardRecipe)
            data.db_table_setstate(message.from_user.id, data.States.S_SEARCH_CHOOSE)
        case 'добавить рецепт с сайта':
            bot.send_message(message.chat.id, messagebox.msgAddText)
            data.db_table_setstate(message.from_user.id, data.States.S_ADD_RECIPE)
        case _:
            bot.send_message(message.chat.id, messagebox.msgAnswer[random.randint(0, len(messagebox.msgAnswer))])


@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_SEARCH_CHOOSE)
def send_search(message):
    match message.text.lower():
        case 'поиск по названию':
            data.db_table_setstate(message.from_user.id, data.States.S_SEARCH_NAME)
            bot.send_message(message.chat.id, "Вводите название", reply_markup=hide_keyboard)
        case 'поиск по ингридиенту':
            data.db_table_setstate(message.from_user.id, data.States.S_SEARCH_TAG)
            bot.send_message(message.chat.id, "Введите ингридиент, по которому вы хотите искать", reply_markup=hide_keyboard)
        case 'просто список':
            for recipe in data.get_all_recipe(message.from_user.id):
                bot.send_message(message.chat.id, recipe[0] + "\n" + recipe[1])
            data.db_table_setstate(message.from_user.id, data.States.S_START)
            bot.send_message(message.chat.id, "Воть", reply_markup=keyboardHelper)


# Добавление разных элментов статьи
@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_ENTER_TITLE)
def new_article(message):
    match message.text.lower():
        case 'отмена':
            cancel(message)
        case _:
            new_text.re_title(message.text)
            get_tag_from_name()
            bot.send_message(message.chat.id, messagebox.msgIngredient, reply_markup=keyboardArticle)
            data.db_table_setstate(message.from_user.id, data.States.S_ENTER_INGREDIENT)


@bot.message_handler(
    func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_ENTER_INGREDIENT)
def add_ingredient(message):
    match message.text.lower():
        case 'я закончил':
            next_step(message)
            bot.send_message(message.chat.id, messagebox.msgSetText)
        case 'отмена':
            cancel(message)
        case _:
            new_text.add_ingredient(message.text)
            tag.append(message.text.lower())
    pass


@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_ENTER_TEXT)
def add_text(message):
    match message.text.lower():
        case 'я закончил':
            end_article(message)
        case 'отмена':
            cancel(message)
        case _:
            new_text.add_text(message.text.lower())
    pass


@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_ENTER_TAG)
def add_tag(message):
    new_text.add_tag(message.text)
    pass


@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_ADD_RECIPE)
def add_new(message):
    func.add_another_recipe(message, new_text, bot)


@bot.message_handler(content_types=["photo"],
                     func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_ENTER_TEXT)
def add_photo(message):
    photo_id = message.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    new_text.add_text("<img src=" + f'https://api.telegram.org/file/bot{data.token}/{file_info.file_path}' + ">")


# Поиск
@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_SEARCH_TAG)
def search_tag(message):
    if not data.db_table_get_article_from_tag(message.from_user.id, message.text.lower()):
        bot.send_message(message.chat.id, messagebox.msgEmptySearch, reply_markup=keyboardHelper)
    for recipe in data.db_table_get_article_from_tag(message.from_user.id, message.text.lower()):
        bot.send_message(message.chat.id, recipe[0] + "\n" + recipe[1], reply_markup=keyboardHelper)
    data.db_table_setstate(message.from_user.id, data.States.S_START)


@bot.message_handler(func=lambda message: data.db_table_getstate(message.from_user.id) == data.States.S_SEARCH_NAME)
def search_name(message):
    if not data.db_table_get_article_from_name(message.from_user.id, message.text.lower()):
        bot.send_message(message.chat.id, messagebox.msgEmptySearch, reply_markup=keyboardHelper)
    for recipe in data.db_table_get_article_from_name(message.from_user.id, message.text.lower()):
        bot.send_message(message.chat.id, recipe[0] + "\n" + recipe[1], reply_markup=keyboardHelper)
    data.db_table_setstate(message.from_user.id, data.States.S_START)


def set_tags(article_id):
    for item in range(0, len(tag)):
        data.db_table_set_all_tag(article_id, tag[item].lower())
    tag.clear()


def get_tag_from_name():
    words = new_text.get_title()
    for word in words.split():
        if len(word) >= 3:
            tag.append(word)
    pass


bot.polling()
# * - НОРМ добавление рецепта
# * - Тэги автоматом
# ! - Больше сайтов для парсинга
# ! - Если успею ккал
# ! - Надо поправить, что бы токен не знать
# * - Что то не так с поиском
# ! - Обработка списков
