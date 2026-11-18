import random
import re
from urllib.parse import unquote, urljoin

import requests

SITE_URL = "https://benjifriedman.com"

# Gallery pages on the site that images can be drawn from.
GALLERIES = [
    {"path": "/digital-abstract", "title": "Digital Abstract"},
    {"path": "/low-cfg-series", "title": "Low CFG Series"},
]


def get_random_website_image():
    """Pick a random image from one of the gallery pages on benjifriedman.com.

    A gallery is chosen at random first, then an image from it. If that
    gallery can't be fetched, the other galleries are tried.

    Returns a dict with url, page_url and title, or None if no gallery
    could be read.
    """
    galleries = random.sample(GALLERIES, len(GALLERIES))
    for gallery in galleries:
        try:
            image = _fetch_gallery_image(gallery)
        except Exception as e:
            print(f"Website image error for {gallery['path']}: {e}")
            continue
        if image:
            return image
    return None


def _fetch_gallery_image(gallery):
    page_url = SITE_URL + gallery["path"]
    response = requests.get(page_url, timeout=20)
    response.raise_for_status()

    # The page serves images through Next.js (/_next/image?url=<original path>).
    # Extract the original path so the README links to the original file.
    encoded_paths = re.findall(r'<img[^>]*?\ssrc="/_next/image\?url=([^&"]+)', response.text)
    paths = sorted({unquote(p) for p in encoded_paths})
    if not paths:
        return None

    return {
        "url": urljoin(SITE_URL, random.choice(paths)),
        "page_url": page_url,
        "title": gallery["title"],
    }
