from django.contrib import admin

# Register your models here.
from .models import Category, Item, Ingredient, Variant, Modifier

class IngredientAdmin(admin.ModelAdmin):
    list_display=('name', 'available')
    list_filter=('available',)

class VariantInline(admin.TabularInline):
    
    verbose_name="Variant"
    model = Item.variants.through
    extra=0

class VariantAdmin(admin.ModelAdmin):
    filter_horizontal = ('item', 'ingredients')

class ModifierAdmin(admin.ModelAdmin):
    filter_horizontal = ('item', 'ingredients')
 
class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('ingredients',)
    inlines = [
        VariantInline
    ]

class ItemInline(admin.TabularInline):
    model = Item
    show_change_link=True
    extra=0
    exclude = ['ingredients']

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Modifier, ModifierAdmin)
