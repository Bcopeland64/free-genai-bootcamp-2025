from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from backend.api.routes import register_routes
from backend.models.db import init_db

app = Flask(__name__)
CORS(app)

# Initialize database
init_db(app)

# Register API routes
register_routes(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)