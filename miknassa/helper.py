from flask_mail import Message
from flask import render_template, current_app
import secrets, os
from PIL import Image

 



def renameImage(imageFile):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(imageFile.filename)
    imageName = random_hex + ext
    imagePath = os.path.join(current_app.root_path, 'static/media', imageName)
    
    size = (200, 200)
    image = Image.open(imageFile)
    image.thumbnail(size)
    image.save(imagePath)
    return imageName


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('additions/404.html'), 404
