from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to allow frontend access
import sys
import os

# Get the absolute path to the 'RAG' folder
# Add the RAG folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'RAG')))

try:
    from rag_model import generate_response
except ImportError:
    print("Error: Could not import 'generate_response' from 'rag_model.py'. Check the file path.", file=sys.stderr)
    generate_response = None

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route('/api/query', methods=['POST'])
def query():
    if generate_response is None:
        return jsonify({'error': 'Server configuration issue: RAG model is not loaded'}), 500

    # Get the user query from the request
    user_query = request.json.get('query')
    
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Get the response from the RAG model
    response = generate_response(user_query)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Listen on all network interfaces
