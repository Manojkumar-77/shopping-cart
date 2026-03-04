from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product
from .models import Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'description', 'status', 'trending', 'created_at')
    list_filter = ('status', 'trending', 'created_at')
    search_fields = ('name', 'description')
    list_per_page = 5

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;" />', obj.image.url)
        return '-'

    image_tag.short_description = 'Image'
    image_tag.admin_order_field = 'image'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_image_tag', 'name', 'category', 'vendor', 'quantity', 'original_price', 'selling_price', 'status', 'trending', 'created_at')
    list_filter = ('category', 'status', 'trending', 'created_at')
    search_fields = ('name', 'vendor', 'description')
    list_per_page = 5

    def product_image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;" />', obj.product_image.url)
        return '-'

    product_image_tag.short_description = 'Image'
    product_image_tag.admin_order_field = 'product_image'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(Order)
admin.site.register(OrderItem)
