from django.shortcuts import render, get_object_or_404
from .models import Property, Amenity

def property_list(request):
    properties = Property.objects.all().order_by('-last_updated')
    
    # Basic filtering logic could go here
    property_type = request.GET.get('type')
    if property_type:
        properties = properties.filter(property_type=property_type)
        
    max_rent = request.GET.get('max_rent')
    if max_rent and max_rent.isdigit():
        properties = properties.filter(numeric_rent__lte=int(max_rent))
        
    amenity_name = request.GET.get('amenity')
    if amenity_name:
        properties = properties.filter(amenities__name__icontains=amenity_name)
        
    amenities = Amenity.objects.all()
        
    context = {
        'properties': properties.distinct(),
        'amenities': amenities,
        'selected_type': property_type,
        'selected_rent': max_rent,
        'selected_amenity': amenity_name
    }
    return render(request, 'properties/property_list.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property_obj})
