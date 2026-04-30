import os
import django
import cv2
import shutil
from pathlib import Path
from django.core.files import File
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stay_viewer_project.settings')
django.setup()

from properties.models import Property, Amenity, Contact, PropertyImage

def extract_frame(video_path, output_path, frame_number=30):
    """Extracts a specific frame from a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video stream or file: {video_path}")
        return False
    
    # Fast forward to the desired frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    if ret:
        cv2.imwrite(output_path, frame)
        cap.release()
        return True
    
    cap.release()
    return False

def ingest():
    print("Clearing database...")
    Property.objects.all().delete()
    Amenity.objects.all().delete()
    
    # Clear out old media files safely
    media_root = Path('media/property_images')
    if media_root.exists():
        for file in media_root.glob('*'):
            if file.is_file():
                file.unlink()
    else:
        media_root.mkdir(parents=True, exist_ok=True)
        
    print("Creating Amenities...")
    base_amenities_names = ["RO water", "Geyser", "Fridge", "Almira", "Bed", "Study Table"]
    base_amenities = [Amenity.objects.create(name=name) for name in base_amenities_names]
    ac_amenity = Amenity.objects.create(name="AC (In one room)")
    
    # Real Property Data
    properties_data = [
        {
            "title": "Above Green Apple Flat",
            "type": "FLAT",
            "config": "3BHK",
            "gender": "COED",
            "rent": "₹11,000 / month",
            "has_ac": False,
            "contacts": [{"name": "Bipin Patel", "role": "BROKER", "phone": "9925062722"}],
            "media": "above green apple flate (3BHK).mp4"
        },
        {
            "title": "Above Green Apple Flat",
            "type": "FLAT",
            "config": "2BHK",
            "gender": "COED",
            "rent": "₹10,000 / month",
            "has_ac": False,
            "contacts": [{"name": "Bipin Patel", "role": "BROKER", "phone": "9925062722"}],
            "media": "above green apple flate (2BHK).mp4"
        },
        {
            "title": "Above The Rangoli Khaman",
            "type": "FLAT",
            "config": "3BHK",
            "gender": "COED",
            "rent": "₹15,500 / month",
            "has_ac": True,
            "contacts": [{"name": "Wasim", "role": "BROKER", "phone": "Not Provided"}],
            "media": "above the rangoli khaman (3BHK).mp4"
        },
        {
            "title": "Behind Vraj Prime",
            "type": "FLAT",
            "config": "2BHK",
            "gender": "COED",
            "rent": "₹12,000 / month",
            "has_ac": False,
            "contacts": [{"name": "Shiv Property", "role": "BROKER", "phone": "8866205001"}],
            "media": "behind vraj prime (2BHK).mp4"
        },
        {
            "title": "Sujan Flats",
            "type": "FLAT",
            "config": "2BHK",
            "gender": "COED",
            "rent": "₹12,800 / month",
            "has_ac": True,
            "contacts": [{"name": "Shiv Property", "role": "BROKER", "phone": "8866205001"}],
            "media": "sujan flates (2BHK).mp4"
        },
        {
            "title": "House",
            "type": "FLAT",
            "config": "3BHK",
            "gender": "COED",
            "rent": "₹22,000 / month",
            "has_ac": False,
            "contacts": [{"name": "Rajdeep", "role": "BROKER", "phone": "Not Provided"}],
            "media": "house (3bhk).mp4"
        },
        {
            "title": "Karamsad Road Flat",
            "type": "FLAT",
            "config": "3BHK",
            "gender": "COED",
            "rent": "₹20,000 / month",
            "has_ac": True,
            "contacts": [{"name": "Rajdeep", "role": "BROKER", "phone": "Not Provided"}],
            "media": "karamsad road flate (3BHK).mp4"
        },
        {
            "title": "Atmiya Avenue",
            "type": "PG",
            "config": "Girls PG",
            "gender": "GIRLS",
            "rent": "Contact Broker for Price",
            "has_ac": False,
            "contacts": [{"name": "Atmiya Avenue Broker", "role": "BROKER", "phone": "8401494595"}],
            "media": "Atmiya Avenue (Girls Only).png"
        },
        {
            "title": "Behind Maheshwari Palace",
            "type": "PG",
            "config": "Rooms",
            "gender": "COED",
            "rent": "Contact for Price",
            "has_ac": False,
            "contacts": [{"name": "Unknown Broker", "role": "BROKER", "phone": "9512326787"}],
            "media": "behind maheshwari palace (rooms).png"
        }
    ]

    print("Ingesting properties...")
    for data in properties_data:
        prop = Property.objects.create(
            title=data["title"],
            property_type=data["type"],
            configuration=data["config"],
            gender_policy=data["gender"],
            address="Vallabh Vidyanagar (Refer to Broker)",
            walking_distance_bvm="Unknown",
            estimated_rent=data["rent"],
            broker_fees="Refer to Broker"
        )
        
        # Add basic amenities
        prop.amenities.add(*base_amenities)
        if data["has_ac"]:
            prop.amenities.add(ac_amenity)
            
        # Add contacts
        for contact in data["contacts"]:
            Contact.objects.create(
                property=prop,
                name=contact["name"],
                role=contact["role"],
                phone_number=contact["phone"]
            )
            
        # Process Media
        raw_path = os.path.join('raw_data', data["media"])
        if not os.path.exists(raw_path):
            print(f"WARNING: Media file not found -> {raw_path}")
            continue
            
        if data["media"].endswith('.mp4'):
            # Extract frame
            print(f"Extracting frame from {data['media']}...")
            temp_image_path = os.path.join('media', f"temp_{prop.id}.jpg")
            success = extract_frame(raw_path, temp_image_path, frame_number=50) # Grab 50th frame
            
            if success:
                with open(temp_image_path, 'rb') as f:
                    PropertyImage.objects.create(
                        property=prop,
                        image=File(f, name=f"{prop.id}_extracted.jpg"),
                        caption="Video Frame",
                        is_primary=True
                    )
                os.remove(temp_image_path)
        
        elif data["media"].endswith('.png'):
            print(f"Linking static image {data['media']}...")
            with open(raw_path, 'rb') as f:
                PropertyImage.objects.create(
                    property=prop,
                    image=File(f, name=data["media"]),
                    caption="Property Photo",
                    is_primary=True
                )

    print("\nSuccessfully ingested all properties!")

if __name__ == '__main__':
    ingest()
