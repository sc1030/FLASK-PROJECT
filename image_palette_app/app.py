from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from collections import Counter
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def extract_colors(image_path, num_colors=5):
    image = Image.open(image_path)
    image = image.resize((200, 200))  # Resize for faster processing
    img_array = np.array(image)
    img_array = img_array.reshape((-1, 3))

    model = KMeans(n_clusters=num_colors)
    labels = model.fit_predict(img_array)
    counts = Counter(labels)

    center_colors = model.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = ['#%02x%02x%02x' % tuple(map(int, color)) for color in ordered_colors]

    return hex_colors

@app.route('/', methods=['GET', 'POST'])
def index():
    colors = []
    image_filename = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Extract colors
            colors = extract_colors(image_path)

            # Only pass the filename to the template
            image_filename = filename
    return render_template('index.html', colors=colors, image=image_filename)


if __name__ == '__main__':
    app.run(debug=True)
