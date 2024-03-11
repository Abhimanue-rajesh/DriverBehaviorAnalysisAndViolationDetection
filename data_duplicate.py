import os
from PIL import Image
from imagehash import phash

def find_duplicate_images(directory):
    image_hashes = {}
    duplicates = []

    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            file_path = os.path.join(directory, filename)
            with Image.open(file_path) as img:
                hash_value = phash(img)
                if hash_value in image_hashes:
                    duplicates.append((file_path, image_hashes[hash_value]))
                else:
                    image_hashes[hash_value] = file_path
                    
    return duplicates

def remove_duplicate_images(duplicates):
    for duplicate in duplicates:
        print(f"Removing duplicate: {duplicate[0]}")
        os.remove(duplicate[0])

if __name__ == "__main__":
    directory_path = 'data/Drowsy'
    print('Finding Duplicates In',directory_path)
    duplicates = find_duplicate_images(directory_path)

    if duplicates:
        print(f"Found {len(duplicates)} duplicate images.")
        remove_duplicate_images(duplicates)
        print("Duplicates removed.")
    else:
        print("No duplicate images found.")