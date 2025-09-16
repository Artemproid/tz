from django.core.management.base import BaseCommand
from api.models import Status, Type, Category, Subcategory

class Command(BaseCommand):
    help = 'Загружает начальные данные для денежных потоков'

    def handle(self, *args, **kwargs):
        # Создаем статусы
        status_business = Status.objects.create(name='Бизнес')
        status_personal = Status.objects.create(name='Личное')
        
        # Создаем типы
        type_income = Type.objects.create(name='Доход')
        type_expense = Type.objects.create(name='Расход')
        
        # Создаем категории для доходов
        cat_salary = Category.objects.create(name='Зарплата', type=type_income)
        cat_investment = Category.objects.create(name='Инвестиции', type=type_income)
        
        # Создаем категории для расходов
        cat_food = Category.objects.create(name='Питание', type=type_expense)
        cat_transport = Category.objects.create(name='Транспорт', type=type_expense)
        
        # Создаем подкатегории
        Subcategory.objects.create(name='Основная работа', category=cat_salary)
        Subcategory.objects.create(name='Подработка', category=cat_salary)
        
        Subcategory.objects.create(name='Дивиденды', category=cat_investment)
        Subcategory.objects.create(name='Проценты по вкладам', category=cat_investment)
        
        Subcategory.objects.create(name='Продукты', category=cat_food)
        Subcategory.objects.create(name='Рестораны', category=cat_food)
        
        Subcategory.objects.create(name='Такси', category=cat_transport)
        Subcategory.objects.create(name='Общественный транспорт', category=cat_transport)

        self.stdout.write('Данные успешно загружены! 🎉')