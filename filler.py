import os
import shutil
import pandas as pd
from tqdm import tqdm
from file_utils import clean_type_name, ensure_folder_exists
from image_fetcher import fetch_images_for_type
from database_manager import (
    read_database,
    mark_type_status,
    initialize_database_from_excel,
    add_missing_types,
    STATUS_PENDING,
    STATUS_SUCCESS,
    STATUS_FAILED
)

def update_missing_types(df, stock_cfg):
    """
    Add missing valid types to the database and fetch images only for them.
    Skips any NaN, empty, or invalid types.
    """
    # Clean and filter valid types only
    types = [clean_type_name(t) for t in df['Type'].dropna().unique()]
    types = [t for t in types if t]  # skip None/empty after cleaning

    add_missing_types(stock_cfg['output_folder'], types)

    api_config = {k: stock_cfg[k] for k in ['unsplash', 'pexels', 'pixabay']}
    n_images = stock_cfg['n_images_per_api']
    stock_images_dir = stock_cfg['output_folder']

    for t in types:
        tqdm.write(f"Fetching images for type '{t}'...")
        # Create type-specific folder for images
        type_folder = os.path.join(stock_images_dir, t)
        ensure_folder_exists(type_folder)
        stats = fetch_images_for_type(
            type_name=t,
            clean_type=t,
            output_folder=type_folder,  # Store inside each type folder
            n_images=n_images,
            config=api_config
        )
        status = STATUS_SUCCESS if stats.get("total", 0) > 0 else STATUS_FAILED
        mark_type_status(stock_cfg['output_folder'], t, status)
        tqdm.write(f"→ {status.upper()}: {stats.get('total', 0)} images for '{t}'")

def run_fill(df, img_cfg, stock_cfg):
    """
    Main fill pipeline.
    Copies images from type folders to each activity folder, skipping NaN/invalid values.
    """
    total = len(df)
    unique_types = df['Type'].nunique()
    tqdm.write(f"Mode: FILL | Total activities: {total} | Unique types: {unique_types}")

    # Initialize DB if needed and update missing types
    initialize_database_from_excel(
        stock_cfg['output_folder'],
        stock_cfg.get('input_excel', ''),
        stock_cfg.get('type_column', 'Type')
    )
    update_missing_types(df, stock_cfg)

    db_df = read_database(stock_cfg['output_folder'])
    stock_images_dir = stock_cfg['output_folder']
    output_dir = img_cfg['output_dir']
    verbose = img_cfg.get('verbose', False)

    for _, row in tqdm(df.iterrows(), total=total, desc="Filling folders", unit="act"):
        activity_id = str(row['ActivityId'])
        type_name = row['Type']
        clean_type = clean_type_name(type_name)
        # Skip missing/NaN activity or type
        if not activity_id or not clean_type:
            continue
        target_folder = os.path.join(output_dir, activity_id)
        ensure_folder_exists(target_folder)
        stock_folder = os.path.join(stock_images_dir, clean_type)
        # Only copy from valid type folders
        if os.path.exists(stock_folder):
            images = [fn for fn in os.listdir(stock_folder) if fn.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for fn in images:
                shutil.copy2(os.path.join(stock_folder, fn), os.path.join(target_folder, fn))
            if verbose:
                tqdm.write(f"[{activity_id}] Copied {len(images)} '{type_name}' images.")
        else:
            tqdm.write(f"Warning: No images found for type '{type_name}' in the stock folder.")

    tqdm.write("✓ Fill complete: all pending activities processed.")
