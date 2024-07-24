# OCR Book Processing Script

This Python script is designed to perform Optical Character Recognition (OCR) on a directory of book screenshots, organized by chapters. It's particularly useful for digitizing physical books or processing e-books into searchable text format.

## Features

- Processes an entire book directory, with each subdirectory treated as a chapter
- Generates text files for each chapter, named after the book and chapter
- Supports incremental processing to avoid unnecessary reprocessing of unchanged chapters
- Utilizes parallel processing for efficient OCR of images within each chapter
- Maintains the order of pages based on screenshot timestamps
- Provides progress bars for both chapter and image processing

## Requirements

- Python 3.6+
- Tesseract OCR engine
- Python libraries: PIL (Pillow), pytesseract, tqdm

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Install Tesseract OCR on your system. Installation instructions can be found [here](https://github.com/tesseract-ocr/tesseract).
3. Install the required Python libraries:

   ```
   pip install Pillow pytesseract tqdm
   ```

## Usage

Basic usage:

```
python ocr_script.py /path/to/book_directory /path/to/output_directory
```

To disable incremental processing and force processing of all chapters:

```
python ocr_script.py /path/to/book_directory /path/to/output_directory --no-incremental
```

### Directory Structure

The script expects the following directory structure:

```
book_directory/
├── chapter1/
│   ├── page1.png
│   ├── page2.png
│   └── ...
├── chapter2/
│   ├── page1.png
│   ├── page2.png
│   └── ...
└── ...
```

### Output

The script will generate text files in the specified output directory, named as follows:

```
output_directory/
├── book_name-chapter1.txt
├── book_name-chapter2.txt
└── ...
```

Where `book_name` is the name of the input book directory.

## Incremental Processing

By default, the script uses incremental processing. It compares the timestamp of the output text file for each chapter with the latest screenshot in that chapter's directory. If the output file is more recent, the chapter is skipped. This feature can be disabled using the `--no-incremental` flag.

## Error Handling

Errors during OCR processing are logged to `ocr_errors.log` in the same directory as the script.

## Notes

- The script assumes that screenshot filenames contain timestamps in the format `YYYY-MM-DD-HH_MM_SS`.
- For best results, ensure that your screenshots are clear and high-quality.
- Large books with many high-resolution images may take significant time to process.

## Contributing

Feel free to fork this project and submit pull requests with any enhancements.

## License

This project is open-source and available under the MIT License.