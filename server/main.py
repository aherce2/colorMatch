from flask import Flask, jsonify
from flask_cors import CORS

# Create An App Instance
app = Flask(__name__)

# Enable Orgins -> Accept all origins for now
cors = CORS(app, origins='*')

@app.route("/api/users", methods=['GET'])

def users():
    return jsonify(
        {
            "users": [
                'Ashley',
                'Angel'   
            ]
            
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=8080)