import cv2
import pytesseract
import time
from picamera2 import Picamera2
import pyttsx3
import numpy as np

# --- Setup ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
found_voice = next((voice.id for voice in voices if 'en' in voice.languages), None)
if found_voice:
    engine.setProperty("voice", found_voice)
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1000, 1000)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

print("Camera initialized. Press 's' to perform OCR and get voice feedback. Press 'q' to quit.")

# --- Main Loop ---
while True:
    image = picam2.capture_array()
    cv2.imshow("Live OCR Feed", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        print("Capturing frame and performing OCR...")

        # 1. Image Preprocessing for improved accuracy
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Rescale the image for better OCR
        scale_factor = 2
        scaled_image = cv2.resize(gray_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        # Apply a Gaussian blur to remove noise
        denoised_image = cv2.GaussianBlur(scaled_image, (3, 3), 0)
        
        # Apply OTSU's thresholding
        thresh_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # 2. Perform OCR
        try:
            text = pytesseract.image_to_string(thresh_image)
            text = text.strip()

            if text:
                print("--- Recognized Text ---")
                print(text)
                print("-----------------------")
                
                # 3. Text-to-Speech Feedback
                engine.say(text)
                engine.runAndWait()
            else:
                print("No text detected in the captured frame.")
                engine.say("No text detected.")
                engine.runAndWait()
                
        except pytesseract.TesseractNotFoundError:
            print("Tesseract not found. Please ensure 'tesseract-ocr' is installed.")
            
    elif key == ord("q"):
        print("Exiting program.")
        break
        
# --- Cleanup ---
picam2.stop()
cv2.destroyAllWindows()
engine.stop()
