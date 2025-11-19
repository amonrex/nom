import requests
import os
from urllib.parse import urlparse
import hashlib

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Accept multiple URLs from the user
    urls = input("Enter one or more image URLs (separate by spaces): ").split()

    # Create directory if it doesn't exist
    folder_name = "Fetched_Images"
    os.makedirs(folder_name, exist_ok=True)

    # Keep track of downloaded image hashes to prevent duplicates
    downloaded_hashes = set()

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or "downloaded_image.jpg"
            filepath = os.path.join(folder_name, filename)

            # --- Precautions before saving ---
            # 1. Check content type (ensure it's an image)
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped {url} — not an image (Content-Type: {content_type})")
                continue

            # 2. Compute hash to detect duplicates
            image_hash = hashlib.md5(response.content).hexdigest()
            if image_hash in downloaded_hashes:
                print(f"✗ Skipped duplicate image: {filename}")
                continue

            downloaded_hashes.add(image_hash)

            # 3. Save image safely
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error fetching {url}: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()