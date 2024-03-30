import os  # Import the os module for interacting with the operating system
from PIL import Image  # Import the Image module from the PIL library for image processing
from imagehash import phash  # Import the phash function from the imagehash module for image hashing

# Function to find duplicate images in a directory
def find_duplicate_images(directory):
    image_hashes = {}  # Create a dictionary to store image hashes
    duplicates = []  # Create a list to store duplicate image pairs

    # Iterate over files in the specified directory
    for filename in os.listdir(directory):
        # Check if the file is an image file (jpg, jpeg, png, gif)
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            file_path = os.path.join(directory, filename)  # Construct the full file path
            with Image.open(file_path) as img:  # Open the image file
                hash_value = phash(img)  # Compute the perceptual hash of the image
                # Check if the hash value already exists in the dictionary
                if hash_value in image_hashes:
                    duplicates.append((file_path, image_hashes[hash_value]))  # Add the duplicate pair to the list
                else:
                    image_hashes[hash_value] = file_path  # Store the hash value and file path in the dictionary
                    
    return duplicates  # Return the list of duplicate image pairs

# Function to remove duplicate images from a directory
def remove_duplicate_images(duplicates):
    # Iterate over each duplicate pair
    for duplicate in duplicates:
        print(f"Removing duplicate: {duplicate[0]}")  # Print the path of the duplicate image to be removed
        os.remove(duplicate[0])  # Remove the duplicate image file

# Main function
if __name__ == "__main__":
    # TODO Change the path to the desired directory
    directory_path = 'data/Drowsy'  # Specify the directory containing images
    print('Finding Duplicates In',directory_path)  # Print a message indicating the directory being processed
    duplicates = find_duplicate_images(directory_path)  # Find duplicate images in the specified directory

    # Check if duplicate images were found
    if duplicates:
        print(f"Found {len(duplicates)} duplicate images.")  # Print the number of duplicate image pairs found
        remove_duplicate_images(duplicates)  # Remove duplicate images from the directory
        print("Duplicates removed.")  # Print a message indicating that duplicate images were removed
    else:
        print("No duplicate images found.")  # Print a message indicating that no duplicate images were found
