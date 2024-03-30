from scipy import ndimage  # Import the ndimage module from scipy for image manipulation
import os  # Import the os module for interacting with the operating system
import imageio  # Import the imageio library for reading and writing images

def main():
    # Specify the output directory for rotated images
    outPath = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/rotated"
    # Specify the input directory containing images to be rotated
    path = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/To_rotate"

    # Create the output directory if it doesn't exist
    os.makedirs(outPath, exist_ok=True)

    # Iterate through the images in the input directory
    for image_path in os.listdir(path):
        # Create the full input path for the current image
        input_path = os.path.join(path, image_path)
        # Read the image using imageio.imread()
        image_to_rotate = imageio.imread(input_path)

        # Rotate the image by 5 degrees clockwise using ndimage.rotate()
        rotated = ndimage.rotate(image_to_rotate, 5)

        # Create the full output path for the rotated image
        rotated_filename = 'rotated_' + image_path
        fullpath = os.path.join(outPath, rotated_filename)
        # Save the rotated image to disk using imageio.imwrite()
        imageio.imwrite(fullpath, rotated)

        # Output the name of the rotated image
        print(f"Rotated and saved: {rotated_filename}")

if __name__ == '__main__':
    main()  # Call the main function if the script is executed directly
