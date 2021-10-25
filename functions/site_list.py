from bs4 import BeautifulSoup
import db.db_functions as db_function
import requests

tag = []


def eda_ru(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('span', itemprop='name')
    ingredients = soup.findAll('span', itemprop='recipeIngredient')
    ingredients_weight = soup.findAll('span', 'css-1t5teuh-Info')
    text = soup.findAll('span', itemprop='text')
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, text, ingredients, ingredients_weight))


def russian_food(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('h1', 'title')
    ingredients = soup.findAll('table', 'ingr')

    rows = ingredients[0].find_all('tr')
    ingredients = list()
    ingredients_weight = list()
    listtext = list()
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    for item in data:
        if not 'Продукты' in item[0]:
            ingredients.append(item[0].partition('-')[0])
            ingredients_weight.append(item[0].partition('-')[2])
    text = soup.findAll('div', 'step_n')
    for item in text:
        listtext.append(item.find('p'))
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, listtext, ingredients, ingredients_weight))
    pass


def povarenok_ru(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('h1')
    ingredient_list = soup.findAll('span', itemprop='ingredient')
    ingredients = list()
    ingredients_weight = list()
    for element in ingredient_list:
        ingredients.append(element.find('span', itemprop='name').text)
        if element.find('span', itemprop='amount'):
            ingredients_weight.append(element.find('span', itemprop='amount').text)
        else:
            ingredients_weight.append(" ")
    text = soup.findAll('div', itemprop='recipeInstructions')
    listtext = list()
    for elem in text:
        listtext.append(elem)
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, listtext, ingredients, ingredients_weight))
    pass


def povar_ru(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('h1', 'detailed')
    ingredient = soup.findAll('li', itemprop='recipeIngredient')
    ingredients = list()
    ingredients_weight = list()
    for element in ingredient:
        all_ingr = ' '.join(element.text.split())
        ingredients.append(all_ingr.partition('—')[0])
        ingredients_weight.append(all_ingr.partition('—')[2])
    text = soup.findAll('div', 'detailed_step_description_big')
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, text, ingredients, ingredients_weight))


def sto_menu(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    name = soup.findAll('h1', itemprop='name')
    ingredients_html = soup.findAll('a', 'name')
    ingredients_weight_html = soup.findAll('span', 'squant value')

    ingredients = list()
    ingredients_weight = list()
    for index, ingredient in enumerate(ingredients_html):
        ingredients.append(' '.join(ingredient.text.split()))
        ingredients_weight.append(' '.join(ingredients_weight_html[index].text.split()))
    text = soup.findAll('p', 'instruction')
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, text, ingredients, ingredients_weight))


def gastronom(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('h1', 'recipe__title')
    ingredient = soup.findAll('li', itemprop='recipeIngredient')

    ingredients = list()
    ingredients_weight = list()

    for element in ingredient:
        all_ingr = ' '.join(element.text.split())
        ingredients.append(all_ingr.partition('—')[0])
        ingredients_weight.append(all_ingr.partition('—')[2])
    text = soup.findAll('div', 'recipe__step-text')
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, text, ingredients, ingredients_weight))


def say7(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('h1', itemprop='name')
    ingredient = soup.findAll('li', itemprop='recipeIngredient')

    ingredients = list()
    ingredients_weight = list()

    for element in ingredient:
        all_ingr = ' '.join(element.text.split())
        ingredients.append(all_ingr.partition('—')[0])
        ingredients_weight.append(all_ingr.partition('—')[2])
    text = soup.findAll('p',itemprop='recipeInstructions')
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, text, ingredients, ingredients_weight))


def edim_doma(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('h1', itemprop='name')
    ingredient = soup.findAll('span', 'recipe_ingredient_title')

    ingredients = list()
    ingredients_weight = list()

    for element in ingredient:
        all_ingr = ' '.join(element.text.split())
        ingredients.append(all_ingr.partition('—')[0])
        ingredients_weight.append(all_ingr.partition('—')[2])
    text = soup.findAll('p', itemprop='recipeInstructions')
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, text, ingredients, ingredients_weight))


def hi_chef(message, bot, article, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.findAll('h1', itemprop="name")
    ingredients = soup.findAll('div', itemprop='recipeIngredient')
    ingredients_weight = soup.findAll('span', '_42d3fbd880')
    text = soup.findAll('div', itemprop='recipeInstructions')
    bot.send_message(message.chat.id,
                     public(message, article, name[0].text, text, ingredients, ingredients_weight))


def public(message, article, name, text, ingredients, ingredients_weight):
    for index, ingredient in enumerate(ingredients):
        try:
            article.add_ingredient(ingredient.text + " - " + ingredients_weight[index].text)
            tag.append(ingredient.text)
        except:
            article.add_ingredient(ingredient + " - " + ingredients_weight[index])
            tag.append(ingredient)
    for step in text:
        article.add_text(step.text)

    article.re_title(name)  # Имя
    article.re_name(message.from_user.username)
    article.publish_article()

    link = article.publish_article()
    db_function.db_table_set_link(message.from_user.id, article.A_Title, link)
    set_tags(db_function.db_table_get_last_index(link, message.from_user.id))
    return link


def set_tags(article_id):
    for item in range(0, len(tag)):
        db_function.db_table_set_all_tag(article_id, tag[item].lower())
    tag.clear()
