from flask_mail import Message
from flask import render_template, current_app
import secrets, os
from PIL import Image
# from geopy.geocoders import Nominatim


def renameImage(imageFile, path="media"):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(imageFile.filename)
    imageName = random_hex + ext
    imagePath = os.path.join(current_app.root_path, "static/" + path, imageName)

    size = (200, 200)
    image = Image.open(imageFile)
    image.thumbnail(size)
    image.save(imagePath)
    return imageName


def convert_to_degrees(value):
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = round((value - degrees - minutes / 60) * 3600, 1)
    return degrees, minutes, seconds


def convert_coordinates(latitude, longitude):
    # Convert latitude to degrees, minutes, seconds
    lat_deg, lat_min, lat_sec = convert_to_degrees(abs(latitude))
    lat_dir = "N" if latitude >= 0 else "S"

    # Convert longitude to degrees, minutes, seconds
    lon_deg, lon_min, lon_sec = convert_to_degrees(abs(longitude))
    lon_dir = "E" if longitude >= 0 else "W"

    # Format coordinates as required
    lat_str = f"{lat_deg}°{lat_min}'{lat_sec}\"{lat_dir}"
    lon_str = f"{lon_deg}°{lon_min}'{lon_sec}\"{lon_dir}"

    return lat_str, lon_str


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template("additions/404.html"), 404


# def convert_coordinates_to_address(latitude, longitude):
#     # Initialize Nominatim geocoder
#     geolocator = Nominatim(user_agent="miknassaApp")

#     # Combine latitude and longitude into a string
#     location = f"{latitude}, {longitude}"

#     # Use reverse geocoding to convert coordinates to address
#     try:
#         address = geolocator.reverse(location)
#         return address.address
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return None
