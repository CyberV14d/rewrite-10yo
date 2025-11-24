from flask import Flask, request, jsonify, send_from_directory
import requests, os

app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")

# Serve the frontend
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# API endpoint for rewriting text
@app.route('/rewrite', methods=['POST'])
def rewrite():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"output": "Please provide some text to rewrite."})

    prompt = f"Rewrite this so that a 10-year-old can understand it, using simple words and short sentences:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral-7b-v0.1",  # <-- switched to Mistral
        "messages": [
            {"role": "system", "content": "Rewrite text for a 10-year-old."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=body, timeout=30
        )

        r.raise_for_status()  # Raise error if HTTP status != 200
        response_json = r.json()

        if 'choices' in response_json and len(response_json['choices']) > 0:
            result = response_json['choices'][0]['message']['content']
        else:
            result = f"API error: {response_json}"

    except requests.exceptions.RequestException as e:
        result = f"Request error: {str(e)}"
    except Exception as e:
        result = f"Unexpected error: {str(e)}"

    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
