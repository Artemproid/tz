from typing import Dict, List, Optional
from decimal import Decimal
from datetime import date, datetime
from django.db import transaction
from django.core.exceptions import ValidationError

from .repositories import MoneyFlowRepository, CategoryRepository
from .models import MoneyFlow, Category, Subcategory


class MoneyFlowService:
    """Сервис для работы с денежными операциями."""
    
    def __init__(self):
        self.repository = MoneyFlowRepository()
    
    def create_money_flow(self, data: Dict, user) -> MoneyFlow:
        """Создание новой денежной операции с валидацией."""
        with transaction.atomic():
            data['user'] = user
            
            if data.get('subcategory') and data.get('category'):
                subcategory = data['subcategory']
                category = data['category']
                if subcategory.category != category:
                    raise ValidationError(
                        'Подкатегория должна принадлежать выбранной категории'
                    )
            
            if data.get('amount') and data['amount'] <= 0:
                raise ValidationError('Сумма должна быть больше 0')
            
            return self.repository.create(**data)
    
    def update_money_flow(self, id: int, data: Dict, user) -> Optional[MoneyFlow]:
        """Обновление денежной операции с валидацией."""
        with transaction.atomic():

            existing_flow = self.repository.get_by_id(id, user=user)
            if not existing_flow:
                raise ValidationError('Операция не найдена или не принадлежит пользователю')
            
            if data.get('subcategory') and data.get('category'):
                subcategory = data['subcategory']
                category = data['category']
                if subcategory.category != category:
                    raise ValidationError(
                        'Подкатегория должна принадлежать выбранной категории'
                    )
            
            if data.get('amount') and data['amount'] <= 0:
                raise ValidationError('Сумма должна быть больше 0')
            
            if 'user' in data:
                del data['user']
            
            return self.repository.update(id, **data)
    
    def get_filtered_money_flows(self, filters: Dict, user):
        """Получение отфильтрованных денежных операций для конкретного пользователя."""
        queryset = self.repository.get_by_user(user)
        
        if filters.get('start_date'):
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        if filters.get('end_date'):
            queryset = queryset.filter(created_at__lte=filters['end_date'])
        
        if filters.get('status'):
            queryset = queryset.filter(status__name__icontains=filters['status'])
        
        if filters.get('type'):
            queryset = queryset.filter(type__name__icontains=filters['type'])
        
        if filters.get('category'):
            queryset = queryset.filter(category__name__icontains=filters['category'])
        
        return queryset.order_by('-created_at')
    
    def get_statistics_report(self, user, start_date=None, end_date=None) -> Dict:
        """Получение отчета по статистике операций для конкретного пользователя."""
        queryset = self.repository.get_by_date_range(user, start_date, end_date)
        
        from django.db.models import Sum, Count, Avg
        
        stats = queryset.aggregate(
            total_count=Count('id'),
            total_amount=Sum('amount'),
            average_amount=Avg('amount')
        )
        
        type_stats = queryset.values('type__name').annotate(
            count=Count('id'),
            total=Sum('amount')
        ).order_by('-total')
        
        category_stats = queryset.values('category__name').annotate(
            count=Count('id'),
            total=Sum('amount')
        ).order_by('-total')
        
        return {
            'summary': stats,
            'by_type': list(type_stats),
            'by_category': list(category_stats),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
    
    def bulk_create_money_flows(self, flows_data: List[Dict], user) -> List[MoneyFlow]:
        """Массовое создание денежных операций для конкретного пользователя."""
        with transaction.atomic():
            validated_flows = []
            for flow_data in flows_data:
                flow_data['user'] = user
                
                if flow_data.get('subcategory') and flow_data.get('category'):
                    subcategory = flow_data['subcategory']
                    category = flow_data['category']
                    if subcategory.category != category:
                        raise ValidationError(
                            f'Подкатегория {subcategory.name} не принадлежит категории {category.name}'
                        )
                
                if flow_data.get('amount') and flow_data['amount'] <= 0:
                    raise ValidationError('Все суммы должны быть больше 0')
                
                validated_flows.append(MoneyFlow(**flow_data))
            
            return MoneyFlow.objects.bulk_create(validated_flows)


class CategoryService:
    """Сервис для работы с категориями."""
    
    def __init__(self):
        self.repository = CategoryRepository()
    
    def create_category_with_subcategories(self, category_data: Dict, subcategories: List[str]) -> Category:
        """Создание категории с подкатегориями."""
        with transaction.atomic():
            category = self.repository.create(**category_data)
            
            subcategory_objects = []
            for subcategory_name in subcategories:
                subcategory_objects.append(
                    Subcategory(name=subcategory_name, category=category)
                )
            
            Subcategory.objects.bulk_create(subcategory_objects)
            return category
    
    def get_categories_with_subcategories(self, type_id: int = None):
        """Получение категорий с подкатегориями."""
        categories = self.repository.get_by_type(type_id) if type_id else self.repository.get_all()
        
        result = []
        for category in categories:
            subcategories = list(category.subcategories.all().values('id', 'name'))
            result.append({
                'id': category.id,
                'name': category.name,
                'type': {
                    'id': category.type.id,
                    'name': category.type.name
                },
                'subcategories': subcategories
            })
        
        return result


class AnalyticsService:
    """Сервис для аналитики и отчетности."""
    
    def __init__(self):
        self.money_flow_repository = MoneyFlowRepository()
    
    def get_monthly_report(self, year: int, month: int) -> Dict:
        """Получение месячного отчета."""
        from calendar import monthrange
        
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])
        
        return self.money_flow_repository.get_statistics()
    
    def get_trend_analysis(self, months: int = 6) -> Dict:
        """Анализ трендов за последние месяцы."""
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        
        end_date = date.today()
        start_date = end_date - relativedelta(months=months)
        
        queryset = self.money_flow_repository.get_by_date_range(start_date, end_date)
        
        from django.db.models import Sum, Count
        from django.db.models.functions import TruncMonth
        
        monthly_data = queryset.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            count=Count('id'),
            total=Sum('amount')
        ).order_by('month')
        
        return {
            'period': f'{start_date} - {end_date}',
            'monthly_breakdown': list(monthly_data)
        } 