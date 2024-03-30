from scipy import ndimage  # Import the ndimage module from scipy for image manipulation
import os  # Import the os module for interacting with the operating system
import imageio  # Import the imageio library for reading and writing images
import numpy as np  # Import numpy for numerical operations

def main():
    # Specify the output directory for flipped images
    outPath = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/Drowsy_flipped"
    # Specify the input directory containing original images
    path = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/Drowsy"

    # Create the output directory if it doesn't exist
    os.makedirs(outPath, exist_ok=True)

    # Iterate through the images in the input directory
    for image_path in os.listdir(path):
        # Create the full input path for the current image
        input_path = os.path.join(path, image_path)
        # Read the image using imageio.imread()
        image_to_flip = imageio.imread(input_path)

        # Flip the image horizontally using numpy.fliplr()
        flipped = np.fliplr(image_to_flip)

        # Create the full output path for the flipped image
        flipped_filename = 'flipped_' + image_path
        fullpath = os.path.join(outPath, flipped_filename)
        # Save the flipped image to disk using imageio.imwrite()
        imageio.imwrite(fullpath, flipped)

        # Output the name of the flipped image
        print(f"Flipped and saved: {flipped_filename}")

if __name__ == '__main__':
    main()  # Call the main function if the script is executed directly
