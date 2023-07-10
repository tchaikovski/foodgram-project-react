from csv import DictReader
from django.core.management import BaseCommand
from recipes.models import Ingredient


ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py migrate` для новой пустой
базы данных с таблицам"""


class Command(BaseCommand):
    # Показывать это, когда пользователь вводит справку
    help = "Загружает данные из файла ingredients.csv"

    def handle(self, *args, **options):
        # Показывать это, если данные уже существуют в базе данных
        if Ingredient.objects.exists():
            print('данные уже загружены...выход.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        # Показывать это перед загрузкой данных в базу данных
        print("Загрузка данных ингредиентов")

        # Код для загрузки данных в базу данных
        for row in DictReader(open('./ingredients.csv')):
            ing = Ingredient(name=row[0],
                             measurement_unit=row[1])
            ing.save()
