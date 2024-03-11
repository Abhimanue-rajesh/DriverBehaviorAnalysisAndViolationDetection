import cv2
import os

def adjust_contrast(image, alpha, beta):
    """
    Adjusts the contrast of an image using the formula: new_pixel = alpha * pixel + beta
    """
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

def main():
    input_path = "data/Normal"
    output_path_increase = "data/Normal_increase"
    output_path_decrease = "data/Normal_decrease"

    # Create output directories if they don't exist
    os.makedirs(output_path_increase, exist_ok=True)
    os.makedirs(output_path_decrease, exist_ok=True)

    # Iterate through the names of contents of the folder
    for image_path in os.listdir(input_path):
        # Create the full input path and read the file
        input_image_path = os.path.join(input_path, image_path)
        original_image = cv2.imread(input_image_path)

        # Increase contrast
        increased_contrast = adjust_contrast(original_image, alpha=1.5, beta=0)
        output_path_increase_img = os.path.join(output_path_increase, 'increased_' + image_path)
        cv2.imwrite(output_path_increase_img, increased_contrast)
        print(f"Increased contrast and saved: {output_path_increase_img}")

        # Decrease contrast
        decreased_contrast = adjust_contrast(original_image, alpha=0.5, beta=0)
        output_path_decrease_img = os.path.join(output_path_decrease, 'decreased_' + image_path)
        cv2.imwrite(output_path_decrease_img, decreased_contrast)
        print(f"Decreased contrast and saved: {output_path_decrease_img}")

if __name__ == '__main__':
    main()
