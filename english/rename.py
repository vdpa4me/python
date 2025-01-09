import os
import re

def rename_mp3_files(directory):
    # Regular expression to match files in the format: basic_day1_[Number].mp3
    pattern = re.compile(r"(basic_day1)_(\d+)\.mp3")

    # List to store tuples of (original_name, number)
    files = []

    # Iterate through files in the directory
    for file in os.listdir(directory):
        match = pattern.match(file)
        if match:
            base_name, number = match.groups()
            files.append((file, int(number)))

    # Sort files by the numeric part of the name
    files.sort(key=lambda x: x[1])

    # Rename files to have sequential numbers starting from 1
    for index, (original_name, _) in enumerate(files, start=1):
        new_name = f"basic_day1_{index}.mp3"
        original_path = os.path.join(directory, original_name)
        new_path = os.path.join(directory, new_name)
        os.rename(original_path, new_path)
        print(f"Renamed: {original_name} -> {new_name}")

# Example usage
directory = "."  # Replace with the path to your folder
rename_mp3_files(directory)
