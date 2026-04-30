import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stay_viewer_project.settings')
django.setup()

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Successfully created superuser 'admin' with password 'admin123'")
else:
    # Reset the password just in case they forgot it
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.save()
    print("Superuser 'admin' already exists. Password reset to 'admin123'")
