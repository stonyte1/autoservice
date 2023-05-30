from django.contrib import admin
from . import models

class OrderLineInline(admin.TabularInline):
    model = models.OrderLine

class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'car')
    inlines = [OrderLineInline]

class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'car_model', 'license_plate', 'VIN_code')
    list_filter = ('client', 'car_model')
    search_fields = ('license_plate', 'VIN_code')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

    

admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Car, CarAdmin)
# admin.site.register(models.OrderLine)
