from flask_mail import Message
from flask import render_template, current_app
import secrets, os
from PIL import Image
from geopy.geocoders import Nominatim




def renameImage(imageFile, path="media"):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(imageFile.filename)
    imageName = random_hex + ext
    imagePath = os.path.join(current_app.root_path, 'static/'+path, imageName)
    
    size = (200, 200)
    image = Image.open(imageFile)
    image.thumbnail(size)
    image.save(imagePath)
    return imageName


def convert_coordinates_to_address(latitude, longitude):
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    # Combine latitude and longitude into a string
    location = f"{latitude}, {longitude}"
    
    # Use reverse geocoding to convert coordinates to address
    try:
        address = geolocator.reverse(location)
        return address.address
    except Exception as e:
        print(f"Error occurred: {e}")
        return None



@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('additions/404.html'), 404
