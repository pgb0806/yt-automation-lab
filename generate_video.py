import argparse

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
print("Reference: ",args.reference)

# Now use these instead of hardcoded values.
