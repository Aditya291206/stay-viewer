from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Optional icon name/class")

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name

class Property(models.Model):
    PROPERTY_TYPES = [
        ('PG', 'Paying Guest'),
        ('FLAT', 'Flat/Apartment'),
        ('HOSTEL', 'Private Hostel'),
    ]

    GENDER_POLICIES = [
        ('BOYS', 'Boys Only'),
        ('GIRLS', 'Girls Only'),
        ('COED', 'Co-ed'),
    ]

    title = models.CharField(max_length=255, help_text="e.g. Sujan Flats")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    configuration = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 1BHK, 2BHK, Shared Room")
    gender_policy = models.CharField(max_length=10, choices=GENDER_POLICIES, default='COED')
    
    address = models.TextField()
    map_coordinates = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., 22.5534, 72.9234 for exact pin drop")
    walking_distance_bvm = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 5 mins walk to BVM")
    
    estimated_rent = models.CharField(max_length=100, help_text="e.g. ₹5000/month")
    numeric_rent = models.IntegerField(blank=True, null=True, help_text="Raw number for search filtering (e.g. 12000)")
    broker_fees = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 1 month rent")
    
    amenities = models.ManyToManyField(Amenity, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Building Exterior, Bedroom")
    is_primary = models.BooleanField(default=False, help_text="Check to make this the main thumbnail")

    def __str__(self):
        return f"Image for {self.property.title}"

class Contact(models.Model):
    CONTACT_ROLES = [
        ('LANDLORD', 'Landlord/Owner'),
        ('WARDEN', 'Warden'),
        ('BROKER', 'Broker'),
    ]
    
    property = models.ForeignKey(Property, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=CONTACT_ROLES)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()}) - {self.property.title}"
