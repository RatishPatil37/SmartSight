
# 📷 RPi Cloud Cam Uploader

A lightweight Flask web interface for the Raspberry Pi that captures photos or videos and automatically uploads them to Microsoft OneDrive.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)
![Cloud](https://img.shields.io/badge/OneDrive-0078D4?style=for-the-badge&logo=microsoft-onedrive&logoColor=white)

## 🚀 Features

* **Web Interface:** Simple control via any browser on the local network.
* **Auto-Upload:** Captured media is instantly synced to your specified OneDrive folder.
* **Photo & Video Support:** Toggle between capturing high-res images or recording short video clips.
* **Lightweight:** Minimal resource usage, perfect for Raspberry Pi Zero W or Pi 3/4.
* **Mobile Friendly:** Responsive design allows you to trigger the camera from your phone.

## 🛠️ Hardware Requirements

* Raspberry Pi (Zero W, 3B+, 4, or 5)
* Raspberry Pi Camera Module (v2, HQ, or compatible USB webcam)
* Micro SD Card (16GB+ recommended)
* Power Supply

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/yourusername/rpi-cloud-cam-uploader.git](https://github.com/yourusername/rpi-cloud-cam-uploader.git)
   cd rpi-cloud-cam-uploader

```

2. **Install Dependencies**
Make sure you have Python 3 installed, then run:
```bash
pip3 install -r requirements.txt

```


3. **Enable the Camera**
Run `sudo raspi-config`, navigate to **Interface Options**, and enable the **Camera**. Reboot the Pi.

## ⚙️ Configuration

1. **OneDrive Setup**
* Register a new app in the [Microsoft Azure Portal](https://www.google.com/search?q=https://portal.azure.com/).
* Obtain your `CLIENT_ID` and `CLIENT_SECRET`.
* Rename `config.example.json` to `config.json` and paste your credentials:
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "redirect_uri": "http://localhost:5000/callback",
  "upload_folder": "RPi_Cam_Uploads"
}

```




2. **Authentication**
On the first run, you will need to authenticate via the browser to generate the access token.

## 🏃 Usage

Start the Flask server:

```bash
python3 app.py

```

Open your browser and navigate to:
`http://<your-raspberry-pi-ip>:5000`

Click **Capture Photo** or **Record Video** to snap media and send it straight to the cloud.

## 📂 Project Structure

```
rpi-cloud-cam-uploader/
├── static/             # CSS and JS files
├── templates/          # HTML templates for the web interface
├── app.py              # Main Flask application logic
├── camera.py           # Camera interface script
├── onedrive_uploader.py # Logic for handling Microsoft Graph API
├── requirements.txt    # Python dependencies
└── config.json         # Configuration file (Git ignored)

```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```
