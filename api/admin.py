from django.contrib import admin

from api.models import Product, Status


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "status", "stock", "price", "created_at", "updated_at")

class StatusAdmin(admin.ModelAdmin):
    list_display = ("__str__", "key",  "created_at", "updated_at")

admin.site.register(Product, ProductAdmin)
admin.site.register(Status, StatusAdmin)
