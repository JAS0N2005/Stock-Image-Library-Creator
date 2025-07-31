import os
from api_utils import fetch_unsplash_images, fetch_pexels_images, fetch_pixabay_images
from file_utils import save_image_from_url

def fetch_images_for_type(type_name, clean_type, output_folder, n_images, config):
    """
    Downloads images for a given type from all APIs. Uses clean_type for filenames for safety.
    Returns download statistics for logging.
    """
    apis = [
        ('unsplash', fetch_unsplash_images),
        ('pexels', fetch_pexels_images),
        ('pixabay', fetch_pixabay_images),
    ]
    sl_no = 1
    per_source = {}
    errors = []
    total_downloaded = 0

    for api_name, api_func in apis:
        per_source[api_name] = 0
        try:
            image_urls = api_func(type_name, n_images, config.get(api_name, {}))
        except Exception as e:
            errors.append(f"{api_name} API fetch failed: {e}")
            continue

        for url in image_urls:
            filename = f"{clean_type}_{sl_no}_STOCK.jpg"
            filepath = os.path.join(output_folder, filename)
            try:
                save_image_from_url(url, filepath)
                per_source[api_name] += 1
                total_downloaded += 1
            except Exception as e:
                errors.append(f"{api_name} download error: {e}")
            sl_no += 1

    return {"total": total_downloaded, "per_source": per_source, "errors": errors}