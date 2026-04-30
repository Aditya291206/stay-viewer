import os
import django
import shutil
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stay_viewer_project.settings')
django.setup()

from properties.models import Property, Amenity, Contact, PropertyImage
from django.core.files import File

def populate():
    print("Clearing existing data...")
    Property.objects.all().delete()
    Amenity.objects.all().delete()

    print("Adding amenities...")
    wifi = Amenity.objects.create(name="High-Speed WiFi")
    ac = Amenity.objects.create(name="Air Conditioning")
    laundry = Amenity.objects.create(name="Laundry Service")
    food = Amenity.objects.create(name="3 Meals Included")

    print("Adding properties...")
    pg1 = Property.objects.create(
        title="Apex Premium Boys PG",
        property_type="PG",
        configuration="2 Sharing / 3 Sharing Rooms",
        gender_policy="BOYS",
        address="12, Vallabh Vidyanagar main road, near BVM",
        walking_distance_bvm="3 mins walk to BVM",
        estimated_rent="₹7500/month",
        broker_fees="No Brokerage"
    )
    pg1.amenities.add(wifi, ac, food, laundry)

    flat1 = Property.objects.create(
        title="Sujan Heights 2BHK",
        property_type="FLAT",
        configuration="2 Bedrooms, 1 Hall, 1 Kitchen",
        gender_policy="COED",
        address="Behind BVM Engineering College",
        walking_distance_bvm="7 mins walk to BVM",
        estimated_rent="₹15,000/month (total)",
        broker_fees="1 Month Rent"
    )
    flat1.amenities.add(wifi, ac)

    print("Adding contacts...")
    Contact.objects.create(property=pg1, name="Ramesh Patel", role="WARDEN", phone_number="+91-9876543210")
    Contact.objects.create(property=flat1, name="Amit Sharma", role="BROKER", phone_number="+91-8888888888")

    print("Adding images...")
    # Add PG exterior image
    img_path1 = r"C:\Users\adity\.gemini\antigravity\brain\97e01fd5-820f-4dee-8631-3a59158d2201\pg_exterior_1777547464920.png"
    if os.path.exists(img_path1):
        with open(img_path1, 'rb') as f:
            PropertyImage.objects.create(property=pg1, image=File(f, name='pg_exterior.png'), caption="Building Exterior", is_primary=True)
            
    # Add Flat interior image
    img_path2 = r"C:\Users\adity\.gemini\antigravity\brain\97e01fd5-820f-4dee-8631-3a59158d2201\flat_interior_1777547489049.png"
    if os.path.exists(img_path2):
        with open(img_path2, 'rb') as f:
            PropertyImage.objects.create(property=flat1, image=File(f, name='flat_interior.png'), caption="Modern Bedroom", is_primary=True)

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
