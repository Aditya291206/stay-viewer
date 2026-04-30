from django.contrib import admin
from .models import Amenity, Property, PropertyImage, Contact

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_name')
    search_fields = ('name',)

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'configuration', 'gender_policy', 'estimated_rent', 'last_updated')
    list_filter = ('property_type', 'gender_policy')
    search_fields = ('title', 'address')
    inlines = [PropertyImageInline, ContactInline]
    filter_horizontal = ('amenities',)
