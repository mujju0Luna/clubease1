from flask import Flask, request, render_template
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Cloudinary config
cloudinary.config( 
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_API_KEY'), 
  api_secret = os.getenv('CLOUDINARY_API_SECRET') 
)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    image_url = None

    if request.method == 'POST':
        if 'image' in request.files:
            upload_result = cloudinary.uploader.upload(request.files['image'])
            image_url = upload_result.get('secure_url')

    return render_template('upload.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
