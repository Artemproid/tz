from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import (
    MyUserViewSet,
    StatusViewSet,
    TypeViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    MoneyFlowViewSet,
    MyStatusViewSet,
    MyTypeViewSet,
    MyCategoryViewSet,
    MySubcategoryViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title="MoneyFlow API",
        default_version='v1',
        description="API для управления денежными потоками",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register('users', MyUserViewSet, basename='users')
router.register('statuses', StatusViewSet, basename='statuses')
router.register('types', TypeViewSet, basename='types')
router.register('categories', CategoryViewSet, basename='categories')
router.register('subcategories', SubcategoryViewSet, basename='subcategories')
router.register('money-flows', MoneyFlowViewSet, basename='money-flows')

router.register('my/statuses', MyStatusViewSet, basename='my-statuses')
router.register('my/types', MyTypeViewSet, basename='my-types')
router.register('my/categories', MyCategoryViewSet, basename='my-categories')
router.register('my/subcategories', MySubcategoryViewSet, basename='my-subcategories')

urlpatterns = [
    
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
    
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
    path('health/', lambda request: None),  
]
