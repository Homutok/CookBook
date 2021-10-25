import data.messagebox as messagebox
import functions.site_list as site
from urllib.parse import urlparse
import db.db_functions as db
import classfolder.class_name as data


def add_another_recipe(message, article, bot):
    url = message.text
    domain = urlparse(url)
    if domain.netloc:
        match domain.netloc:
            case 'eda.ru':
                site.eda_ru(message, bot, article, url)
            case 'www.russianfood.com':
                site.russian_food(message, bot, article, url)
            case 'www.povarenok.ru':
                site.povarenok_ru(message, bot, article, url)
            case 'povar.ru':
                site.povar_ru(message, bot, article, url)
            case '1000.menu':
                site.sto_menu(message, bot, article, url)
            case 'www.gastronom.ru':
                site.gastronom(message, bot, article, url)
            case 'www.say7.info':
                site.say7(message, bot, article, url)
            case 'www.edimdoma.ru':
                site.edim_doma(message, bot, article, url)
            case 'hi-chef.ru':
                site.hi_chef(message, bot, article, url)
            case _:
                bot.send_message(message.chat.id, messagebox.msgWrongLink)
    db.db_table_setstate(message.from_user.id, data.States.S_START)


