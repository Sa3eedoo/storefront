from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.aggregates import Count
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    FILTER_LOW = '<10'
    FILTER_MEDIUM = '<100'
    FILTER_HIGH = '>100'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.FILTER_LOW, 'Low'),
            (InventoryFilter.FILTER_MEDIUM, 'Medium'),
            (InventoryFilter.FILTER_HIGH, 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.FILTER_LOW:
            return queryset.filter(inventory__lt=10)
        elif self.value() == InventoryFilter.FILTER_MEDIUM:
            return queryset.filter(inventory__gte=10).filter(inventory__lt=100)
        elif self.value() == InventoryFilter.FILTER_HIGH:
            return queryset.filter(inventory__gte=100)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    ordering = ['title']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title__icontains']
    actions = ['clear_inventory']
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['collection']

    @admin.display(ordering='collection__title')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        elif 10 <= product.inventory < 100:
            return 'Medium'
        elif product.inventory >= 100:
            return 'High'

    @admin.action(description='Clear inventory of selected products')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': customer.id
            })
        )
        return format_html('<a href="{}">{}</a>', url, str(customer.orders) + ' Orders')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders=Count('order')
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    ordering = ['title']
    search_fields = ['title__icontains']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': collection.id
            })
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ['product']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    ordering = ['id']
    list_per_page = 10
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
