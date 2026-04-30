# Stay Viewer 🏡
**Find Your Next Stay in Vallabh Vidyanagar**

Stay Viewer is a modern, responsive, and feature-rich directory web application designed to help students discover curated local PGs, Flats, and Private Hostels in Vallabh Vidyanagar, Gujarat. 

Built with a sleek, dark-themed glassmorphism UI, this platform prioritizes student experience by offering advanced filtering, exact GPS mapping, and direct broker contact information without any hidden fees or login walls.

## ✨ Key Features
- **Advanced Search & Filtering**: Instantly filter properties by accommodation type (PG/Flat/Hostel), maximum budget, and must-have facilities (e.g., AC, RO water, Wi-Fi).
- **Interactive Google Maps**: Exact pin-drops utilizing GPS coordinates or hyper-specific address routing to help students find stays relative to their college (like BVM).
- **Premium Glassmorphism UI**: Beautiful, fully mobile-responsive dark theme built with raw CSS, featuring smooth hover states, custom typography, and dynamic layouts.
- **Automated Data Processing**: Includes Python scripts utilizing OpenCV to automatically extract thumbnail frames from raw `.mp4` video tours.
- **Admin CMS**: Fully configured Django Admin backend for easy property management, amenity tagging, and broker detail updates.

## 🛠️ Technology Stack
- **Backend:** Python, Django 6.0
- **Database:** SQLite (Local/Development)
- **Frontend:** HTML5, Vanilla CSS3 (Glassmorphism design language), JavaScript
- **Video Processing:** OpenCV (`opencv-python`)
- **Deployment:** Gunicorn, WhiteNoise (for static file serving)

## 🚀 How to Run Locally

### Prerequisites
Make sure you have Python 3.x installed on your machine.

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/Aditya291206/stay-viewer.git
   cd stay-viewer
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
6. Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📂 Project Structure
- `/properties/` - Core Django app handling the models, views, and URL routing for property listings.
- `/templates/` - HTML templates built with Django templating language.
- `/static/css/` - Custom stylesheets, including the primary `styles.css`.
- `/media/` - Automatically generated thumbnails and uploaded property assets.
- `ingest_real_data.py` - Custom script for automating database population and video frame extraction.

## 🌐 Deployment
This application is configured for easy deployment on platforms like Render or PythonAnywhere.
- Static files are managed via `whitenoise`.
- The entry point is handled by `gunicorn`.
- Use the included `build.sh` script to automate dependency installation and static collection on your host.

---
*Disclaimer: This platform does not facilitate real-time bookings or inventory tracking. Please contact landlords directly to confirm availability.*
