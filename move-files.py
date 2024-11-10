import os
import sys
import shutil

# Move a specific file extension between folders

def copy_mp3_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        print(f"Destination directory {dest_dir} does not exist")
        sys.exit(1)

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(extension):
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_dir, file)
                shutil.copy2(src_file_path, dest_file_path)
                print(f"Copied {src_file_path} to {dest_file_path}")


if __name__ == "__main__":
    src_directory = "D:\\UpdateMusic\\downloadedDemistify\\demistify"
    dest_directory = "D:\\UpdateMusic\\Lyrics"
    extension = ".lrc"
    copy_mp3_files(src_directory, dest_directory, extension)
