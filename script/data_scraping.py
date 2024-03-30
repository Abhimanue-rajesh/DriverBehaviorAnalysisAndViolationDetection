from bing_image_downloader import downloader  # Import the downloader module from bing_image_downloader
import re  # Import the re module for regular expressions (used for input validation)

# Function to download images from Bing Image Search
def download_images(category, limit=100, output_dir='UnsortedImageData',
                    adult_filter_off=True, force_replace=False,
                    timeout=60, verbose=True):

    # Input validation with enhanced error messages and user guidance
    if not re.match(r"^[a-zA-Z0-9_ ]+$", category):
        print("Invalid category name. Please enter a valid category using only letters, numbers, spaces, and underscores.")
        return

    try:
        limit = int(limit)
        if limit <= 0:
            print("Limit must be a positive integer.")
            return
    except ValueError:
        print("Invalid limit. Please enter a positive integer.")
        return

    # Download images using the downloader module
    try:
        downloader.download(category, limit, output_dir, adult_filter_off,
                            force_replace, timeout, verbose)
        print(f"Downloaded images for category: '{category}'.")
    except Exception as e:
        print(f"Error downloading images: {e}")

# Main function
if __name__ == "__main__":
    while True:
        # Prompt the user to enter a category for image download
        category = input(
            "Enter the category you want to download images for (or 'q' to quit): ")
        if category.lower() == 'q':
            break  # Exit the loop if the user enters 'q'

        # Prompt the user to enter the number of images they would like to download
        limit = input(
            'Enter the number of images you would like (or enter "all" to download all available images): ')
        if limit.lower() == 'all':
            limit = None  # Download all available images if the user enters 'all'
        else:
            try:
                limit = int(limit)
                if limit <= 0:
                    print("Limit must be a positive integer or 'all'.")
                    continue
            except ValueError:
                print("Invalid limit. Please enter a positive integer or 'all'.")
                continue

        # Call the download_images function with the provided category and limit
        download_images(category, limit)
