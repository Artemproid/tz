import pytest
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import transaction

from api.models import MoneyFlow, Status, Type, Category, Subcategory
from api.services import MoneyFlowService, CategoryService, AnalyticsService
from users.models import User


class MoneyFlowServiceTest(TestCase):
    """Тесты для сервиса MoneyFlow."""
    
    def setUp(self):
        """Подготовка тестовых данных."""
        self.service = MoneyFlowService()
        
        # Создаем тестовые объекты
        self.status = Status.objects.create(name='Активный')
        self.type = Type.objects.create(name='Доход')
        self.category = Category.objects.create(name='Зарплата', type=self.type)
        self.subcategory = Subcategory.objects.create(
            name='Основная работа', 
            category=self.category
        )
    
    def test_create_money_flow_success(self):
        """Тест успешного создания денежной операции."""
        data = {
            'created_at': '2024-01-15',
            'status': self.status,
            'type': self.type,
            'category': self.category,
            'subcategory': self.subcategory,
            'amount': Decimal('50000.00'),
            'comment': 'Тестовая операция'
        }
        
        money_flow = self.service.create_money_flow(data)
        
        self.assertIsNotNone(money_flow.id)
        self.assertEqual(money_flow.amount, Decimal('50000.00'))
        self.assertEqual(money_flow.comment, 'Тестовая операция')
    
    def test_create_money_flow_invalid_subcategory(self):
        """Тест создания операции с неподходящей подкатегорией."""
        # Создаем другую категорию и подкатегорию
        other_type = Type.objects.create(name='Расход')
        other_category = Category.objects.create(name='Питание', type=other_type)
        other_subcategory = Subcategory.objects.create(
            name='Ресторан', 
            category=other_category
        )
        
        data = {
            'created_at': '2024-01-15',
            'status': self.status,
            'type': self.type,
            'category': self.category,  # Категория "Зарплата"
            'subcategory': other_subcategory,  # Подкатегория "Ресторан" (не подходит)
            'amount': Decimal('50000.00'),
            'comment': 'Тестовая операция'
        }
        
        with self.assertRaises(ValidationError):
            self.service.create_money_flow(data)
    
    def test_create_money_flow_negative_amount(self):
        """Тест создания операции с отрицательной суммой."""
        data = {
            'created_at': '2024-01-15',
            'status': self.status,
            'type': self.type,
            'category': self.category,
            'subcategory': self.subcategory,
            'amount': Decimal('-1000.00'),  # Отрицательная сумма
            'comment': 'Тестовая операция'
        }
        
        with self.assertRaises(ValidationError):
            self.service.create_money_flow(data)
    
    def test_bulk_create_money_flows(self):
        """Тест массового создания операций."""
        flows_data = [
            {
                'created_at': '2024-01-15',
                'status': self.status,
                'type': self.type,
                'category': self.category,
                'subcategory': self.subcategory,
                'amount': Decimal('10000.00'),
                'comment': 'Операция 1'
            },
            {
                'created_at': '2024-01-16',
                'status': self.status,
                'type': self.type,
                'category': self.category,
                'subcategory': self.subcategory,
                'amount': Decimal('20000.00'),
                'comment': 'Операция 2'
            }
        ]
        
        created_flows = self.service.bulk_create_money_flows(flows_data)
        
        self.assertEqual(len(created_flows), 2)
        self.assertEqual(MoneyFlow.objects.count(), 2)
    
    def test_get_statistics_report(self):
        """Тест получения статистического отчета."""
        # Создаем несколько операций
        MoneyFlow.objects.create(
            created_at='2024-01-15',
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('10000.00')
        )
        MoneyFlow.objects.create(
            created_at='2024-01-16',
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('20000.00')
        )
        
        stats = self.service.get_statistics_report()
        
        self.assertEqual(stats['summary']['total_count'], 2)
        self.assertEqual(stats['summary']['total_amount'], Decimal('30000.00'))
        self.assertEqual(stats['summary']['average_amount'], Decimal('15000.00'))


class CategoryServiceTest(TestCase):
    """Тесты для сервиса Category."""
    
    def setUp(self):
        """Подготовка тестовых данных."""
        self.service = CategoryService()
        self.type = Type.objects.create(name='Доход')
    
    def test_create_category_with_subcategories(self):
        """Тест создания категории с подкатегориями."""
        category_data = {
            'name': 'Зарплата',
            'type': self.type
        }
        subcategories = ['Основная работа', 'Подработка', 'Премия']
        
        category = self.service.create_category_with_subcategories(
            category_data, 
            subcategories
        )
        
        self.assertEqual(category.name, 'Зарплата')
        self.assertEqual(category.subcategories.count(), 3)
        
        subcategory_names = list(
            category.subcategories.values_list('name', flat=True)
        )
        self.assertIn('Основная работа', subcategory_names)
        self.assertIn('Подработка', subcategory_names)
        self.assertIn('Премия', subcategory_names)
    
    def test_get_categories_with_subcategories(self):
        """Тест получения категорий с подкатегориями."""
        # Создаем категорию с подкатегориями
        category = Category.objects.create(name='Зарплата', type=self.type)
        Subcategory.objects.create(name='Основная работа', category=category)
        Subcategory.objects.create(name='Подработка', category=category)
        
        result = self.service.get_categories_with_subcategories()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Зарплата')
        self.assertEqual(len(result[0]['subcategories']), 2)


@pytest.mark.django_db
class TestMoneyFlowServicePytest:
    """Тесты с использованием pytest для более сложных сценариев."""
    
    @pytest.fixture
    def setup_data(self):
        """Фикстура для подготовки данных."""
        status = Status.objects.create(name='Активный')
        type_obj = Type.objects.create(name='Доход')
        category = Category.objects.create(name='Зарплата', type=type_obj)
        subcategory = Subcategory.objects.create(
            name='Основная работа', 
            category=category
        )
        return {
            'status': status,
            'type': type_obj,
            'category': category,
            'subcategory': subcategory
        }
    
    def test_transaction_rollback_on_error(self, setup_data):
        """Тест отката транзакции при ошибке."""
        service = MoneyFlowService()
        
        # Первая операция - валидная
        valid_data = {
            'created_at': '2024-01-15',
            'status': setup_data['status'],
            'type': setup_data['type'],
            'category': setup_data['category'],
            'subcategory': setup_data['subcategory'],
            'amount': Decimal('10000.00'),
        }
        
        # Создаем другую категорию для невалидной подкатегории
        other_type = Type.objects.create(name='Расход')
        other_category = Category.objects.create(name='Питание', type=other_type)
        other_subcategory = Subcategory.objects.create(
            name='Ресторан', 
            category=other_category
        )
        
        # Вторая операция - с ошибкой
        invalid_data = {
            'created_at': '2024-01-16',
            'status': setup_data['status'],
            'type': setup_data['type'],
            'category': setup_data['category'],
            'subcategory': other_subcategory,  # Неподходящая подкатегория
            'amount': Decimal('20000.00'),
        }
        
        flows_data = [valid_data, invalid_data]
        
        # Проверяем, что транзакция откатывается при ошибке
        with pytest.raises(ValidationError):
            service.bulk_create_money_flows(flows_data)
        
        # Проверяем, что ни одна операция не была создана
        assert MoneyFlow.objects.count() == 0
    
    @pytest.mark.parametrize("amount,should_raise", [
        (Decimal('100.00'), False),
        (Decimal('0.01'), False),
        (Decimal('0'), True),
        (Decimal('-100.00'), True),
    ])
    def test_amount_validation(self, setup_data, amount, should_raise):
        """Параметризованный тест валидации суммы."""
        service = MoneyFlowService()
        
        data = {
            'created_at': '2024-01-15',
            'status': setup_data['status'],
            'type': setup_data['type'],
            'category': setup_data['category'],
            'subcategory': setup_data['subcategory'],
            'amount': amount,
        }
        
        if should_raise:
            with pytest.raises(ValidationError):
                service.create_money_flow(data)
        else:
            money_flow = service.create_money_flow(data)
            assert money_flow.amount == amount 