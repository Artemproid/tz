#!/usr/bin/env python
"""
Скрипт для загрузки тестовых данных в систему управления финансами.
Создает пользователей, справочники и денежные операции для демонстрации.
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import Status, Type, Category, Subcategory, MoneyFlow

User = get_user_model()

def create_users():
    """Создание тестовых пользователей."""
    print("🧑‍💼 Создание пользователей...")
    
    users_data = [
        {
            'username': 'alice_manager',
            'email': 'alice@example.com',
            'first_name': 'Алиса',
            'last_name': 'Менеджер',
            'password': 'testpass123'
        },
        {
            'username': 'bob_developer',
            'email': 'bob@example.com',
            'first_name': 'Боб',
            'last_name': 'Разработчик',
            'password': 'testpass123'
        },
        {
            'username': 'carol_designer',
            'email': 'carol@example.com',
            'first_name': 'Кэрол',
            'last_name': 'Дизайнер',
            'password': 'testpass123'
        },
        {
            'username': 'demo_user',
            'email': 'demo@example.com',
            'first_name': 'Демо',
            'last_name': 'Пользователь',
            'password': 'demo123'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"  ✅ Создан пользователь: {user.username} ({user.email})")
        else:
            print(f"  ℹ️  Пользователь уже существует: {user.username}")
        
        created_users.append(user)
    
    return created_users

def create_reference_data():
    """Создание справочных данных."""
    print("\n📋 Создание справочников...")
    
    # Статусы
    statuses_data = [
        {'name': 'Активный', 'description': 'Подтвержденная операция'},
        {'name': 'В ожидании', 'description': 'Операция ожидает подтверждения'},
        {'name': 'Отменен', 'description': 'Отмененная операция'},
        {'name': 'Запланирован', 'description': 'Запланированная операция'}
    ]
    
    statuses = []
    for status_data in statuses_data:
        status, created = Status.objects.get_or_create(
            name=status_data['name'],
            defaults={'description': status_data['description']}
        )
        statuses.append(status)
        if created:
            print(f"  ✅ Создан статус: {status.name}")
    
    # Типы операций
    types_data = [
        {'name': 'Доход'},
        {'name': 'Расход'},
        {'name': 'Перевод'},
        {'name': 'Инвестиции'}
    ]
    
    types = []
    for type_data in types_data:
        type_obj, created = Type.objects.get_or_create(
            name=type_data['name']
        )
        types.append(type_obj)
        if created:
            print(f"  ✅ Создан тип: {type_obj.name}")
    
    # Категории и подкатегории
    categories_data = {
        'Доходы': {
            'type': 'Доход',
            'subcategories': ['Зарплата', 'Премия', 'Фриланс', 'Инвестиции', 'Подарки']
        },
        'Питание': {
            'type': 'Расход',
            'subcategories': ['Продукты', 'Рестораны', 'Кафе', 'Доставка еды']
        },
        'Транспорт': {
            'type': 'Расход',
            'subcategories': ['Общественный транспорт', 'Такси', 'Бензин', 'Парковка']
        },
        'Жилье': {
            'type': 'Расход',
            'subcategories': ['Аренда', 'Коммунальные услуги', 'Ремонт', 'Мебель']
        },
        'Развлечения': {
            'type': 'Расход',
            'subcategories': ['Кино', 'Концерты', 'Игры', 'Хобби']
        },
        'Здоровье': {
            'type': 'Расход',
            'subcategories': ['Врачи', 'Лекарства', 'Фитнес', 'Косметика']
        },
        'Образование': {
            'type': 'Расход',
            'subcategories': ['Курсы', 'Книги', 'Конференции', 'Сертификации']
        }
    }
    
    categories = []
    for category_name, category_info in categories_data.items():
        # Найти тип
        type_obj = next(t for t in types if t.name == category_info['type'])
        
        # Создать категорию
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'type': type_obj}
        )
        categories.append(category)
        if created:
            print(f"  ✅ Создана категория: {category.name}")
        
        # Создать подкатегории
        for subcategory_name in category_info['subcategories']:
            subcategory, created = Subcategory.objects.get_or_create(
                name=subcategory_name,
                defaults={'category': category}
            )
            if created:
                print(f"    ✅ Создана подкатегория: {subcategory.name}")
    
    return statuses, types, categories

def create_money_flows(users, statuses, categories):
    """Создание тестовых денежных операций."""
    print("\n💰 Создание денежных операций...")
    
    # Шаблоны операций для разных пользователей
    operations_templates = {
        'alice_manager': [
            # Доходы
            {'category': 'Доходы', 'subcategory': 'Зарплата', 'amount_range': (80000, 120000), 'frequency': 'monthly'},
            {'category': 'Доходы', 'subcategory': 'Премия', 'amount_range': (20000, 50000), 'frequency': 'quarterly'},
            # Расходы
            {'category': 'Жилье', 'subcategory': 'Аренда', 'amount_range': (30000, 35000), 'frequency': 'monthly'},
            {'category': 'Питание', 'subcategory': 'Продукты', 'amount_range': (8000, 12000), 'frequency': 'weekly'},
            {'category': 'Транспорт', 'subcategory': 'Бензин', 'amount_range': (3000, 5000), 'frequency': 'weekly'},
            {'category': 'Развлечения', 'subcategory': 'Рестораны', 'amount_range': (2000, 8000), 'frequency': 'weekly'},
        ],
        'bob_developer': [
            # Доходы
            {'category': 'Доходы', 'subcategory': 'Зарплата', 'amount_range': (100000, 150000), 'frequency': 'monthly'},
            {'category': 'Доходы', 'subcategory': 'Фриланс', 'amount_range': (15000, 30000), 'frequency': 'monthly'},
            # Расходы
            {'category': 'Жилье', 'subcategory': 'Коммунальные услуги', 'amount_range': (5000, 8000), 'frequency': 'monthly'},
            {'category': 'Питание', 'subcategory': 'Доставка еды', 'amount_range': (1500, 3000), 'frequency': 'weekly'},
            {'category': 'Образование', 'subcategory': 'Курсы', 'amount_range': (5000, 15000), 'frequency': 'monthly'},
            {'category': 'Развлечения', 'subcategory': 'Игры', 'amount_range': (1000, 3000), 'frequency': 'weekly'},
        ],
        'carol_designer': [
            # Доходы
            {'category': 'Доходы', 'subcategory': 'Фриланс', 'amount_range': (50000, 80000), 'frequency': 'monthly'},
            {'category': 'Доходы', 'subcategory': 'Подарки', 'amount_range': (3000, 10000), 'frequency': 'rarely'},
            # Расходы
            {'category': 'Питание', 'subcategory': 'Кафе', 'amount_range': (500, 1500), 'frequency': 'daily'},
            {'category': 'Транспорт', 'subcategory': 'Общественный транспорт', 'amount_range': (2000, 3000), 'frequency': 'monthly'},
            {'category': 'Здоровье', 'subcategory': 'Косметика', 'amount_range': (2000, 5000), 'frequency': 'monthly'},
            {'category': 'Развлечения', 'subcategory': 'Кино', 'amount_range': (800, 1200), 'frequency': 'weekly'},
        ],
        'demo_user': [
            # Простые операции для демо
            {'category': 'Доходы', 'subcategory': 'Зарплата', 'amount_range': (45000, 55000), 'frequency': 'monthly'},
            {'category': 'Питание', 'subcategory': 'Продукты', 'amount_range': (3000, 6000), 'frequency': 'weekly'},
            {'category': 'Транспорт', 'subcategory': 'Такси', 'amount_range': (300, 800), 'frequency': 'weekly'},
            {'category': 'Развлечения', 'subcategory': 'Концерты', 'amount_range': (1500, 3000), 'frequency': 'rarely'},
        ]
    }
    
    # Генерация операций за последние 6 месяцев
    start_date = datetime.now() - timedelta(days=180)
    end_date = datetime.now()
    
    active_status = statuses[0]  # Активный статус
    
    created_count = 0
    
    for user in users:
        user_templates = operations_templates.get(user.username, operations_templates['demo_user'])
        
        print(f"\n  👤 Создание операций для {user.first_name} {user.last_name}:")
        
        current_date = start_date
        while current_date <= end_date:
            for template in user_templates:
                # Определяем, нужно ли создавать операцию в эту дату
                should_create = False
                
                if template['frequency'] == 'daily':
                    should_create = random.random() < 0.7  # 70% вероятность
                elif template['frequency'] == 'weekly':
                    should_create = current_date.weekday() == 1 and random.random() < 0.8  # Вторник, 80%
                elif template['frequency'] == 'monthly':
                    should_create = current_date.day == 1 and random.random() < 0.9  # 1 число, 90%
                elif template['frequency'] == 'quarterly':
                    should_create = current_date.day == 1 and current_date.month in [1, 4, 7, 10] and random.random() < 0.7
                elif template['frequency'] == 'rarely':
                    should_create = random.random() < 0.05  # 5% вероятность
                
                if should_create:
                    # Найти категорию и подкатегорию
                    try:
                        category = Category.objects.get(name=template['category'])
                        subcategory = Subcategory.objects.get(
                            name=template['subcategory'],
                            category=category
                        )
                        
                        # Генерировать сумму
                        min_amount, max_amount = template['amount_range']
                        amount = Decimal(str(random.randint(min_amount, max_amount)))
                        
                        # Создать операцию
                        money_flow = MoneyFlow.objects.create(
                            user=user,
                            created_at=current_date.date(),
                            status=active_status,
                            type=category.type,
                            category=category,
                            subcategory=subcategory,
                            amount=amount,
                            comment=f"Автоматически созданная операция: {subcategory.name}"
                        )
                        
                        created_count += 1
                        
                    except (Category.DoesNotExist, Subcategory.DoesNotExist) as e:
                        print(f"    ⚠️ Ошибка: {e}")
            
            current_date += timedelta(days=1)
        
        user_operations = MoneyFlow.objects.filter(user=user).count()
        print(f"    ✅ Создано операций: {user_operations}")
    
    print(f"\n💰 Всего создано операций: {created_count}")
    return created_count

def create_sample_comments():
    """Добавление реалистичных комментариев к операциям."""
    print("\n💬 Добавление комментариев к операциям...")
    
    comments_by_subcategory = {
        'Зарплата': [
            'Зарплата за месяц',
            'Основная зарплата',
            'Зарплата + переработки',
            'Заработная плата'
        ],
        'Продукты': [
            'Закупка продуктов на неделю',
            'Поход в супермаркет',
            'Продукты в Пятерочке',
            'Еда на дом',
            'Овощи и фрукты на рынке'
        ],
        'Кафе': [
            'Кофе с коллегами',
            'Обед в кафе рядом с работой',
            'Встреча с друзьями в кафе',
            'Кофе-брейк',
            'Завтрак в кафе'
        ],
        'Такси': [
            'Поездка на работу',
            'Такси домой после работы',
            'Поездка в аэропорт',
            'Такси в дождь',
            'Срочная поездка'
        ],
        'Бензин': [
            'Заправка полного бака',
            'Заправка на АЗС',
            'Топливо для поездки',
            'Заправка машины'
        ],
        'Рестораны': [
            'Ужин в ресторане',
            'День рождения друга',
            'Романтический ужин',
            'Деловой обед',
            'Семейный ужин'
        ]
    }
    
    flows = MoneyFlow.objects.filter(
        comment__startswith='Автоматически созданная операция'
    )
    
    updated_count = 0
    for flow in flows:
        subcategory_name = flow.subcategory.name
        if subcategory_name in comments_by_subcategory:
            new_comment = random.choice(comments_by_subcategory[subcategory_name])
            flow.comment = new_comment
            flow.save()
            updated_count += 1
    
    print(f"  ✅ Обновлено комментариев: {updated_count}")

def print_summary():
    """Вывод сводной информации."""
    print("\n📊 СВОДКА СОЗДАННЫХ ДАННЫХ:")
    print("=" * 50)
    
    # Пользователи
    users_count = User.objects.count()
    print(f"👥 Пользователей: {users_count}")
    
    # Справочники
    statuses_count = Status.objects.count()
    types_count = Type.objects.count()
    categories_count = Category.objects.count()
    subcategories_count = Subcategory.objects.count()
    
    print(f"📋 Справочники:")
    print(f"   - Статусов: {statuses_count}")
    print(f"   - Типов операций: {types_count}")
    print(f"   - Категорий: {categories_count}")
    print(f"   - Подкатегорий: {subcategories_count}")
    
    # Операции по пользователям
    print(f"💰 Операции по пользователям:")
    for user in User.objects.all():
        operations_count = MoneyFlow.objects.filter(user=user).count()
        if operations_count > 0:
            total_income = MoneyFlow.objects.filter(
                user=user, 
                type__name='Доход'
            ).aggregate(total=django.db.models.Sum('amount'))['total'] or 0
            
            total_expense = MoneyFlow.objects.filter(
                user=user, 
                type__name='Расход'
            ).aggregate(total=django.db.models.Sum('amount'))['total'] or 0
            
            print(f"   - {user.first_name} {user.last_name}: {operations_count} операций")
            print(f"     Доходы: {total_income:,.2f} ₽, Расходы: {total_expense:,.2f} ₽")
    
    total_operations = MoneyFlow.objects.count()
    print(f"\n💰 Всего операций в системе: {total_operations}")

def main():
    """Основная функция загрузки тестовых данных."""
    print("🚀 ЗАГРУЗКА ТЕСТОВЫХ ДАННЫХ")
    print("=" * 50)
    
    try:
        # Создание данных
        users = create_users()
        statuses, types, categories = create_reference_data()
        create_money_flows(users, statuses, categories)
        create_sample_comments()
        
        # Сводка
        print_summary()
        
        print("\n🎉 ДАННЫЕ УСПЕШНО ЗАГРУЖЕНЫ!")
        print("\n🔑 Данные для входа:")
        print("   Email: alice@example.com, Пароль: testpass123")
        print("   Email: bob@example.com, Пароль: testpass123") 
        print("   Email: carol@example.com, Пароль: testpass123")
        print("   Email: demo@example.com, Пароль: demo123")
        
        print("\n🌐 Для тестирования:")
        print("   1. Откройте http://localhost:8000/")
        print("   2. Зарегистрируйтесь или войдите с данными выше")
        print("   3. Просмотрите операции каждого пользователя")
        print("   4. API документация: http://localhost:8000/api/swagger/")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 