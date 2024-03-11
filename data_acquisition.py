import uuid  # Unique identifier
import os
import time
import cv2  # Open-Cv

# Create a directory - /data/images
IMAGES_PATH = os.path.join('new_data', 'unsorted')
labels = ['normal', 'drowsy', 'using_mobile']
number_imgs = 20


cap = cv2.VideoCapture(0)
for label in labels:
    print('Collecting images for {}'.format(label))
    time.sleep(5)

    # Loop through image range
    for img_num in range(number_imgs):
        print("Collecting images for {}, image number {}".format(label, img_num))
        # Webcam feed
        ret, frame = cap.read()
        # Render to the screen
        cv2.imshow("Data Collection", frame)

        # Naming out image path
        imgname = os.path.join(IMAGES_PATH, label +"." + str(uuid.uuid1()) + ".jpg")

        # Writes out image to file
        cv2.imwrite(imgname, frame)


        # 5 second delay between captures
        time.sleep(5)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
cap.release()
cv2.destroyAllWindows()
