import os
import argparse
from PIL import Image
import pytesseract
import logging
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import re
from datetime import datetime

def setup_logging():
    logging.basicConfig(filename='ocr_errors.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def process_image(image_path):
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
        return image_path, text
    except Exception as e:
        logging.error(f"Error processing image {image_path}: {str(e)}")
        return image_path, ""

def extract_timestamp(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2}-\d{2}_\d{2}_\d{2})', filename)
    return match.group(1) if match else filename

def get_latest_image_timestamp(directory):
    image_files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
    if not image_files:
        return None
    return max(datetime.strptime(extract_timestamp(f), '%Y-%m-%d-%H_%M_%S') for f in image_files)

def process_chapter(chapter_dir):
    image_files = [f for f in os.listdir(chapter_dir) if f.lower().endswith('.png')]
    image_files.sort(key=lambda x: extract_timestamp(x))

    results = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_image, os.path.join(chapter_dir, img)) for img in image_files]
        for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing {os.path.basename(chapter_dir)}"):
            results.append(future.result())

    results.sort(key=lambda x: extract_timestamp(os.path.basename(x[0])))
    return "\n\n".join(text for _, text in results)

def process_book(book_dir, output_dir, incremental):
    book_name = os.path.basename(book_dir)
    chapter_dirs = [d for d in os.listdir(book_dir) if os.path.isdir(os.path.join(book_dir, d))]
    
    for chapter in tqdm(chapter_dirs, desc=f"Processing chapters of {book_name}"):
        chapter_path = os.path.join(book_dir, chapter)
        output_filename = f"{book_name}-{chapter}.txt"
        output_path = os.path.join(output_dir, output_filename)

        if incremental and os.path.exists(output_path):
            output_mod_time = datetime.fromtimestamp(os.path.getmtime(output_path))
            latest_image_time = get_latest_image_timestamp(chapter_path)
            
            if latest_image_time and output_mod_time > latest_image_time:
                print(f"Skipping {chapter} - no new images")
                continue

        output_text = process_chapter(chapter_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)

def main():
    parser = argparse.ArgumentParser(description="OCR script for processing book chapters")
    parser.add_argument("input_dir", help="Input directory containing chapter subdirectories with PNG images")
    parser.add_argument("output_dir", help="Output directory for text files")
    parser.add_argument("--no-incremental", action="store_false", dest="incremental",
                        help="Disable incremental processing (process all chapters regardless of existing output)")
    parser.set_defaults(incremental=True)
    args = parser.parse_args()

    setup_logging()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    process_book(args.input_dir, args.output_dir, args.incremental)

if __name__ == "__main__":
    main()