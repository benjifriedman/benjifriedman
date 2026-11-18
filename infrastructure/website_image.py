import random
import re
from urllib.parse import unquote, urljoin

import requests

SITE_URL = "https://benjifriedman.com"
GALLERY_PATH = "/digital-abstract"


def get_random_website_image():
    """Pick a random image from the gallery page on benjifriedman.com.

    Returns a dict with url, page_url and title, or None if the page
    can't be fetched or contains no images.
    """
    try:
        return _fetch_website_image()
    except Exception as e:
        print(f"Website image error, skipping image: {e}")
        return None


def _fetch_website_image():
    page_url = SITE_URL + GALLERY_PATH
    response = requests.get(page_url, timeout=20)
    response.raise_for_status()

    # The page serves images through Next.js (/_next/image?url=<original path>).
    # Extract the original path so the README links to the original file.
    encoded_paths = re.findall(r'<img[^>]*?\ssrc="/_next/image\?url=([^&"]+)', response.text)
    paths = sorted({unquote(p) for p in encoded_paths})
    if not paths:
        return None

    path = random.choice(paths)
    return {
        "url": urljoin(SITE_URL, path),
        "page_url": page_url,
        "title": "Digital Abstract",
    }
