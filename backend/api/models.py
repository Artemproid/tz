from django.core.validators import MinValueValidator
from django.db import models
from users.models import User  # Импортируем User из users.models

from .constants import (MAX_LENGTH_DEFAULT,
                        MAX_LENGTH_TEN,
                        MAX_LENGTH_EIGHT,
                        MIN_VALIDATE,)


class Status(models.Model):
    """Модель для статусов операций."""
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_DEFAULT
    )
    description = models.TextField(
        'Описание',
        blank=True
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Type(models.Model):
    """Модель для типов операций."""
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_DEFAULT,
        unique=True
    )

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий операций."""
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_DEFAULT
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ['name', 'type']
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.type})'


class Subcategory(models.Model):
    """Модель для подкатегорий операций."""
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_DEFAULT
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        unique_together = ['name', 'category']
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.category})'


class MoneyFlow(models.Model):
    """Модель для записей о движении денежных средств."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='money_flows',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    created_at = models.DateField('Дата создания')
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='money_flows',
        verbose_name='Статус'
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        related_name='money_flows',
        verbose_name='Тип'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='money_flows',
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name='money_flows',
        verbose_name='Подкатегория'
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    comment = models.TextField(
        'Комментарий',
        blank=True
    )

    class Meta:
        verbose_name = 'Движение денежных средств'
        verbose_name_plural = 'Движения денежных средств'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username if self.user else "anon"} - {self.created_at} - {self.type} - {self.amount} руб.'


class StatusOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_statuses')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='owners')

    class Meta:
        unique_together = ('user', 'status')


class TypeOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_types')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='owners')

    class Meta:
        unique_together = ('user', 'type')


class CategoryOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='owners')

    class Meta:
        unique_together = ('user', 'category')


class SubcategoryOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_subcategories')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='owners')

    class Meta:
        unique_together = ('user', 'subcategory')
