import os
import requests
import yt_dlp

# === Config ===
VIDEO_URL = "https://youtu.be/nOk-3Qije9Y?si=SSXdZgYy7Fk6Usip"
OUTPUT_FILE = "video.mp4"
STREAMTAPE_API_KEY = os.getenv("STREAMTAPE_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# === 1. Download YouTube video ===
def download_video():
    print("📥 Downloading video...")
    ydl_opts =
    {
        # Try to download 1080p with audio; fallback to best available
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': OUTPUT_FILE,
        'merge_output_format': 'mp4',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([VIDEO_URL])
    print("✅ Video downloaded.")

# === 2. Upload to StreamTape ===
def upload_to_streamtape():
    print("🚀 Uploading to StreamTape...")

    # Step 1: Get upload URL
    r = requests.get(f"https://api.streamtape.com/file/ul?login=79e10358ea0fdad85e40&key={STREAMTAPE_API_KEY}")
    upload_url = r.json()['result']['url']

    # Step 2: Upload file
    with open(OUTPUT_FILE, 'rb') as f:
        files = {'file1': (OUTPUT_FILE, f)}
        res = requests.post(upload_url, files=files)

    result = res.json()
    print("✅ Uploaded to StreamTape.")
    print("🌐 Link:", result)

    if result.get("status") == 200:
        link = result["result"]["url"]
        return link
    else:
        return "❌ Upload failed."

# === 3. Send link to Telegram ===
def send_telegram_message(link):
    print("📩 Sending StreamTape link to Telegram...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": f"🎥 Your video is uploaded!\n\n🔗 {link}"
    }
    response = requests.post(url, data=data)
    print("✅ Message sent to Telegram.", response.json())

# === 4. Cleanup ===
def cleanup():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print("🗑️ Video deleted from local server.")

# === Main ===
if __name__ == "__main__":
    download_video()
    streamtape_link = upload_to_streamtape()
    send_telegram_message(streamtape_link)
    cleanup()
