#!/usr/bin/env python3
"""
PDF to PNG Converter with Size Limit
Converts PDF files to PNG format ensuring output is no more than 1MB
"""

import os
import sys
from pathlib import Path
from PIL import Image
import io

def get_file_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def optimize_png_size(image, output_path, max_size_mb=1.0, initial_quality=95):
    """
    Optimize PNG size by adjusting quality and dimensions
    
    Args:
        image: PIL Image object
        output_path: Path to save the optimized PNG
        max_size_mb: Maximum file size in MB (default: 1.0)
        initial_quality: Starting quality for compression (default: 95)
    """
    quality = initial_quality
    scale = 1.0
    temp_path = output_path + ".tmp"
    
    while True:
        # Resize image if scale < 1.0
        if scale < 1.0:
            new_width = int(image.width * scale)
            new_height = int(image.height * scale)
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            resized_image = image
        
        # Save with current settings
        if quality >= 60:
            # Use PNG with optimization
            resized_image.save(temp_path, "PNG", optimize=True)
        else:
            # Convert to RGB if needed and save as compressed PNG
            if resized_image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                rgb_image = Image.new('RGB', resized_image.size, (255, 255, 255))
                if resized_image.mode == 'P':
                    resized_image = resized_image.convert('RGBA')
                rgb_image.paste(resized_image, mask=resized_image.split()[-1] if resized_image.mode in ('RGBA', 'LA') else None)
                resized_image = rgb_image
            
            # Save as JPEG for better compression, then convert back to PNG
            buffer = io.BytesIO()
            resized_image.save(buffer, "JPEG", quality=quality, optimize=True)
            buffer.seek(0)
            compressed = Image.open(buffer)
            compressed.save(temp_path, "PNG", optimize=True)
        
        # Check file size
        file_size_mb = get_file_size_mb(temp_path)
        
        if file_size_mb <= max_size_mb:
            # Success! Move temp file to final destination
            os.rename(temp_path, output_path)
            return file_size_mb, quality, scale
        
        # File too large, adjust parameters
        if quality > 60:
            quality -= 5
        elif scale > 0.5:
            scale -= 0.05
        else:
            # Aggressive reduction needed
            quality -= 10
            scale -= 0.1
            
        if quality < 20 or scale < 0.2:
            # Can't compress further, save what we have
            os.rename(temp_path, output_path)
            print(f"Warning: Could not reduce file size below {file_size_mb:.2f}MB")
            return file_size_mb, quality, scale

def convert_pdf_to_png(pdf_path, output_dir=None, dpi=80, max_size_mb=1.0):
    """
    Convert PDF to PNG files with size limit
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Output directory (default: same as PDF location)
        dpi: DPI for conversion (default: 80)
        max_size_mb: Maximum file size in MB (default: 1.0)
    """
    # Import pdf2image only when needed for PDF conversion
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Error: pdf2image is required for PDF conversion")
        print("Install with: pip install pdf2image")
        print("Also requires poppler - see README for installation instructions")
        return False
    
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {pdf_path.name}")
    print(f"Output directory: {output_dir}")
    
    try:
        # Convert PDF to images
        print(f"Converting PDF pages at {dpi} DPI...")
        images = convert_from_path(str(pdf_path), dpi=dpi)
        
        print(f"Found {len(images)} page(s)")
        
        # Process each page
        for i, image in enumerate(images, 1):
            # Generate output filename
            base_name = pdf_path.stem
            if len(images) > 1:
                output_path = output_dir / f"{base_name}_page_{i}.png"
            else:
                output_path = output_dir / f"{base_name}.png"
            
            print(f"\nProcessing page {i}/{len(images)}...")
            print(f"  Original dimensions: {image.width}x{image.height}")
            
            # Optimize and save
            file_size, quality, scale = optimize_png_size(
                image, 
                str(output_path), 
                max_size_mb=max_size_mb
            )
            
            print(f"  Saved: {output_path.name}")
            print(f"  Final size: {file_size:.2f}MB")
            if scale < 1.0:
                print(f"  Scaled to: {int(image.width * scale)}x{int(image.height * scale)}")
            if quality < 95:
                print(f"  Compression quality: {quality}")
        
        print(f"\n✓ Conversion complete!")
        return True
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def find_pdf_files(path):
    """
    Find all PDF files in a given path (file or directory)
    
    Args:
        path: Path to a PDF file or directory
        
    Returns:
        List of Path objects for PDF files
    """
    path = Path(path)
    
    if path.is_file():
        if path.suffix.lower() == '.pdf':
            return [path]
        else:
            print(f"Warning: {path} is not a PDF file")
            return []
    elif path.is_dir():
        # Find all PDF files in directory (non-recursive)
        pdf_files = list(path.glob('*.pdf')) + list(path.glob('*.PDF'))
        return sorted(pdf_files)
    else:
        print(f"Error: Path not found: {path}")
        return []

def find_png_files(path):
    """
    Find all PNG files in a given path (file or directory)
    
    Args:
        path: Path to a PNG file or directory
        
    Returns:
        List of Path objects for PNG files
    """
    path = Path(path)
    
    if path.is_file():
        if path.suffix.lower() == '.png':
            return [path]
        else:
            print(f"Warning: {path} is not a PNG file")
            return []
    elif path.is_dir():
        # Find all PNG files in directory (non-recursive)
        png_files = list(path.glob('*.png')) + list(path.glob('*.PNG'))
        return sorted(png_files)
    else:
        print(f"Error: Path not found: {path}")
        return []

def compress_existing_png(png_path, max_size_mb=1.0, backup=False):
    """
    Compress an existing PNG file if it exceeds the size limit
    Reuses optimize_png_size for compression logic
    
    Args:
        png_path: Path to the PNG file
        max_size_mb: Maximum file size in MB (default: 1.0)
        backup: If True, create a backup of the original file
        
    Returns:
        Tuple of (success, original_size_mb, final_size_mb, quality, scale)
    """
    png_path = Path(png_path)
    
    if not png_path.exists():
        print(f"Error: PNG file not found: {png_path}")
        return False, 0, 0, 0, 0
    
    # Check current file size
    original_size_mb = get_file_size_mb(png_path)
    
    if original_size_mb <= max_size_mb:
        return True, original_size_mb, original_size_mb, 95, 1.0
    
    try:
        # Create backup if requested
        if backup:
            backup_path = png_path.with_suffix('.png.backup')
            import shutil
            shutil.copy2(png_path, backup_path)
            print(f"    Backup created: {backup_path.name}")
        
        # Load the image
        image = Image.open(png_path)
        
        # Reuse optimize_png_size function
        final_size_mb, quality, scale = optimize_png_size(
            image, 
            str(png_path), 
            max_size_mb=max_size_mb
        )
        
        image.close()
        return True, original_size_mb, final_size_mb, quality, scale
        
    except Exception as e:
        print(f"    Error compressing: {e}")
        return False, original_size_mb, 0, 0, 0

def compress_png_directory(directory_path, max_size_mb=1.0, backup=False):
    """
    Find and compress all oversized PNG files in a directory
    
    Args:
        directory_path: Path to directory containing PNG files
        max_size_mb: Maximum file size in MB
        backup: If True, create backups of original files
        
    Returns:
        Tuple of (compressed_count, skipped_count, failed_count)
    """
    png_files = find_png_files(directory_path)
    
    if not png_files:
        print("No PNG files found in directory")
        return 0, 0, 0
    
    print(f"Found {len(png_files)} PNG file(s) to check")
    print("=" * 60)
    
    compressed = 0
    skipped = 0
    failed = 0
    
    for png_path in png_files:
        current_size_mb = get_file_size_mb(png_path)
        
        if current_size_mb <= max_size_mb:
            skipped += 1
            print(f"  {png_path.name}: {current_size_mb:.2f}MB - Already under limit ✓")
        else:
            print(f"  {png_path.name}: {current_size_mb:.2f}MB - Compressing...")
            success, orig_size, final_size, quality, scale = compress_existing_png(
                png_path, 
                max_size_mb=max_size_mb, 
                backup=backup
            )
            
            if success:
                compressed += 1
                reduction_percent = ((orig_size - final_size) / orig_size) * 100
                print(f"    Compressed to {final_size:.2f}MB ({reduction_percent:.1f}% reduction) ✓")
                if scale < 1.0:
                    image = Image.open(png_path)
                    print(f"    Dimensions: {image.width}x{image.height}")
                    image.close()
                if quality < 95:
                    print(f"    Quality: {quality}")
            else:
                failed += 1
    
    print("\n" + "=" * 60)
    print(f"PNG compression complete!")
    print(f"  Compressed: {compressed}")
    print(f"  Already under limit: {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(png_files)}")
    
    return compressed, skipped, failed

def batch_convert_pdfs(pdf_paths, output_dir=None, dpi=80, max_size_mb=1.0):
    """
    Convert multiple PDF files to PNG format
    
    Args:
        pdf_paths: List of paths to PDF files or directories
        output_dir: Output directory for all PNG files
        dpi: DPI for conversion
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (successful_count, failed_count)
    """
    # Collect all PDF files
    all_pdfs = []
    for path_str in pdf_paths:
        pdfs = find_pdf_files(path_str)
        all_pdfs.extend(pdfs)
    
    if not all_pdfs:
        print("No PDF files found to convert")
        return 0, 0
    
    print(f"Found {len(all_pdfs)} PDF file(s) to convert")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for idx, pdf_path in enumerate(all_pdfs, 1):
        print(f"\n[{idx}/{len(all_pdfs)}] Processing: {pdf_path.name}")
        print("-" * 60)
        
        # Determine output directory for this PDF
        if output_dir:
            pdf_output_dir = Path(output_dir)
        else:
            # Use same directory as source PDF
            pdf_output_dir = pdf_path.parent
        
        # Convert the PDF
        success = convert_pdf_to_png(
            str(pdf_path), 
            str(pdf_output_dir), 
            dpi=dpi, 
            max_size_mb=max_size_mb
        )
        
        if success:
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Batch conversion complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(all_pdfs)}")
    
    return successful, failed

def main():
    """Main entry point for the script"""
    if len(sys.argv) < 2:
        print("PDF to PNG Converter with Size Limit")
        print("\nUsage:")
        print(f"  {sys.argv[0]} <path> [options...]")
        print("\nModes:")
        print("  PDF Conversion Mode (default):")
        print(f"    {sys.argv[0]} <pdf_file_or_directory> [output_directory] [dpi] [max_size_mb]")
        print("\n  PNG Compression Mode:")
        print(f"    {sys.argv[0]} --compress-png <png_file_or_directory> [max_size_mb] [--backup]")
        print("\nArguments:")
        print("  pdf_file_or_directory    : Path to PDF file or directory containing PDFs")
        print("  png_file_or_directory    : Path to PNG file or directory containing PNGs")
        print("  output_directory         : (Optional) Output directory for PNG files")
        print("  dpi                      : (Optional) DPI for PDF conversion (default: 80)")
        print("  max_size_mb              : (Optional) Maximum file size in MB (default: 1.0)")
        print("  --backup                 : (Optional) Create backup of original PNG files")
        print("\nExamples:")
        print("  PDF Conversion:")
        print(f"    {sys.argv[0]} document.pdf")
        print(f"    {sys.argv[0]} document.pdf ./output")
        print(f"    {sys.argv[0]} ./pdfs_folder ./output 300 0.5")
        print("\n  PNG Compression:")
        print(f"    {sys.argv[0]} --compress-png ./images")
        print(f"    {sys.argv[0]} --compress-png ./images 0.5")
        print(f"    {sys.argv[0]} --compress-png ./images 1.0 --backup")
        sys.exit(1)
    
    # Check if we're in PNG compression mode
    if sys.argv[1] == '--compress-png':
        if len(sys.argv) < 3:
            print("Error: --compress-png requires a path to PNG file(s) or directory")
            sys.exit(1)
        
        png_path = sys.argv[2]
        max_size_mb = 1.0
        backup = False
        
        # Parse optional arguments for PNG compression
        for i in range(3, len(sys.argv)):
            arg = sys.argv[i]
            if arg == '--backup':
                backup = True
            else:
                try:
                    max_size_mb = float(arg)
                except ValueError:
                    print(f"Warning: Ignoring invalid argument: {arg}")
        
        print(f"PNG Compression Mode")
        print(f"Max size limit: {max_size_mb}MB")
        print(f"Backup enabled: {backup}")
        print()
        
        # Compress PNG files
        compressed, skipped, failed = compress_png_directory(
            png_path,
            max_size_mb=max_size_mb,
            backup=backup
        )
        
        sys.exit(0 if failed == 0 else 1)
    
    # PDF Conversion Mode (default)
    input_paths = [sys.argv[1]]
    
    # Parse optional arguments
    output_dir = None
    dpi = 80
    max_size_mb = 1.0
    
    if len(sys.argv) > 2:
        # Check if second argument is an existing directory or looks like an output path
        second_arg = sys.argv[2]
        if not second_arg.isdigit() and not second_arg.replace('.', '').isdigit():
            output_dir = second_arg
            if len(sys.argv) > 3:
                dpi = int(sys.argv[3])
            if len(sys.argv) > 4:
                max_size_mb = float(sys.argv[4])
        else:
            # Second argument is DPI
            dpi = int(second_arg)
            if len(sys.argv) > 3:
                max_size_mb = float(sys.argv[3])
    
    # Check if we're doing batch processing
    pdf_files = find_pdf_files(input_paths[0])
    
    if len(pdf_files) == 1:
        # Single PDF conversion
        success = convert_pdf_to_png(
            str(pdf_files[0]), 
            output_dir, 
            dpi=dpi, 
            max_size_mb=max_size_mb
        )
        sys.exit(0 if success else 1)
    else:
        # Batch conversion
        successful, failed = batch_convert_pdfs(
            input_paths, 
            output_dir=output_dir, 
            dpi=dpi, 
            max_size_mb=max_size_mb
        )
        sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
