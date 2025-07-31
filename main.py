import os
import json
from database_manager import (
    initialize_database_from_excel,
    read_database,
    mark_type_successful,
)
from image_fetcher import fetch_images_for_type
from file_utils import ensure_folder_exists

def main():
    config_path = "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    input_excel = config["input_excel_path"]
    type_column = config["type_column"]
    output_folder = config["output_folder"]

    # Step 1: Initialize database from Excel if not present
    initialize_database_from_excel(output_folder, input_excel, type_column)

    # Step 2: Read database and print stats
    db = read_database(output_folder)
    total_pending = (db['status'] == 'pending download').sum()
    total_downloaded = (db['status'] == 'successfully downloaded from all 3 sources').sum()
    grand_total = len(db)
    print(f"Total types pending download: {total_pending}")
    print(f"Total types already downloaded: {total_downloaded}")
    print(f"Grand total types in the database: {grand_total}")

    # Step 3: Work only on pending types
    pending_types = db[db['status'] == 'pending download']
    if len(pending_types) == 0:
        print("All types have been processed. Nothing to do.")
        return

    # Step 4: Download for each pending type using efficient itertuples
    for row in pending_types.itertuples(index=False):
        type_name = row.Type
        clean_type = row.CleanType
        type_folder = os.path.join(output_folder, clean_type)
        ensure_folder_exists(type_folder)
        stats = fetch_images_for_type(
            type_name, clean_type, output_folder=type_folder, n_images=config["n_images_per_api"], config=config
        )

        # Concise summary print
        summary = f"[{type_name}] total: {stats['total']} | " + \
                  " | ".join(f"{src.title()}: {cnt}" for src, cnt in stats['per_source'].items())
        print(summary)
        if stats['errors']:
            print(f"  Errors: {len(stats['errors'])} - {stats['errors'][0]}")

        mark_type_successful(output_folder, clean_type)

if __name__ == "__main__":
    main()