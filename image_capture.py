import os
import time
import cv2

# Create a directory to store captured images
output_directory = "captured_images"
os.makedirs(output_directory, exist_ok=True)

cap = cv2.VideoCapture(0)

# Webcam feed
ret, frame = cap.read()

# Render to the screen
cv2.imshow("Image Collection", frame)

# Add a delay (e.g., 5000 milliseconds for 5 seconds)
cv2.waitKey(5000)

# Close the window
cv2.destroyAllWindows()

# Naming our image path with a timestamp
img_name = os.path.join(output_directory, f"captured_image_{int(time.time())}.jpg")

# Writes out the image to the file
cv2.imwrite(img_name, frame)

cap.release()
