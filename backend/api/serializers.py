from django.db.models import Q
from drf_extra_fields.fields import Base64ImageField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework import serializers

from .models import (
    Status,
    Type,
    Category,
    Subcategory,
    MoneyFlow,
    StatusOwnership,
    TypeOwnership,
    CategoryOwnership,
    SubcategoryOwnership
)
from users.models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Проверка подписки на пользователя."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                subscribed_to=obj
            ).exists()
        return False


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара пользователя."""
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['avatar']


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор для статусов."""
    class Meta:
        model = Status
        fields = ('id', 'name', 'description')


class TypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типов операций."""
    class Meta:
        model = Type
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.none())

    class Meta:
        model = Category
        fields = ('id', 'name', 'type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Фильтруем типы по владению пользователем
            owned_types = Type.objects.filter(owners__user=request.user).distinct()
            self.fields['type'].queryset = owned_types

    def to_representation(self, instance):
        """Добавление имени типа в представление."""
        representation = super().to_representation(instance)
        representation['type_name'] = (
            instance.type.name if instance.type else None
        )
        return representation


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий."""
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Фильтруем категории по владению пользователем
            owned_categories = Category.objects.filter(owners__user=request.user).distinct()
            self.fields['category'].queryset = owned_categories

    def to_representation(self, instance):
        """Добавление имени категории в представление."""
        representation = super().to_representation(instance)
        representation['category_name'] = (
            instance.category.name if instance.category else None
        )
        return representation


class MoneyFlowSerializer(serializers.ModelSerializer):
    """Сериализатор для денежных операций."""
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.none())
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.none())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.none())

    class Meta:
        model = MoneyFlow
        fields = (
            'id',
            'created_at',
            'status',
            'type',
            'category',
            'subcategory',
            'amount',
            'comment'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Фильтруем справочники по владению пользователем
            self.fields['status'].queryset = Status.objects.filter(owners__user=request.user).distinct()
            self.fields['type'].queryset = Type.objects.filter(owners__user=request.user).distinct()
            self.fields['category'].queryset = Category.objects.filter(owners__user=request.user).distinct()
            self.fields['subcategory'].queryset = Subcategory.objects.filter(owners__user=request.user).distinct()

    def to_representation(self, instance):
        """Добавление имен связанных объектов в представление."""
        representation = super().to_representation(instance)
        
        # Используем вложенные сериализаторы для полного представления
        representation['status'] = StatusSerializer(instance.status, context=self.context).data if instance.status else None
        representation['type'] = TypeSerializer(instance.type, context=self.context).data if instance.type else None
        representation['category'] = CategorySerializer(instance.category, context=self.context).data if instance.category else None
        representation['subcategory'] = SubcategorySerializer(instance.subcategory, context=self.context).data if instance.subcategory else None
        
        return representation


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'recipes',
            'recipes_count'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    def get_recipes_count(self, obj):
        """Получение количества рецептов пользователя."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """Получение рецептов пользователя с ограничением."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit') if request else None
        limit = int(limit) if limit and limit.isdigit() else None
        
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:limit]
            
        from .serializers import RecipeShortSerializer
        return RecipeShortSerializer(recipes, many=True, context=self.context).data