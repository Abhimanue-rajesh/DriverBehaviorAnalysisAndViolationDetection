import cv2  # Import the OpenCV library for image processing
import os  # Import the os module for interacting with the operating system

def adjust_contrast(image, alpha, beta):
    """
    Adjusts the contrast of an image using the formula: new_pixel = alpha * pixel + beta
    """
    # Apply the contrast adjustment to the image using cv2.convertScaleAbs()
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

def main():
    # Specify input and output paths for original and adjusted images
    input_path = "data/Normal" # TODO Change the path to the desired directory
    output_path_increase = "data/Normal_increase"
    output_path_decrease = "data/Normal_decrease"

    # Create output directories if they don't exist
    os.makedirs(output_path_increase, exist_ok=True)
    os.makedirs(output_path_decrease, exist_ok=True)

    # Iterate through the images in the input directory
    for image_path in os.listdir(input_path):
        # Create the full input path for the current image
        input_image_path = os.path.join(input_path, image_path)
        # Read the original image using cv2.imread()
        original_image = cv2.imread(input_image_path)

        # Increase contrast
        increased_contrast = adjust_contrast(original_image, alpha=1.5, beta=0)
        # Create the full output path for the increased contrast image
        output_path_increase_img = os.path.join(output_path_increase, 'increased_' + image_path)
        # Write the increased contrast image to the output path using cv2.imwrite()
        cv2.imwrite(output_path_increase_img, increased_contrast)
        print(f"Increased contrast and saved: {output_path_increase_img}")

        # Decrease contrast
        decreased_contrast = adjust_contrast(original_image, alpha=0.5, beta=0)
        # Create the full output path for the decreased contrast image
        output_path_decrease_img = os.path.join(output_path_decrease, 'decreased_' + image_path)
        # Write the decreased contrast image to the output path using cv2.imwrite()
        cv2.imwrite(output_path_decrease_img, decreased_contrast)
        print(f"Decreased contrast and saved: {output_path_decrease_img}")

if __name__ == '__main__':
    main()  # Call the main function if the script is executed directly
