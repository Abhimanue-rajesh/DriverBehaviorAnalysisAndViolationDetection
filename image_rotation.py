from scipy import ndimage
import os
import imageio

def main():
    outPath = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/rotated"
    path = "P:/MachineLearning/DriverBehaviorAnalysisAndViolationDetection/data/To_rotate"

    # Create the output directory if it doesn't exist
    os.makedirs(outPath, exist_ok=True)

    # Iterate through the names of contents of the folder
    for image_path in os.listdir(path):
        # Create the full input path and read the file
        input_path = os.path.join(path, image_path)
        image_to_rotate = imageio.imread(input_path)

        # Rotate the image by 45 degrees
        rotated = ndimage.rotate(image_to_rotate, 5)

        # Create the full output path, 'example.jpg' 
        # becomes 'rotated_example.jpg', save the file to disk
        rotated_filename = 'rotated_' + image_path
        fullpath = os.path.join(outPath, rotated_filename)
        imageio.imwrite(fullpath, rotated)

        # Output the name of the rotated image
        print(f"Rotated and saved: {rotated_filename}")

if __name__ == '__main__':
    main()
