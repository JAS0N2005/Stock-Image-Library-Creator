import os
import re
import requests

def ensure_folder_exists(path):
    """Ensure a directory exists; create if missing."""
    os.makedirs(path, exist_ok=True)

def save_image_from_url(url, filepath):
    """Download and save an image from a URL."""
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    except Exception as e:
        print(f"Error: Failed to download {url}: {e}")

def clean_type_name(type_name):
    """Clean type name for valid folder/file usage. Returns None for NaN/bad input."""
    if not isinstance(type_name, str):
        return None
    cleaned = re.sub(r'[\\/:*?"<>|\r\n\t]', '', type_name).strip()
    return cleaned if cleaned else None