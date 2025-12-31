from django.contrib import admin
from .models import Product, UserProfile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'price', 'created_at')
	list_display_links = ('id', 'name')
	search_fields = ('name', 'description')
	list_per_page = 20


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'created_at', 'updated_at')
	search_fields = ('user__username', 'user__email')
	readonly_fields = ('created_at', 'updated_at')
