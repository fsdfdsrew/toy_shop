from . import translation
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from .models import Category, Brand, AgeGroup, Toy, ToyImage, Review, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    ordering = ['name']

@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    list_display = ['name', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'country', 'created_at']
    search_fields = ['name', 'description', 'country']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    ordering = ['name']

@admin.register(AgeGroup)
class AgeGroupAdmin(TranslationAdmin):
    list_display = ['name', 'min_age', 'max_age', 'image_preview', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['min_age']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Изображение'

class ToyImageInline(admin.TabularInline):
    model = ToyImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main', 'order']

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at']
    fields = ['name', 'email', 'rating', 'comment', 'is_approved', 'created_at']

@admin.register(Toy)
class ToyAdmin(TranslationAdmin):
    list_display = [
        'name', 'category', 'brand', 'price', 'stock', 'is_active', 
        'is_featured', 'is_bestseller', 'is_new', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_featured', 'is_bestseller', 'is_new', 
        'category', 'brand', 'age_group', 'condition', 'gender', 'created_at'
    ]
    search_fields = ['name', 'description', 'sku', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_active', 'is_featured', 'is_bestseller', 'is_new']
    readonly_fields = ['sku', 'views_count', 'created_at', 'updated_at']
    inlines = [ToyImageInline, ReviewInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'sku', 'description', 'short_description')
        }),
        ('Категоризация', {
            'fields': ('category', 'brand', 'age_group', 'gender')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'old_price', 'stock', 'min_stock')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_featured', 'is_bestseller', 'is_new', 'condition')
        }),
        ('Характеристики', {
            'fields': ('weight', 'dimensions', 'specifications')
        }),
        ('Изображения', {
            'fields': ('main_image',)
        }),
        ('Метаданные', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    list_per_page = 25

@admin.register(ToyImage)
class ToyImageAdmin(admin.ModelAdmin):
    list_display = ['toy', 'image_preview', 'is_main', 'order', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['toy__name', 'alt_text']
    list_editable = ['is_main', 'order']
    ordering = ['toy', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'toy', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['name', 'toy__name', 'comment']
    list_editable = ['is_approved']
    ordering = ['-created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'first_name', 'last_name', 'email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('order_number', 'status', 'total_amount')
        }),
        ('Данные покупателя', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'toy', 'quantity', 'price', 'subtotal']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'toy__name']
    readonly_fields = ['subtotal']