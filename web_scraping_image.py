from bing_image_downloader import downloader
import re  # For input validation


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

    # Download images
    try:
        downloader.download(category, limit, output_dir, adult_filter_off,
                            force_replace, timeout, verbose)
        print(f"Downloaded images for category in : '{category}'.")
    except Exception as e:
        print(f"Error downloading images: {e}")


if __name__ == "__main__":
    while True:
        category = input(
            "Enter the category you want to download images for (or 'q' to quit): ")
        if category.lower() == 'q':
            break

        limit = input(
            'Enter the number of images you would like: ')
        if limit.lower() == 'all':
            limit = None  # Download all available images
        else:
            try:
                limit = int(limit)
                if limit <= 0:
                    print("Limit must be a positive integer or 'all'.")
                    continue
            except ValueError:
                print("Invalid limit. Please enter a positive integer or 'all'.")
                continue

        download_images(category, limit)
