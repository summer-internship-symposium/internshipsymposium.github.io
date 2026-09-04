# PDF to PNG Converter

A Python script that converts PDF files to PNG images with automatic size optimization to ensure output files are no more than 1MB each. Also includes functionality to compress existing PNG files.

## Features

- ✅ Convert single or multiple PDF files to PNG format
- ✅ Compress existing PNG files to meet size limits
- ✅ Automatic size optimization (compression and scaling) to meet file size limits
- ✅ Batch processing - convert entire directories of PDFs or compress PNGs
- ✅ Multi-page PDF support
- ✅ Customizable DPI and maximum file size
- ✅ All output files saved to a single directory (no subdirectories)
- ✅ Optional backup creation for PNG compression

## Requirements

- Python 3.7 or higher
- System dependencies for pdf2image:
  - **macOS**: `brew install poppler`
  - **Linux**: `apt-get install poppler-utils` (Ubuntu/Debian) or `yum install poppler-utils` (RHEL/CentOS)
  - **Windows**: Download poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/)

## Installation

1. **Install system dependencies** (see Requirements above)

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pdf2image Pillow
   ```

3. **Make the script executable** (optional, on macOS/Linux):
   ```bash
   chmod +x pdf_to_png.py
   ```

## Usage

### Basic Usage

Convert a single PDF file:
```bash
python3 pdf_to_png.py document.pdf
```

This will create PNG file(s) in the same directory as the PDF.

### Specify Output Directory

```bash
python3 pdf_to_png.py document.pdf ./output
```

### Batch Convert All PDFs in a Directory

```bash
python3 pdf_to_png.py ./pdfs_folder ./output
```

This will process all PDF files in `pdfs_folder` and save all PNG files directly in `./output` (no subdirectories).

### Customize DPI and Maximum File Size

```bash
python3 pdf_to_png.py document.pdf ./output 300 0.5
```

- `300` = DPI (higher = better quality but larger file)
- `0.5` = Maximum file size in MB (0.5 MB = 500 KB)

### Command-Line Arguments

```
python3 pdf_to_png.py <pdf_file_or_directory> [output_directory] [dpi] [max_size_mb]
```

| Argument | Description | Default |
|----------|-------------|---------|
| `pdf_file_or_directory` | Path to a PDF file or directory containing PDFs | Required |
| `output_directory` | Directory to save PNG files | Same as PDF location |
| `dpi` | Resolution for conversion (higher = better quality) | 200 |
| `max_size_mb` | Maximum file size in MB | 1.0 |

## How It Works

1. **PDF Conversion**: The script uses `pdf2image` to render PDF pages as high-resolution images
2. **Size Optimization**: If the PNG exceeds the size limit, the script automatically:
   - First tries PNG optimization
   - Then reduces quality through JPEG compression
   - Finally scales down dimensions if needed
3. **Output**: Saves the optimized PNG file(s) with size ≤ 1MB (or your specified limit)

## Examples

### Convert a presentation with high quality
```bash
python3 pdf_to_png.py presentation.pdf ./images 300 1.0
```

### Create small thumbnails
```bash
python3 pdf_to_png.py document.pdf ./thumbnails 150 0.3
```

### Batch convert all PDFs in a folder
```bash
python3 pdf_to_png.py ./reports ./converted_images
```

### Compress Existing PNG Files

Compress all PNG files in a directory to meet size limit:
```bash
python3 pdf_to_png.py --compress-png ./images
```

Compress with custom size limit (0.5MB):
```bash
python3 pdf_to_png.py --compress-png ./images 0.5
```

Compress with backup of original files:
```bash
python3 pdf_to_png.py --compress-png ./images 1.0 --backup
```

## Output Structure

### Single PDF (1 page)
```
output/
  └── document.png
```

### Single PDF (multiple pages)
```
output/
  ├── document_page_1.png
  ├── document_page_2.png
  └── document_page_3.png
```

### Multiple PDFs (batch processing)
All files saved in the same directory:
```
output/
  ├── document1_page_1.png
  ├── document1_page_2.png
  ├── document2.png
  ├── report_page_1.png
  └── report_page_2.png
```

## Troubleshooting

### "pdf2image is required for PDF conversion"
Install pdf2image and poppler:
- `pip install pdf2image`
- Install poppler using the instructions in the Requirements section

### "No PDF files found"
Check that:
- The file path is correct
- The file has a `.pdf` extension
- You have read permissions for the file

### "Could not reduce file size below X MB"
The script tried its best but couldn't meet the size limit. Try:
- Reducing the DPI (e.g., use 150 instead of 200)
- Increasing the max_size_mb limit
- The PDF might have very complex graphics that don't compress well

### High quality loss
Try:
- Increasing the DPI (e.g., 300 or higher)
- Increasing the max_size_mb limit (e.g., 2.0 for 2MB)

## Notes

- The script automatically handles multi-page PDFs
- For batch processing, all PNG files are saved to the same output directory
- Images use LANCZOS resampling for high-quality scaling
- Transparency is preserved when possible, or converted to white background
- Temporary files are cleaned up automatically

## License

This script is provided as-is for the internshipsymposium.github.io project.
