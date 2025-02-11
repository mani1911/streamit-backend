from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
DEEZER_CHART_URL = "https://api.deezer.com/chart/0/tracks"

@app.route('/health', methods=['GET'])
def health():
    return "healthy"

@app.route('/songs', methods=['GET'])
def get_songs():
    """Fetch popular Deezer songs with pagination."""
    limit = request.args.get("limit", 10)  # Default 10 results per page
    index = request.args.get("index", 0)   # Default start from 0

    params = {
        "limit": limit,
        "index": index
    }

    response = requests.get(DEEZER_CHART_URL, params=params)
    data = response.json()

    if "data" not in data or not data["data"]:
        return jsonify({"error": "No songs found"}), 404

    songs = []
    for track in data["data"]:
        songs.append({
            "name": track["title"],
            "artist": track["artist"]["name"],
            "album": track["album"]["title"],
            "deezer_url": track["link"],
            "preview_url": track["preview"] if track["preview"] else "No preview available",
            "duration_sec": track["duration"]
        })

    next_index = int(index) + int(limit)
    next_page_url = f"/songs?limit={limit}&index={next_index}"

    return jsonify({
        "songs": songs,
        "next_page": next_page_url
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
