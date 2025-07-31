from tqdm import tqdm
from file_ops import delete_folder
import os

def run_clean(df, output_dir):
    stats = {'deleted': 0, 'missing': 0}
    for activity_id in tqdm(df['ActivityId'], desc="Cleaning folders", unit="folder"):
        target = os.path.join(output_dir, str(activity_id))
        if delete_folder(target):
            stats['deleted'] += 1
        else:
            stats['missing'] += 1
    print(f"Clean complete: {stats['deleted']} folders deleted, {stats['missing']} not found.")
