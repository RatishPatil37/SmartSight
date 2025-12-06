# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Find a suitable English voice, or use the first one
found_voice = None
for voice in voices:
    # Use 'en' as a general check for English language
    if 'en' in voice.languages or 'english' in voice.id.lower():
        found_voice = voice.id
        break
if found_voice:
    engine.setProperty("voice", found_voice)
else:
    print("Warning: No suitable English voice found. Using default.")

engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# --- Welcome Message ---
welcome_text = " System initialized. Starting object detection."
print(welcome_text)
engine.say(welcome_text)
engine.runAndWait()  # Wait for the welcome message to finish speaking

# Set up the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (900, 900)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load YOLOv8 model
model = YOLO("yolov5su_ncnn_model")

# --- Main Loop ---
# Time interval for announcements to avoid rapid, confusing speech
tts_interval = 3.0
last_tts_time = time.time() - tts_interval  # Initialize to speak immediately

while True:
    # Capture a frame
    frame = picam2.capture_array()

    # Run YOLO model
    results = model(frame)
    annotated_frame = results[0].plot(boxes=True, masks=False)

    # Text-to-Speech logic for all detected objects
    current_time = time.time()
    if current_time - last_tts_time >= tts_interval:
        detections = []
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls)
                class_name = model.names[class_id]
                confidence = float(box.conf)

                if confidence > 0.6:  # Announce all objects with high confidence
                    detections.append(class_name)

        if detections:
            # Combine multiple detections into a single sentence
            unique_detections = sorted(list(set(detections)))
            announcement_text = "Detected: " + ", ".join(unique_detections) + "."
            
            engine.say(announcement_text)
            engine.runAndWait()
            last_tts_time = current_time  # Update the last announcement time

    # Display inference time and FPS
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time
    text = f'FPS: {fps:.1f}'

    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = annotated_frame.shape[1] - text_size[0] - 10
    text_y = text_size[1] + 10

    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow("Camera", annotated_frame)

    # Exit program
    if cv2.waitKey(1) == ord("q"):
        break

# --- Cleanup ---
cv2.destroyAllWindows()
engine.stop()
