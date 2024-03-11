from scipy import ndimage
import os
import imageio
import numpy as np

def main():
    outPath = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/Drowsy_flipped"
    path = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/Drowsy"

    # Create the output directory if it doesn't exist
    os.makedirs(outPath, exist_ok=True)

    # Iterate through the names of contents of the folder
    for image_path in os.listdir(path):
        # Create the full input path and read the file
        input_path = os.path.join(path, image_path)
        image_to_flip = imageio.imread(input_path)

        # Flip the image horizontally
        flipped = np.fliplr(image_to_flip)

        # Create the full output path, 'example.jpg' 
        # becomes 'flipped_example.jpg', save the file to disk
        flipped_filename = 'flipped_' + image_path
        fullpath = os.path.join(outPath, flipped_filename)
        imageio.imwrite(fullpath, flipped)

        # Output the name of the flipped image
        print(f"Flipped and saved: {flipped_filename}")

if __name__ == '__main__':
    main()
