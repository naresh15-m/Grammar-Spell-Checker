import cv2

# Load the face detection classifier
face_cap = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture
video_cap = cv2.VideoCapture(0)

while True:
    ret, video_data = video_cap.read()
    if not ret:  # Check if frame was captured successfully
        break
    
    # Convert to grayscale (CORRECTED color conversion)
    gray = cv2.cvtColor(video_data, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cap.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(video_data, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Show the video
    cv2.imshow("Video_live", video_data)
    
    # Exit if 'a' is pressed
    if cv2.waitKey(10) == ord("a"):
        break

# Clean up
video_cap.release()
cv2.destroyAllWindows()
