import requests
import base64

API_URL = "http://api.zyphra.com/v1/audio/text-to-speech"
API_KEY = "zsk-82233f324357f8c8210c3c0e21a83ea6ef91e88e99c590d357db9572151c783f"

def generate_tts(text, output_file):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "speaking_rate": "12.5",
        # speaker_audio must be BASE64 if you're sending a local file
        # Or leave empty if using default voice
        "speaker_audio": "",
        "model": "zonos-v0.1-transformer",
        "mime_type": "audio/mp3",
        "emotion": {
            "happiness": 0.8,
            "neutral": 0.3,
            "sadness": 0.05,
            "disgust": 0.05,
            "fear": 0.05,
            "surprise": 0.05,
            "anger": 0.05,
            "other": 0.5
        },
        # "pitchStd": "50.0"
    }

    with open("tts_audio.mp3", "rb") as f:
        payload["speaker_audio"] = base64.b64encode(f.read()).decode("utf-8")


    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # Zyphra returns raw audio bytes
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✅ TTS saved to {output_file}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

# Test
if __name__ == "__main__":
    generate_tts("An empty quiver never won a war. Fill it with arrows when you are ready to strike true.", "output.mp3")
