from flask import Flask , jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello, World!"}, 200
    
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data:
            return {"error": "Please provide a 'name' in JSON format."}, 400
        
        name = data['name']
        return {"message": f"Hello, {name}!"}, 201
    
api.add_resource(HelloWorld, '/hello')

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)