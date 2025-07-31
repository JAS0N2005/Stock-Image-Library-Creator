import requests

def fetch_unsplash_images(query, n, api_config):
    access_key = api_config.get("access_key")
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page={n}"
    headers = {"Authorization": f"Client-ID {access_key}"}
    r = requests.get(url, headers=headers)
    data = r.json()
    return [img["urls"]["regular"] for img in data.get("results", [])]

def fetch_pexels_images(query, n, api_config):
    api_key = api_config.get("api_key")
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={n}"
    headers = {"Authorization": api_key}
    r = requests.get(url, headers=headers)
    data = r.json()
    return [photo["src"]["large"] for photo in data.get("photos", [])]

def fetch_pixabay_images(query, n, api_config):
    api_key = api_config.get("api_key")
    url = f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&per_page={n}"
    r = requests.get(url)
    data = r.json()
    return [img["largeImageURL"] for img in data.get("hits", [])]
