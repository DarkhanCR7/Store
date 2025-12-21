from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'price', 'created_at')
	list_display_links = ('id', 'name')
	search_fields = ('name', 'description')
	list_per_page = 20
