"""Flask web server for the Emotion Detection final project.

Exposes:
- GET "/" -> renders the provided index.html
- GET "/emotionDetector" -> runs emotion detection and returns a formatted string
"""
import requests
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector
app = Flask(__name__)

@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")

@app.route("/emotionDetector")
def detect_emotion():
    """Analyze the text provided by the user and return detected emotions."""
    text_to_analyze = request.args.get("textToAnalyze", "", type=str).strip()

    if not text_to_analyze:
        return "Invalid text! Please try again."

    try:
        result = emotion_detector(text_to_analyze)
    except (requests.exceptions.RequestException, ValueError):
        return "Invalid text! Please try again."

    needed = {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"}
    if not isinstance(result, dict) or not needed.issubset(result):
        return "Invalid text! Please try again."

    response_text = (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return response_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
