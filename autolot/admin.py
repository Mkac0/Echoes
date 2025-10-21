from django.contrib import admin
from .models import Car, CarPhoto, User

class CarPhotoInLine(admin.TabularInline):
    model = CarPhoto
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'vin', 'price', 'status')
    list_filter = ('status', 'make', 'model', 'year', 'condition')
    search_fields = ('vin', 'make', 'model', 'trim')
    inlines = [CarPhotoInLine]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status', 'interested_in')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email')
