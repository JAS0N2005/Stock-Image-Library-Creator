import pandas as pd
from config_loader import load_config
from cleaner import run_clean
from filler import run_fill

def main():
    cfg = load_config()
    img_cfg = cfg['image_organizer']
    stock_cfg = cfg['stock_library']
    # Load pending review Excel
    df = pd.read_excel(img_cfg['pending_excel'], dtype={'ActivityId': str, 'Type': str})
    # Filter out invalid/NaN ActivityId and Type
    df = df[(df['ActivityId'].notna()) & (df['Type'].notna())]
    if 'ActivityId' not in df.columns or 'Type' not in df.columns:
        raise ValueError("PENDING sheet must have 'ActivityId' and 'Type' columns.")
    mode = img_cfg.get('mode', 'FILL').upper()
    if mode == 'CLEAN':
        run_clean(df, img_cfg['output_dir'])
    else:
        run_fill(df, img_cfg, stock_cfg)

if __name__ == '__main__':
    main()