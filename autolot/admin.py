from django.contrib import admin
from .models import Car, CarPhoto, CustomerLead, Profile

class CarPhotoInLine(admin.TabularInline):
    model = CarPhoto
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'vin', 'price', 'status', 'owner')
    list_filter = ('status', 'make', 'model', 'year', 'condition')
    search_fields = ('vin', 'make', 'model', 'trim')
    inlines = [CarPhotoInLine]

@admin.register(CustomerLead)
class CustomerLeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status', 'interested_in')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dealership_name')
    search_fields = ('user__username', 'name', 'dealership_name')
