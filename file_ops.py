import os
import shutil

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def delete_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        return True
    return False
