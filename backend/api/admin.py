from django.contrib import admin

from .models import ( MoneyFlow, Status,
                      Type, Category, Subcategory,)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(MoneyFlow)
class MoneyFlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'type', 'category', 'amount')
    list_filter = ('type', 'category', 'status')
    search_fields = ('comment',)
