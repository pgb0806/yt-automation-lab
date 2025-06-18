import argparse
import requests
import base64
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from dotenv import load_dotenv
load_dotenv() 

# ========================
# 1️⃣  Parse arguments
# ========================
parser = argparse.ArgumentParser()
parser.add_argument("--video_url")
parser.add_argument("--music_url")
parser.add_argument("--text")
parser.add_argument("--author")
parser.add_argument("--reference")
args = parser.parse_args()

print("🎥 Video URL:", args.video_url)
print("🎶 Music URL:", args.music_url)
print("📝 Text:", args.text)
print("🗿 Author:", args.author)
print("📚 Reference:", args.reference)

# ========================
# 2️⃣  Download background video
# ========================
video_path = "background.mp4"
print(f"⏬ Downloading video: {args.video_url}")
r = requests.get(args.video_url)
with open(video_path, "wb") as f:
    f.write(r.content)

# ========================
# 3️⃣  Download background music from YouTube
# ========================
music_path = "music.mp3"
print(f"⏬ Downloading music: {args.music_url}")
yt = YouTube(args.music_url)
stream = yt.streams.filter(only_audio=True).first()
stream.download(filename="temp_music.mp4")
# Convert to mp3 using moviepy
audio_clip = AudioFileClip("temp_music.mp4")
audio_clip.write_audiofile(music_path)
audio_clip.close()
os.remove("temp_music.mp4")

# ========================
# 4️⃣  Generate TTS voice-over
# ========================
tts_path = "tts.mp3"
API_URL = "http://api.zyphra.com/v1/audio/text-to-speech"
# API_KEY = "zsk-xxxxxx"  # Replace with your valid key
API_KEY = os.getenv("ZYPHRA_API_KEY")

print(f"🎙️ Generating TTS for: {args.text +" "+ args.author +" "+ args.reference}")
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}
# payload = {
#     "text": args.text,
#     "model": "zonos-v0.1-transformer",
#     "mime_type": "audio/mp3",
#     "emotion": {
#         "happiness": 0.8,
#         "neutral": 0.3
#     }
payload = {
        "text": args.text +" "+ args.author +" "+ args.reference,
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
}
response = requests.post(API_URL, headers=headers, json=payload)
if response.status_code == 200:
    with open(tts_path, "wb") as f:
        f.write(response.content)
    print(f"✅ TTS saved to {tts_path}")
else:
    print(f"❌ TTS generation failed: {response.text}")

# ========================
# 5️⃣  Merge video + audio + TTS + text overlay
# ========================
print("🛠️ Compositing final video...")
video = VideoFileClip(video_path)
music = AudioFileClip(music_path).volumex(0.5)
tts = AudioFileClip(tts_path)

# Combine music and TTS by overlaying
combined_audio = music.audio_fadeout(1).fx( 
    lambda clip: clip.volumex(0.5)
).set_duration(video.duration).audio_fadein(1)

final_audio = tts.set_start(1).audio_fadein(0.5).volumex(1.0)
video_audio = combined_audio.overlay(final_audio)

# Text overlay
txt = TextClip(
    f"{args.text}\n- {args.author}\n{args.reference}",
    fontsize=50, color='white', font='Amiri-Bold', method='caption', size=(video.w * 0.9, None)
).set_position(('center', 'bottom')).set_duration(video.duration)

final = CompositeVideoClip([video, txt]).set_audio(video_audio)
final.write_videofile("output.mp4", fps=24)

print("✅ Final video saved as output.mp4")
