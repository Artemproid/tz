from djoser.views import UserViewSet
from rest_framework import (status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django.db import transaction

from .models import (MoneyFlow,
                     Status, Type, Category, Subcategory,
                     StatusOwnership, TypeOwnership, CategoryOwnership, SubcategoryOwnership)
from .serializers import (StatusSerializer, TypeSerializer, CategorySerializer,
                          SubcategorySerializer, MoneyFlowSerializer,
                          AvatarSerializer)
from .serializers import UserSerializer
from .pagination import CustomPagination
from users.models import User, Subscription


class MyUserViewSet(UserViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Получение данных текущего пользователя."""
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        url_path='me/avatar',
        methods=['put', 'delete'],
        serializer_class=AvatarSerializer,
        permission_classes=[IsAuthenticated]
    )
    def avatar(self, request):
        """Обновление или удаление аватара пользователя."""
        if request.method == 'PUT':
            serializer = AvatarSerializer(
                instance=request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid() and request.data:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        url_path='subscriptions',
        pagination_class=CustomPagination,
    )
    def get_subscriptions(self, *args, **kwargs):
        subscriptions_list = Subscription.objects.filter(
            user=self.request.user)
        use1r = []
        for i in subscriptions_list:
            new_user = UserSerializer(i.subscribed_to).data
            new_user['is_subscribed'] = True
            if 'recipes_limit' in self.request.GET:
                new_user['limit'] = self.request.GET['recipes_limit']
            use1r.append(new_user)
        paginator = self.paginator
        result_page = paginator.paginate_queryset(use1r, self.request)
        serializer = SubscribeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MoneyFlowFilter(filters.FilterSet):
    """Фильтр для денежных операций."""
    created_at = filters.DateFilter(field_name='created_at')
    status = filters.CharFilter(
        field_name='status__name',
        lookup_expr='icontains'
    )
    type = filters.CharFilter(
        field_name='type__name',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains'
    )
    subcategory = filters.CharFilter(
        field_name='subcategory__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = MoneyFlow
        fields = ['created_at', 'status', 'type', 'category', 'subcategory']


class StatusViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы со статусами (глобальный, read-only для анонимов)."""
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Status.objects.all()


class TypeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с типами операций (глобальный, read-only для анонимов)."""
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Type.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с категориями (глобальный, read-only для анонимов)."""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()


class SubcategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с подкатегориями (глобальный, read-only для анонимов)."""
    serializer_class = SubcategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Subcategory.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class MyStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.filter(owners__user=self.request.user).distinct()

    @transaction.atomic
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        status_obj, _ = Status.objects.get_or_create(name=name)
        StatusOwnership.objects.get_or_create(user=self.request.user, status=status_obj)
        serializer.instance = status_obj

    @transaction.atomic
    def perform_destroy(self, instance):
        StatusOwnership.objects.filter(user=self.request.user, status=instance).delete()
        if not instance.owners.exists():
            instance.delete()


class MyTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TypeSerializer

    def get_queryset(self):
        return Type.objects.filter(owners__user=self.request.user).distinct()

    @transaction.atomic
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        type_obj, _ = Type.objects.get_or_create(name=name)
        TypeOwnership.objects.get_or_create(user=self.request.user, type=type_obj)
        serializer.instance = type_obj

    @transaction.atomic
    def perform_destroy(self, instance):
        TypeOwnership.objects.filter(user=self.request.user, type=instance).delete()
        if not instance.owners.exists():
            instance.delete()


class MyCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(owners__user=self.request.user).distinct()

    @transaction.atomic
    def perform_create(self, serializer):
        type_obj = serializer.validated_data.get('type')
        # Разрешаем использовать только типы, принадлежащие пользователю
        if not TypeOwnership.objects.filter(user=self.request.user, type=type_obj).exists():
            return Response({'detail': 'Недоступный тип'}, status=status.HTTP_400_BAD_REQUEST)
        category_obj, _ = Category.objects.get_or_create(
            name=serializer.validated_data.get('name'),
            type=type_obj,
        )
        CategoryOwnership.objects.get_or_create(user=self.request.user, category=category_obj)
        serializer.instance = category_obj

    @transaction.atomic
    def perform_destroy(self, instance):
        CategoryOwnership.objects.filter(user=self.request.user, category=instance).delete()
        if not instance.owners.exists():
            instance.delete()


class MySubcategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        qs = Subcategory.objects.filter(owners__user=self.request.user).distinct()
        category_id = self.request.query_params.get('category')
        if category_id is not None:
            qs = qs.filter(category_id=category_id)
        return qs

    @transaction.atomic
    def perform_create(self, serializer):
        category_obj = serializer.validated_data.get('category')
        if not CategoryOwnership.objects.filter(user=self.request.user, category=category_obj).exists():
            return Response({'detail': 'Недоступная категория'}, status=status.HTTP_400_BAD_REQUEST)
        subcategory_obj, _ = Subcategory.objects.get_or_create(
            name=serializer.validated_data.get('name'),
            category=category_obj,
        )
        SubcategoryOwnership.objects.get_or_create(user=self.request.user, subcategory=subcategory_obj)
        serializer.instance = subcategory_obj

    @transaction.atomic
    def perform_destroy(self, instance):
        SubcategoryOwnership.objects.filter(user=self.request.user, subcategory=instance).delete()
        if not instance.owners.exists():
            instance.delete()


class MoneyFlowViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с денежными операциями."""
    serializer_class = MoneyFlowSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MoneyFlowFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи
    page_size = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .services import MoneyFlowService
        self.service = MoneyFlowService()

    def get_queryset(self):
        """Получение операций только текущего пользователя."""
        if not self.request.user.is_authenticated:
            return MoneyFlow.objects.none()
        
        # Получаем фильтры из запроса
        filters_dict = {}
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        status_name = self.request.query_params.get('status')
        type_filter = self.request.query_params.get('type')
        category = self.request.query_params.get('category')

        if start_date:
            filters_dict['start_date'] = start_date
        if end_date:
            filters_dict['end_date'] = end_date
        if status_name:
            filters_dict['status'] = status_name
        if type_filter:
            filters_dict['type'] = type_filter
        if category:
            filters_dict['category'] = category

        return self.service.get_filtered_money_flows(filters_dict, self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы можете редактировать только свои операции")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Вы можете удалять только свои операции")
        instance.delete()
