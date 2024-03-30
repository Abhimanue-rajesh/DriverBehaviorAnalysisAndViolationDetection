import os  # Import the os module for interacting with the operating system
import cv2  # Import the OpenCV library for image processing
from tqdm import tqdm  # Import tqdm for displaying progress bars

# The directory in which all the data is located
data_directory = 'data' # TODO Change the directory here
# Define the wanted extensions for images
wanted_image_extension = ['.jpeg', '.jpg', '.bmp', '.png']

# Count total number of images
# This counts the total number of image files in the data directory and its subdirectories
total_images = sum(len(files) for _, _, files in os.walk(data_directory))

# Initialize tqdm with total number of images
# tqdm is used to display a progress bar during image processing
progress_bar = tqdm(total=total_images, desc="Processing images")

try:
    # Loop through each image class directory in the data directory
    for image_class in os.listdir(data_directory):
        # Loop through each image file in the current image class directory
        for image in os.listdir(os.path.join(data_directory, image_class)):
            # Construct the full path to the current image file
            image_path = os.path.join(data_directory, image_class, image)
            try:
                # Read the image using OpenCV
                to_check_image = cv2.imread(image_path)
                # Get the extension of the image file
                image_extension = os.path.splitext(image_path)[1]
                # Check if the image extension is not in the list of wanted extensions
                if image_extension not in wanted_image_extension:
                    # Print a message indicating that the image is not in the list of wanted extensions
                    print('\nImage not in list {}'.format(image_path))
                    # Remove the image file
                    os.remove(image_path)
                # Update the progress bar to indicate processing of one image
                progress_bar.update(1)
            except Exception as error:
                # Print a message indicating that there is an issue with the current image
                print('\nIssues with image {}'.format(image_path), error)
                # Update the progress bar to indicate processing of one image
                progress_bar.update(1)
except FileNotFoundError:
    # Print a message indicating that the specified directory was not found
    print('\nFile not Found in the directory!, Please Check the Data Directory')

# Close progress bar
# This closes the progress bar after all images have been processed
progress_bar.close()
