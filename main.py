#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path

def download_image(image_url: str, save_path: Path) -> bool:
    """
    Download image from URL and save it to specified path.

    Parameters:
    image_url (str): The URL of the image to download.
    save_path (Path): The path where the downloaded image will be saved.

    Returns:
    bool: True if the image is successfully downloaded and saved, False otherwise.
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Extract filename from URL or use a default
        filename = os.path.basename(urlparse(image_url).path)
        if not filename:
            filename = 'image.jpg'

        file_path = save_path / filename

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"Failed to download image {image_url}: {e}")
        return False


def get_page_metadata(url: str) -> tuple[str | None, str | None, str | None]:
    """
    Extract og:image URL, title, and description from a given web page URL.

    This function fetches the HTML content of the specified URL and parses it to extract
    the Open Graph image URL, page title, and meta description.

    Parameters:
    url (str): The URL of the web page to extract metadata from.

    Returns:
    tuple[str | None, str | None, str | None]: A tuple containing three elements:
        - og_image_url (str | None): The URL of the Open Graph image, or None if not found.
        - title_text (str | None): The text content of the page's title tag, or None if not found.
        - desc_text (str | None): The content of the meta description tag, or None if not found.

    If an error occurs during processing, all three return values will be None.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get title from <title> tag
        title = soup.find('title')
        title_text = title.text.strip() if title else None

        # Get og:image
        og_image = soup.find('meta', property='og:image')
        og_image_url = urljoin(url, og_image['content']) if og_image and og_image.get('content') else None

        # Get description
        description = soup.find('meta', attrs={'name': 'description'})
        desc_text = description['content'].strip() if description and description.get('content') else None

        return og_image_url, title_text, desc_text
    except Exception as e:
        print(f"Failed to process URL {url}: {e}")
        return None, None, None


def save_metadata(url: str, title: str | None, description: str | None, save_path: Path) -> bool:
    """
    Save metadata (URL, title, and description) to a text file.

    This function creates a text file named after the domain of the URL
    and writes the provided metadata into it.

    Parameters:
    url (str): The URL of the webpage.
    title (str | None): The title of the webpage. If None, 'Not found' will be written.
    description (str | None): The description of the webpage. If None, 'Not found' will be written.
    save_path (Path): The directory path where the metadata file will be saved.

    Returns:
    bool: True if the metadata is successfully saved, False otherwise.
    """
    try:
        # Create a filename from the URL
        filename = urlparse(url).netloc + '.txt'
        file_path = save_path / filename

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n\n")
            f.write(f"Title: {title or 'Not found'}\n\n")
            f.write(f"Description: {description or 'Not found'}\n")

        return True
    except Exception as e:
        print(f"Failed to save metadata for {url}: {e}")
        return False


def main():
    """
    Main entry point for the application.

    This function orchestrates the process of reading URLs from a file,
    fetching metadata and og:image for each URL, downloading images,
    and saving metadata to files.

    The function performs the following steps:
    1. Creates a 'dist' directory if it doesn't exist.
    2. Reads URLs from a 'urls.txt' file.
    3. For each URL:
       - Retrieves the og:image URL, title, and description.
       - Downloads the og:image if found.
       - Saves the metadata (URL, title, description) to a file.

    Returns:
        int: 0 if the process completes successfully, 1 if an error occurs.
    """
    try:
        print("Application starting...")

        # Create dist directory if it doesn't exist
        dist_path = Path('dist')
        dist_path.mkdir(exist_ok=True)

        # Read URLs from file
        with open('urls.txt', 'r') as f:
            urls = [line.strip() for line in f if line.strip()]

        for url in urls:
            print(f"Processing {url}")
            og_image_url, title, description = get_page_metadata(url)

            if og_image_url:
                print(f"Found og:image: {og_image_url}")
                if download_image(og_image_url, dist_path):
                    print(f"Successfully downloaded image from {url}")
            else:
                print(f"No og:image found for {url}")

            if save_metadata(url, title, description, dist_path):
                print(f"Successfully saved metadata for {url}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
