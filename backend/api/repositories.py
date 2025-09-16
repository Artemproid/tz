from abc import ABC, abstractmethod
from typing import List, Optional
from django.db.models import QuerySet
from .models import MoneyFlow, Status, Type, Category, Subcategory


class BaseRepository(ABC):
    """Базовый абстрактный класс для репозиториев."""
    
    @abstractmethod
    def get_all(self) -> QuerySet:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int):
        pass
    
    @abstractmethod
    def create(self, **kwargs):
        pass
    
    @abstractmethod
    def update(self, id: int, **kwargs):
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class MoneyFlowRepository(BaseRepository):
    """Репозиторий для работы с денежными операциями."""
    
    def get_all(self) -> QuerySet:
        return MoneyFlow.objects.select_related(
            'user', 'status', 'type', 'category', 'subcategory'
        ).all()
    
    def get_by_user(self, user) -> QuerySet:
        """Получение всех операций конкретного пользователя."""
        return self.get_all().filter(user=user)
    
    def get_by_id(self, id: int, user=None) -> Optional[MoneyFlow]:
        """Получение операции по ID с проверкой принадлежности пользователю."""
        try:
            queryset = MoneyFlow.objects.select_related(
                'user', 'status', 'type', 'category', 'subcategory'
            )
            if user:
                queryset = queryset.filter(user=user)
            return queryset.get(id=id)
        except MoneyFlow.DoesNotExist:
            return None
    
    def create(self, **kwargs) -> MoneyFlow:
        return MoneyFlow.objects.create(**kwargs)
    
    def update(self, id: int, **kwargs) -> Optional[MoneyFlow]:
        try:
            money_flow = MoneyFlow.objects.get(id=id)
            for key, value in kwargs.items():
                setattr(money_flow, key, value)
            money_flow.save()
            return money_flow
        except MoneyFlow.DoesNotExist:
            return None
    
    def delete(self, id: int) -> bool:
        try:
            MoneyFlow.objects.get(id=id).delete()
            return True
        except MoneyFlow.DoesNotExist:
            return False
    
    def get_by_date_range(self, user=None, start_date=None, end_date=None) -> QuerySet:
        """Получение операций по диапазону дат для конкретного пользователя."""
        if user:
            queryset = self.get_by_user(user)
        else:
            queryset = self.get_all()
            
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        return queryset.order_by('-created_at')
    
    def get_by_category(self, category_id: int, user=None) -> QuerySet:
        """Получение операций по категории для конкретного пользователя."""
        if user:
            return self.get_by_user(user).filter(category_id=category_id)
        return self.get_all().filter(category_id=category_id)
    
    def get_statistics(self, user=None):
        """Получение статистики по операциям для конкретного пользователя."""
        from django.db.models import Sum, Count
        
        if user:
            queryset = self.get_by_user(user)
        else:
            queryset = self.get_all()
            
        return {
            'total_count': queryset.count(),
            'total_amount': queryset.aggregate(Sum('amount'))['amount__sum'] or 0,
            'by_type': queryset.values('type__name').annotate(
                count=Count('id'),
                total=Sum('amount')
            )
        }


class CategoryRepository(BaseRepository):
    """Репозиторий для работы с категориями."""
    
    def get_all(self) -> QuerySet:
        return Category.objects.select_related('type').all()
    
    def get_by_id(self, id: int) -> Optional[Category]:
        try:
            return Category.objects.select_related('type').get(id=id)
        except Category.DoesNotExist:
            return None
    
    def create(self, **kwargs) -> Category:
        return Category.objects.create(**kwargs)
    
    def update(self, id: int, **kwargs) -> Optional[Category]:
        try:
            category = Category.objects.get(id=id)
            for key, value in kwargs.items():
                setattr(category, key, value)
            category.save()
            return category
        except Category.DoesNotExist:
            return None
    
    def delete(self, id: int) -> bool:
        try:
            Category.objects.get(id=id).delete()
            return True
        except Category.DoesNotExist:
            return False
    
    def get_by_type(self, type_id: int) -> QuerySet:
        """Получение категорий по типу."""
        return self.get_all().filter(type_id=type_id) 