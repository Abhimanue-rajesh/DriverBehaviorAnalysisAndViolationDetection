import os
import cv2
from tqdm import tqdm

# The directory in which all the data is located
data_directory = 'data'
# Define the wanted extensions
wanted_image_extension = ['.jpeg', '.jpg', '.bmp', '.png']

# Count total number of images
total_images = sum(len(files) for _, _, files in os.walk(data_directory))

# Initialize tqdm with total number of images
progress_bar = tqdm(total=total_images, desc="Processing images")

try:
    for image_class in os.listdir(data_directory):
        for image in os.listdir(os.path.join(data_directory, image_class)):
            image_path = os.path.join(data_directory, image_class, image)
            try:
                to_check_image = cv2.imread(image_path)
                image_extension = os.path.splitext(image_path)[1]
                if image_extension not in wanted_image_extension:
                    print('\nImage not in list {}'.format(image_path))
                    os.remove(image_path)
                progress_bar.update(1)

            except Exception as error:
                print('\nIssues with image {}'.format(image_path), error)
                progress_bar.update(1)
except FileNotFoundError:
    print('\nFile not Found in the directory!, Please Check the Data Directory')

# Close progress bar
progress_bar.close()
