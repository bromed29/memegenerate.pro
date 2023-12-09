from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    top_text = request.form.get('top_text')
    bottom_text = request.form.get('bottom_text')
    image_url = request.form.get('image_url')

    meme_url = generate_meme(top_text, bottom_text, image_url)

    return render_template('result.html', meme_url=meme_url)

def generate_meme(top_text, bottom_text, image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert('RGBA')
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Calculate the position for top and bottom text
    text_width, text_height = draw.textsize(top_text, font)
    top_text_position = ((image.width - text_width) // 2, 10)

    text_width, text_height = draw.textsize(bottom_text, font)
    bottom_text_position = ((image.width - text_width) // 2, image.height - text_height - 10)

    # Add text to the image
    draw.text(top_text_position, top_text, (255, 255, 255), font=font)
    draw.text(bottom_text_position, bottom_text, (255, 255, 255), font=font)

    # Save or serve the generated meme
    meme_path = "static/generated_meme.png"
    image.save(meme_path)

    return meme_path

if __name__ == '__main__':
    app.run(debug=True)


