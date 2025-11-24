import os
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq

# Initialize Flask
app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Serve the frontend
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# API endpoint
@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"output": "Please provide some text to rewrite."})

    # Include the "10-year-old" instruction directly in the user message
    prompt = f"Rewrite this text so that a 10-year-old can understand it, using simple words and short sentences:\n\n{text}"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},  # no system instruction
            ],
            model="mistral-7b-v0.1",
        )

        # Get the output text safely
        if chat_completion.choices and len(chat_completion.choices) > 0:
            result = chat_completion.choices[0].message.content
        else:
            result = "No output returned by the model."

    except Exception as e:
        result = f"Error contacting Groq API: {str(e)}"

    return jsonify({"output": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
