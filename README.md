# 📦 Image Organizer & Stock Filler

A Python automation tool that organizes activity folders with relevant stock images based on their **Type** from an Excel sheet. It integrates with **Unsplash**, **Pexels**, and **Pixabay APIs** to fetch relevant images and supports both **filling** and **cleaning** operations.

---

## 🚀 Features

- Fetches stock images based on activity "Type" from Excel.
- Integrates with Unsplash, Pexels, and Pixabay APIs.
- Organizes images into type-based folders and copies them into activity folders.
- Cleans up folders using "ActivityId".
- Tracks status of types using a persistent CSV database.

---

## 📁 Folder Structure

```
project-root/
│
├── main.py                  # Entry point
├── config.json              # Configuration for inputs, APIs, and output
├── requirements.txt         # Python dependencies
│
├── api_utils.py             # Fetch images from Unsplash, Pexels, Pixabay
├── config_loader.py         # Loads config.json
├── cleaner.py               # Handles folder deletion by ActivityId
├── database_manager.py      # Manages stock image database CSV
├── filler.py                # Core logic to copy images into folders
├── image_fetcher.py         # Image download coordinator
├── file_ops.py              # Directory helpers
├── file_utils.py            # Filename sanitization and file download helpers
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure `config.json`

Edit the paths and API keys as needed in `config.json`:

```json
{
  "image_organizer": {
    "pending_excel": "path/to/PENDING_REVIEW.xlsx",
    "output_dir": "path/to/PENDING",
    "mode": "FILL",
    "verbose": false
  },
  "stock_library": {
    "database_csv": "path/to/STOCK_DATABASE.csv",
    "type_column": "Type",
    "output_folder": "path/to/stock_images",
    "n_images_per_api": 5,
    "unsplash": {"access_key": "YOUR_UNSPLASH_KEY"},
    "pexels": {"api_key": "YOUR_PEXELS_KEY"},
    "pixabay": {"api_key": "YOUR_PIXABAY_KEY"}
  }
}
```

---

## ▶️ Running the Program

### **FILL Mode (Default)**

```bash
python main.py
```

- Reads Excel to get ActivityId and Type.
- Fills folders with stock images per Type.
- Tracks processed types in the stock database CSV.

### **CLEAN Mode**

Edit `config.json`:
```json
"mode": "CLEAN"
```

Then run:
```bash
python main.py
```

- Deletes folders for the ActivityIds listed in the Excel file.

---

## 📘 Excel Requirements

Your `PENDING_REVIEW.xlsx` must have:
- A column **`ActivityId`** (used for folder naming)
- A column **`Type`** (used to determine which stock images to use)

---

## 🧠 What Each Module Does

| Module | Purpose |
|--------|---------|
| `main.py` | Entry point. Loads config, Excel, and runs FILL or CLEAN mode. |
| `config_loader.py` | Loads settings from `config.json`. |
| `cleaner.py` | Deletes folders listed in the Excel sheet by ActivityId. |
| `filler.py` | Main logic for copying images from stock folders to activity folders. Also initializes the image database and updates it with new types. |
| `database_manager.py` | Reads/updates a CSV database that tracks types and their status (pending, success, failed). |
| `api_utils.py` | Contains functions for fetching image URLs from Unsplash, Pexels, and Pixabay. |
| `image_fetcher.py` | Uses all image APIs to download images for a given type and save them with clean filenames. |
| `file_ops.py` | Provides helper functions to create/delete folders. |
| `file_utils.py` | Sanitizes type names and handles image download and storage. |

---

## 📄 requirements.txt

Make sure this includes at least:
```
pandas
requests
tqdm
openpyxl
```

> If not present, create it manually or run:
```bash
pip freeze > requirements.txt
```

---

## 🧹 Ignored Files

Your `.gitignore` should include:
```
__pycache__/
.env/
.vscode/
*.log
*.db
*.sqlite3
*.pyc
desktop.ini
```

---

## ✅ Example Use Case

Imagine you have a list of 200 activities, each tagged as “Mountain”, “Beach”, or “Museum”. This program will:

- Download stock images related to those tags.
- Organize them into folders by tag.
- Copy relevant images into each activity folder for use in a review process or CMS.

---

## 📬 Questions or Contributions

Feel free to open issues or submit pull requests to improve the automation further!
