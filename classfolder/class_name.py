from telegraph import Telegraph
from telegraph import exceptions

class States:
    S_START = 0  # Начало нового диалога
    S_ENTER_TITLE = 1  # Ввод названия
    S_ENTER_INGREDIENT = 2  # Ввод ингридиентов
    S_ENTER_TEXT = 3  # Ввод рецепта
    S_ENTER_TAG = 4  # Ввод тегов вручную
    S_ADD_RECIPE = 5  # Добавление стороннего рецепта
    S_SEARCH_CHOOSE = 6  # Выбор способа поиска
    S_SEARCH_NAME = 7  # Поиск по названию
    S_SEARCH_TAG = 8  # Поиск по тегам


class Article(object):

    def __init__(self, A_Title, A_Author, A_Ingredient, A_Text, A_Tag):
        self.A_Title = A_Title
        self.A_Author = A_Author
        self.A_Ingredient = A_Ingredient
        self.A_Text = A_Text
        self.A_Tag = A_Tag

    def add_tag(self, A_Tag):
        self.A_Tag += "#" + A_Tag + " "

    def add_ingredient(self, A_Ingredient):
        self.A_Ingredient += "<p>-" + A_Ingredient + "</p>"

    def add_text(self, A_Text):
        if self.A_Text == "empty":
            self.A_Text = "<p>" + A_Text + "</p>"
        else:
            self.A_Text += "<p>" + A_Text + "</p>"

    def re_text(self, A_Text):
        self.A_Text = " "

    def re_title(self, A_Title):
        self.A_Title = A_Title

    def re_name(self, A_Author):
        self.A_Author = A_Author

    def text_erase(self):
        self.A_Text = ""

    def get_title(self):
        return self.A_Title

    def publish_article(self):
        try:
            telegraph = Telegraph()
            telegraph.create_account(short_name=self.A_Author)
            response = telegraph.create_page(
                self.A_Title,
                html_content="<p>Состав: </p>"+self.A_Ingredient \
                            +"<hr>" + self.A_Text \
                             + "<p>" + self.A_Tag + "</p>"
            )
            return 'https://telegra.ph/{}'.format(response['path'])
        except exceptions.TelegraphException as Error:
            print(Error)

    pass