import os
import requests
import re

def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_image_from_url(url, filepath):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"        Error: Failed to download {url} (status {r.status_code})")
    except Exception as e:
        print(f"        Error: Failed to download {url}: {e}")

def clean_type_name(type_name):
    """
    Removes characters from type_name that are invalid in folder/file names.
    This includes: \ / : * ? " < > | and control characters.
    """
    # Windows forbidden: \ / : * ? " < > | and ASCII control chars
    return re.sub(r'[\\/:*?"<>|\r\n\t]', '', type_name)