from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/rewrite', methods=['POST'])
def rewrite():
    data = request.get_json()
    text = data.get("text", "")

    prompt = f"Rewrite this so that a 10-year-old can understand it, using simple words and short sentences:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "Rewrite text for a 10-year-old."},
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                      headers=headers, json=body)

    result = r.json()['choices'][0]['message']['content']
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
