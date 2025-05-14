from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def scatter_plot():
    # Generate some advanced random data
    np.random.seed(42)
    x = np.random.rand(100)
    y = np.random.rand(100)
    colors = np.random.rand(100)
    sizes = 1000 * np.random.rand(100)

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis', edgecolors='w', linewidth=0.5)
    ax.set_title("Advanced Scatter Plot")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    fig.colorbar(scatter)

    # Save plot to BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("index.html", plot_url=plot_url)
