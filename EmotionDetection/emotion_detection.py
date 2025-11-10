# final_project/emotion_detection.py
import json
import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}

def _empty_result():
    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

def emotion_detector(text_to_analyze: str):
    """
    Task 2: call Watson endpoint and return response.text (initially).
    Task 3: parse JSON, extract five emotions, compute dominant.
    Task 7: if blank input or HTTP 400 (or any non-200), return all-None dict.
    """
    # --- Task 7 blank handling ---
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_result()

    try:
        payload = { "raw_document": { "text": text_to_analyze } }
        resp = requests.post(URL, headers=HEADERS, json=payload)

        # --- Task 7 HTTP status handling ---
        if resp.status_code != 200:
            # The lab asks to return same dict but with all None on 400
            return _empty_result()

        # --- Task 3 formatting & dominant emotion ---
        data = resp.json()
        # Expected path from Skills Network endpoint:
        # data["emotionPredictions"][0]["emotion"] -> dict with anger, disgust, fear, joy, sadness
        emo = (data.get("emotionPredictions") or [{}])[0].get("emotion") or {}

        # Extract the required five, default to 0.0 if missing
        anger   = float(emo.get("anger", 0.0))
        disgust = float(emo.get("disgust", 0.0))
        fear    = float(emo.get("fear", 0.0))
        joy     = float(emo.get("joy", 0.0))
        sadness = float(emo.get("sadness", 0.0))

        scores = {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness
        }

        # Dominant emotion
        dominant = max(scores, key=scores.get) if any(scores.values()) else None
        scores['dominant_emotion'] = dominant
        return scores

    except Exception:
        # Any unexpected error -> behave like Task 7 requirement
        return _empty_result()
