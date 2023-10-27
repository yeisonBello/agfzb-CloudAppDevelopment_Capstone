from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here

# Register the CarMake model

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CarModelInline]  # Include CarModelInline here to manage CarModel within CarMake admin page

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'name', 'type', 'year', 'dealer_id')
    list_filter = ('car_make', 'type')
    search_fields = ('name', 'car_make__name', 'dealer_id')

