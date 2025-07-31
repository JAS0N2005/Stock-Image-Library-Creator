# Stock Image Automation Bot

This project automates the process of fetching royalty-free stock images for each unique "Type" in a dataset (such as POI types or business categories) using multiple public APIs (Unsplash, Pexels, Pixabay, Wikimedia). It maintains a type database (Excel), organizes images by type, and can resume after interruptions. **It is optimized for use with cloud drives (Google Drive, OneDrive, Dropbox) where the drive letter may change—no drive letters or absolute paths are stored.**

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Setup Instructions](#setup-instructions)
- [Configuration: `config.json`](#configuration-configjson)
  - [Parameter Descriptions](#parameter-descriptions)
  - [When to Use Each API](#when-to-use-each-api)
- [Module Descriptions](#module-descriptions)
- [Example Workflow](#example-workflow)
- [Resume Functionality](#resume-functionality)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Goal:**  
For every unique "Type" (e.g., "Bakery", "Museum", "Park") found in an Excel file, this tool downloads a batch of images from stock photo APIs, organizes them by type, and logs progress in a database. It is robust to interruptions and drive letter changes.

---

## How It Works

1. **Extracts all unique types** from a specified Excel column.
2. **Compares** extracted types to those in the database (`STOCK_DATABASE.xlsx` in the output folder) to find new types.
3. **Updates the database** with new types.
4. **For each new type:**
    - Creates a folder inside the output directory named after the type.
    - Fetches a specified number of images from each API.
    - Saves images using a consistent naming scheme.
    - Updates `RESUME_ROW` in config to allow safe resumption.

**No absolute paths or drive letters are stored.**  
The database always lives in the output folder. All type folders are children of the output folder.

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```

### Setup

1. **Configure API keys** (see `config.json`).
2. **Edit paths** in `config.json` to point to your Excel data and output folder.
3. **Run the script**:
    ```sh
    python main.py
    ```

---

## Configuration: `config.json`

```json
{
    "input_excel_path": ".../PENDING_REVIEW.xlsx",
    "type_column": "Type",
    "output_folder": ".../STOCK IMAGES",
    "n_images_per_api": 5,
    "unsplash": {"access_key": "YOUR-UNSPLASH-KEY"},
    "pexels":   {"api_key": "YOUR-PEXELS-KEY"},
    "pixabay":  {"api_key": "YOUR-PIXABAY-KEY"},
    "wikimedia": {},
    "RESUME_ROW": 0
}
```

### Parameter Descriptions

| Key                   | Description                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| input_excel_path      | Path to input Excel file listing all activities/POIs and their types.                                       |
| type_column           | Name of the column in Excel containing the type/category.                                                   |
| output_folder         | Base directory where images and the type database are stored.                                               |
| n_images_per_api      | Number of images to fetch from each API per type.                                                           |
| unsplash / pexels / pixabay | API credentials for respective services.                                                              |
| wikimedia             | (No credentials needed)                                                                                     |
| RESUME_ROW            | Index of the next type to process (auto-updated for resume).                                               |

#### When to Use Each API

- **Unsplash, Pexels, Pixabay:** For high-quality, royalty-free images. Most types will have good photo coverage here.
- **Wikimedia:** For types that might be underrepresented in stock APIs or for more "encyclopedic" images.

---

## Module Descriptions

### `main.py`
Coordinates the workflow:
- Loads config and paths.
- Extracts new types from Excel.
- Updates the type database (always `STOCK_DATABASE.xlsx` in the output folder).
- Iterates through new types, creating folders and fetching images.
- Updates `RESUME_ROW` in config for safe resumption.

### `type_extractor.py`
- `extract_types_from_excel(excel_path, type_column)`
- Reads the input Excel and returns all unique, non-empty types.

### `database_manager.py`
- `update_type_database(output_folder, types)` and `get_existing_types(output_folder)`
- Manages the type database (Excel) in the output folder.
- Only type names are stored—no folder paths.

### `image_fetcher.py`
- `fetch_images_for_type(type_name, output_folder, n_images, config)`
- For each API, fetches images and saves them in `output_folder/type_name/`.

### `api_utils.py`
- Calls each API and returns image URLs.

### `file_utils.py`
- Ensures folders exist and handles robust image download and saving.

---

## Example Workflow

1. Your `PENDING_REVIEW.xlsx` has a "Type" column with rows like "Bakery", "Museum", "Park", etc.
2. The tool finds all unique types not already present in `STOCK_DATABASE.xlsx` (in the output folder).
3. For each new type:
    - Creates a folder: `STOCK IMAGES/Bakery/`
    - Fetches images from Unsplash, Pexels, Pixabay, Wikimedia.
    - Images are saved as: `Bakery_1_STOCK.jpg`, `Bakery_2_STOCK.jpg`, ...
4. If interrupted, re-run: it skips already-processed types and continues.

---

## Resume Functionality

- `RESUME_ROW` in `config.json` is updated after each type is processed.
- If an error occurs or you stop the script, simply re-run:
    - It skips already-processed types and continues.

---

## Troubleshooting

- **Missing Images:** Check API keys and internet connection.
- **API Limits:** Each API may have rate limits. If you hit a limit, wait or use fewer images per run.
- **Excel Errors:** Ensure column names and file paths are correct and files are not open elsewhere.

---

## Contributing

By yours truly,
Subhojyoti :]

---