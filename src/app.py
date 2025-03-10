from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os, requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'RAG')))

try:
    from rag_model import generate_response
except ImportError:
    print("Error: Could not import 'generate_response' from 'rag_model.py'. Check the file path.", file=sys.stderr)
    generate_response = None

app = Flask(__name__)
CORS(app)

UNSPLASH_API_KEY = 'P_9ov9AuFnABuXfdkTBYEQrAUtN5j7RmSU46IynLAGQ'
UNSPLASH_URL = 'https://api.unsplash.com/photos/random'

def get_unsplash_image(query):
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_API_KEY}'
    }
    params = {
        'query': query,
        'count': 1
    }
    
    response = requests.get(UNSPLASH_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['urls']['regular']  
    return None  

@app.route('/api/query', methods=['POST'])
@app.route('/api/query', methods=['POST'])

def query():
    user_query = request.json.get('query')

    if not user_query:
        return jsonify({'error': 'No query provided'}), 400

    response = generate_response(user_query)

    image_url = get_unsplash_image(user_query)  
    print("Fetched image URL:", image_url)  

    return jsonify({'response': response, 'image_url': image_url})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  
