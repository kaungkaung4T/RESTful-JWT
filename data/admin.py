from django.contrib import admin
from data.models import Item

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "time"]


admin.site.register(Item, ItemAdmin)
