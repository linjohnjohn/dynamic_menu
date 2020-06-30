from django.contrib import admin

# Register your models here.
from .models import Category, Item, CategoryVariant, Ingredient, ItemVariant

class IngredientAdmin(admin.ModelAdmin):
    list_display=('name', 'available')
    list_filter=('available',)

class ItemVariantInline(admin.TabularInline):
    model = ItemVariant
    filter_horizontal = ('ingredients',)
    show_change_link=True
    extra=1

class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('ingredients',)
    inlines = [
        ItemVariantInline
    ]

class ItemInline(admin.TabularInline):
    model = Item
    show_change_link=True
    extra=0
    # filter_vertical = ('ingredients',)
    exclude = ['ingredients']

class VariantInline(admin.TabularInline):
    model = CategoryVariant
    filter_horizontal = ('ingredients',)
    show_change_link=True
    extra=0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
        VariantInline
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Ingredient, IngredientAdmin)
