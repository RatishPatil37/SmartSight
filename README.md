# SmartSight
Yolov8n based AI Navigation Smart Glasses for the Visually Impaired using Raspberry PI 4B 

# 📸 RPi Cloud Cam Uploader
A lightweight Flask web interface for the Raspberry Pi that captures photos or videos and automatically uploads them to Microsoft OneDrive (or any cloud storage) using **Rclone**.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)
![Cloud](https://img.shields.io/badge/OneDrive-0078D4?style=for-the-badge&logo=microsoft-onedrive&logoColor=white)

## 🚀 Features

* **Web Interface:** Simple control via any browser on the local network.
* **Instant Photo Mode:** Captures high-res images using `rpicam-still`.
* **Video Mode:** Records 5-second clips, automatically converts them to MP4 (Android/iOS compatible), and uploads them.
* **Auto-Cleanup:** Deletes local files immediately after a successful upload to save SD card space.
* **Cloud Sync:** Uses `rclone` for reliable, secure uploads to OneDrive.

---

## 🛠️ System Architecture

Here is how the data flows from your browser to the cloud:

```mermaid
graph TD
    User["User (Mobile/PC)"] -->|HTTP POST| Flask["Flask Web Server"]
    
    subgraph Raspberry Pi
        Flask -->|Trigger| Cam{"Camera Module"}
        Cam -->|Capture Photo| JPG["IMG.jpg"]
        Cam -->|Capture Video| RAW["raw.h264"]
        
        RAW -->|FFmpeg| MP4["VID.mp4"]
        
        JPG -->|Rclone| CloudProcess["Cloud Upload"]
        MP4 -->|Rclone| CloudProcess
    end
    
    CloudProcess -->|Upload| OneDrive(("OneDrive"))
    CloudProcess -->|Success| Cleanup["Delete Local Files"]
    Cleanup -->|Response| Flask
    Flask -->|JSON| User

```

---

## 📋 Prerequisites

Before running the Python code, you must install the necessary system tools on your Raspberry Pi.

### 1. Install System Dependencies

Open your terminal and run:

```bash
sudo apt update
sudo apt install ffmpeg rclone

```

### 2. Configure Rclone

You need to connect Rclone to your OneDrive account.

1. Run the config wizard:
```bash
rclone config

```


2. Create a new remote named **`cloud_sight`** (matches the code configuration).
3. Select `onedrive` from the list.
4. Follow the on-screen instructions to authorize via your browser.

### 3. Verify Camera

Ensure your Raspberry Pi camera is enabled and working with the modern libcamera stack:

```bash
rpicam-hello

```

---

## ⚙️ Installation & Setup

1. **Clone or Download this repository** to your Raspberry Pi.
2. **Install Python Requirements:**
```bash
pip install -r requirements.txt

```


*Note: If you see a `numpy` error, run: `pip install "numpy<2.0"`*

3. **Project Structure:**
Ensure your folder looks like this:
```
/project-folder
├── app.py                # The main Flask application
├── requirements.txt      # Python dependencies
└── templates/
    └── index.html        # Your HTML frontend

```



---

## ▶️ Usage

1. **Start the Server:**
```bash
python app.py

```


*You should see output indicating the server is running on port 5000.*
2. **Access the Interface:**
* Find your Pi's IP address: `hostname -I`
* Open a browser on your phone/laptop and go to: `http://<YOUR_PI_IP>:5000`


3. **Capture:**
* Click **Capture Photo** or **Record Video**.
* Watch the terminal for status updates (`[*] Uploading...`).
* Check your OneDrive folder (`Apps/rclone/rpi cam` or similar) to see the files appear!



---

## 🔧 Configuration

If you want to change the cloud destination, edit the top of `app.py`:

```python
# Name of your Rclone remote (set during 'rclone config')
RCLONE_REMOTE = "cloud_sight" 

# Folder path inside your OneDrive
CLOUD_FOLDER = "rpi cam" 

```

## 🐛 Troubleshooting

| Issue | Solution |
| --- | --- |
| **"Camera/Upload Failed"** | Check if another app is using the camera. Run `rpicam-hello` to test. |
| **"Video Failed"** | Ensure `ffmpeg` is installed (`sudo apt install ffmpeg`). |
| **Rclone Error** | Run `rclone listremotes` to check if your remote name matches `cloud_sight`. |
| **Numpy Error** | Run `pip install "numpy<2.0"` to fix version conflicts. |


## DEXTER GUIDE

1. **dex.py:** This is a voice-only chatbot script. It continuously listens for speech using Voice Activity Detection (VAD), transcribes the audio using the faster_whisper model, generates a response using a local LLM via ollama (specifically the tinyllama model), and speaks the response back using Kokoro TTS.
2. **dex_vision.py:** This is the more advanced version of the assistant that links the voice chatbot with the vision system. It listens for specific wake words ("hey dexter", etc.). When you ask it to start "object recognition", it launches the tts.py script. It also includes clever power-saving features: it instantly "freezes" the vision process while you are speaking to it so it doesn't max out the CPU.
3. **dex_wake.py:** A stripped-down, power-optimized version of the voice assistant. It is explicitly designed to run on a low-power 5V 2.1A power bank. It limits CPU threads and only activates when it hears its wake word, making it efficient for portable use without the camera.
4. **tts.py:** This is the "Smart Sight" vision module. It uses a camera to capture video, runs a YOLO object detection model (checking for a custom yolov5su_ncnn_model), and then uses text-to-speech (pyttsx3) to announce what it sees and where it is located (e.g., "I see a person at left, cup at center"). It also displays a video feed with bounding boxes and vertical guide lines.
5. **test_mic.py:** A small utility script likely used just to verify that the microphone is working correctly.
yolov5su_ncnn_model: A folder containing the specific neural network model used by the vision script to detect objects.

---

Made with ❤️ and 🐍 Python

```

```
