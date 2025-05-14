from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
import plotly.utils
import json
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_chart', methods=['POST'])
def get_chart():
    # Example data - you can replace this with your own logic
    data = request.get_json()
    categories = data.get('categories', ['A', 'B', 'C', 'D'])
    values = data.get('values', [10, 20, 30, 40])

    # Ensure values are standard Python lists (not NumPy arrays)
    values = list(np.array(values))

    fig = go.Figure(data=[
        go.Bar(x=categories, y=values)
    ])
    fig.update_layout(title='Bar Chart', xaxis_title='Category', yaxis_title='Value')

    # Convert to JSON string
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({'chart': graphJSON})

if __name__ == '__main__':
    app.run(debug=True)
