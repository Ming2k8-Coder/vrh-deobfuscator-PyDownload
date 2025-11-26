import os
import re
from typing import Optional, Tuple
# Note: sqlite3 and time are no longer needed, so they are removed.

# --- Configuration ---
# Set the root directory you want to scan.
# For absolute Windows paths like E:\Master_Project\!3D_prjext\VRM, 
# use forward slashes or escaped backslashes in Python string:
SCAN_ROOT_DIR = 'E:/Master_Project/!3D_prjext/VRM'
#SCAN_ROOT_DIR = 'target_files'
# New output file name
OUTPUT_FILE_NAME = 'extracted_ids.txt'

# NEW: List of folder names (not paths) to completely ignore during the scan.
# Any directory name matching one of these will be skipped, including all its contents.
EXCLUDE_FOLDERS = ['My project','ignored_cache', 'temp_files', 'SubDirB']

# Regex pattern to match and capture the ID enclosed in brackets at the start of the filename.
# ^\[(\d+)\].*
ID_PATTERN = re.compile(r'^\[(\d+)\].*')

# The database setup functions have been removed.

def extract_id(filename: str) -> Optional[str]:
    """Extracts the numeric ID from the filename based on the defined regex pattern."""
    match = ID_PATTERN.match(filename)
    if match:
        # group(1) returns the content of the first capture group, which is the ID
        return match.group(1)
    return None

def save_to_file(extracted_id: str, full_path: str):
    """Appends the extracted ID and full path to the plain text file in a machine-readable TSV format."""
    # The format is now: ID \t FULL_PATH (Tab-Separated Values)
    output_line = f"{extracted_id}\t{full_path}\n"
    
    try:
        # 'a' mode appends to the file, creating it if it doesn't exist.
        with open(OUTPUT_FILE_NAME, 'a', encoding='utf-8') as f:
            f.write(output_line)
        print(f"    [SAVED] ID: {extracted_id}, Path: {full_path}")
    except Exception as e:
        print(f"    [ERROR] Could not save {full_path}: {e}")

def create_dummy_files(root_dir: str):
    """Creates a sample directory structure for testing purposes."""
    print(f"Creating dummy files in: {root_dir}")
    os.makedirs(os.path.join(root_dir, 'SubDirA'), exist_ok=True)
    os.makedirs(os.path.join(root_dir, 'SubDirB', 'Nested'), exist_ok=True) # This directory will be excluded
    os.makedirs(os.path.join(root_dir, 'temp_files'), exist_ok=True) # This directory will be excluded

    # Files that match the pattern
    matching_files = [
        '[4940686603855165070].DEMON QUEEN SKELETON GOTH GIRL_--Nero Studios.deobf.vrm', # In root
        '[1234567890123456789].Another File Title.obj', # In SubDirA
        '[987654321].SimpleTest.txt', # In SubDirB/Nested (should be excluded)
        '[555555555].TempFile.dat', # In temp_files (should be excluded)
    ]

    # Files that do NOT match the pattern
    non_matching_files = [
        'NoID_File.vrm',
        '[[1234]]DoubleBracket.zip',
        'SomeFile[555].rar',
    ]

    # Place files in different directories
    with open(os.path.join(root_dir, matching_files[0]), 'w') as f: f.write("dummy")
    with open(os.path.join(root_dir, 'SubDirA', matching_files[1]), 'w') as f: f.write("dummy")
    with open(os.path.join(root_dir, 'SubDirB', 'Nested', matching_files[2]), 'w') as f: f.write("dummy") # Excluded
    with open(os.path.join(root_dir, 'temp_files', matching_files[3]), 'w') as f: f.write("dummy") # Excluded

    with open(os.path.join(root_dir, non_matching_files[0]), 'w') as f: f.write("dummy")

    print("Dummy files created successfully for testing.\n")


def scan_and_save(start_dir: str):
    """
    Recursively scans the specified directory, extracts IDs, and saves them to the text file,
    while excluding specified folders.
    """
    print(f"--- Starting scan of directory: {start_dir} ---")
    file_count = 0
    id_count = 0

    # os.walk iterates through the directory structure recursively
    for root, dirnames, files in os.walk(start_dir):
        # 1. Exclusion Logic: Check if the current directory ('root') path contains any excluded folder names
        
        # Normalize the path for consistent splitting (important for Windows drive letters)
        normalized_root = os.path.normpath(root)
        
        # Split the path into parts using the OS-specific separator
        # This handles absolute paths like C:\... or E:\... correctly.
        root_parts = normalized_root.split(os.sep)
        
        # Filter out empty strings that result from splitting (e.g., C:\ split might give ['', '']
        # and ignore the drive letter if it's the first element)
        folder_names = [part for part in root_parts if part and ':' not in part]
        
        should_skip_root = False
        for part in folder_names:
            if part in EXCLUDE_FOLDERS:
                should_skip_root = True
                break
        
        if should_skip_root and root != start_dir:
            print(f"--- FOLDER EXCLUDED: {root} (Skipping contents)")
            # Prevent os.walk from descending into subdirectories of 'root'.
            dirnames[:] = [] 
            continue # Skip processing files in this excluded root

        # 2. File Processing Logic (only runs if the folder is NOT excluded)
        for filename in files:
            file_count += 1
            extracted_id = extract_id(filename)

            if extracted_id:
                # Construct the full path
                full_path = os.path.join(root, filename)
                save_to_file(extracted_id, full_path)
                id_count += 1
            else:
                pass # Skip non-matching files

    print(f"\n--- Scan Complete ---")
    print(f"Total files checked: {file_count}")
    print(f"IDs extracted and saved: {id_count}")


if __name__ == '__main__':
    # 1. Setup the dummy files for testing
    #create_dummy_files(SCAN_ROOT_DIR)

    # Clear the file before starting a new scan to ensure a fresh run
    if os.path.exists(OUTPUT_FILE_NAME):
        os.remove(OUTPUT_FILE_NAME)
        print(f"Cleared previous run's data from '{OUTPUT_FILE_NAME}'.")
    
    # 2. Perform the scan and save operation
    scan_and_save(SCAN_ROOT_DIR)

    # 3. Final message
    print(f"\nAll results have been saved to the plain text file: {OUTPUT_FILE_NAME}")

    # OPTIONAL: Cleanup dummy files
    #import shutil
    # if os.path.exists(SCAN_ROOT_DIR):
    #     print(f"Cleaning up dummy directory: {SCAN_ROOT_DIR}")
    #     shutil.rmtree(SCAN_ROOT_DIR)
