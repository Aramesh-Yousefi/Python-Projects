import os
import hashlib
import shutil
import zipfile
from cryptography.fernet import Fernet

def calculate_hash(file_path):
    # Calculate SHA256 hash of the file
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # 64 KB buffer
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def find_duplicate_files(folder):
    # Dictionary to store file hashes
    file_hashes = {}
    duplicates = []

    # Traverse through all files in the folder and its subfolders
    for root, _, files in os.walk(folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = calculate_hash(file_path)
            if file_hash in file_hashes:
                duplicates.append((file_path, file_hashes[file_hash]))
            else:
                file_hashes[file_hash] = file_path
    return duplicates

def move_duplicates_to_folder(duplicates, destination_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Move duplicate files to the destination folder
    for original_file, duplicate_file in duplicates:
        shutil.move(duplicate_file, destination_folder)

def compress_folder(folder, output_zip):
    # Create a zip file containing the folder contents
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder))

def encrypt_file(file_path, key):
    # Read file contents
    with open(file_path, 'rb') as f:
        data = f.read()

    # Encrypt file contents
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    # Write encrypted data back to the file
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

# Main function
if __name__ == "__main__":
    # Get the path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define folder paths and filenames
    folder_to_scan = current_dir  # Use the current directory
    destination_folder = os.path.join(current_dir, 'duplicates_folder')
    output_zip = os.path.join(current_dir, 'compressed_folder.zip')

    # Generate a Fernet key
    encryption_key = Fernet.generate_key()

    # Find duplicate files
    duplicates = find_duplicate_files(folder_to_scan)

    if duplicates:
        # Move duplicate files to a separate folder
        move_duplicates_to_folder(duplicates, destination_folder)

        # Compress the folder containing duplicate files
        compress_folder(destination_folder, output_zip)

        # Encrypt the compressed file
        encrypt_file(output_zip, encryption_key)
        
        print("Duplicate files identified, moved to a folder, compressed, and encrypted successfully.")
    else:
        print("No duplicate files found.")
