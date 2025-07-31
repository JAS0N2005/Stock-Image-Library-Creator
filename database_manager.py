import os
from api_utils import fetch_unsplash_images, fetch_pexels_images, fetch_pixabay_images
from file_utils import save_image_from_url, ensure_folder_exists

import pandas as pd
import os
from file_utils import clean_type_name

STATUS_PENDING = "pending"
STATUS_SUCCESS = "success"
STATUS_FAILED = "failed"

def get_database_path(output_folder):
    return os.path.join(output_folder, "STOCK_DATABASE.csv")

def initialize_database_from_excel(output_folder, input_excel, type_column):
    """Create database CSV from Excel if missing. Only valid types, all start as pending."""
    db_csv = get_database_path(output_folder)
    if os.path.exists(db_csv):
        return
    df = pd.read_excel(input_excel)
    types = [clean_type_name(t) for t in df[type_column].dropna().unique()]
    types = [t for t in types if t]  # skip None
    db_df = pd.DataFrame({'CleanType': types, 'status': STATUS_PENDING})
    db_df.to_csv(db_csv, index=False)

def read_database(output_folder):
    db_csv = get_database_path(output_folder)
    return pd.read_csv(db_csv)

def get_pending_types(output_folder):
    df = read_database(output_folder)
    return df[df['status'] == STATUS_PENDING].copy()

def add_missing_types(output_folder, types):
    db_csv = get_database_path(output_folder)
    db_df = read_database(output_folder)
    existing_types = set(db_df['CleanType'].dropna())
    new_types = [t for t in types if t and t not in existing_types]
    if not new_types:
        return
    new_df = pd.DataFrame({'CleanType': new_types, 'status': STATUS_PENDING})
    db_df = pd.concat([db_df, new_df], ignore_index=True)
    db_df.to_csv(db_csv, index=False)  # atomic write

def mark_type_status(output_folder, clean_type, status):
    db_csv = get_database_path(output_folder)
    df = pd.read_csv(db_csv)
    df.loc[df['CleanType'] == clean_type, 'status'] = status
    df.to_csv(db_csv, index=False)  # atomic write

def fetch_images_for_type(type_name, clean_type, output_folder, n_images, config):
    """
    Downloads images for a given type from all APIs into output_folder/<CleanType>/.
    Skips if clean_type is None.
    """
    if not clean_type:
        return {"total": 0, "per_source": {}, "errors": ["Invalid type name"]}
    folder = os.path.join(output_folder, clean_type)
    ensure_folder_exists(folder)
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
            filepath = os.path.join(folder, filename)
            try:
                save_image_from_url(url, filepath)
                per_source[api_name] += 1
                total_downloaded += 1
            except Exception as e:
                errors.append(f"{api_name} download error: {e}")
            sl_no += 1
    return {"total": total_downloaded, "per_source": per_source, "errors": errors}

