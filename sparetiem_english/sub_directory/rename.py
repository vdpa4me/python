import os
import re
import csv

def rename_mp3_files(directory):
    # Regular expression to match files in the format: basic_day3_X.mp3
    pattern = re.compile(r"(basic_day\d+)_(\d+)\.mp3")

    # List to store matched files with their base names and numbers
    files = []

    # Iterate through files in the directory
    for file in os.listdir(directory):
        match = pattern.match(file)
        if match:
            base_name, number = match.groups()  # Capture the base name and number
            files.append((file, base_name, int(number)))

    # Sort files by the numeric part of the name
    files.sort(key=lambda x: x[2])

    # Step 1: Rename files to temporary names to avoid conflicts
    temp_files = []
    for index, (original_name, base_name, _) in enumerate(files, start=1):
        temp_name = f"{base_name}_temp{index}.mp3"
        original_path = os.path.join(directory, original_name)
        temp_path = os.path.join(directory, temp_name)
        os.rename(original_path, temp_path)
        temp_files.append((temp_name, base_name, index))
        print(f"Temporarily renamed: {original_name} -> {temp_name}")

    # Step 2: Rename files to final names
    final_files = []
    for temp_name, base_name, index in temp_files:
        final_name = f"{base_name}_{index}.mp3"
        temp_path = os.path.join(directory, temp_name)
        final_path = os.path.join(directory, final_name)
        os.rename(temp_path, final_path)
        final_files.append((base_name, index, final_name))
        print(f"Renamed: {temp_name} -> {final_name}")

    # Step 3: Create CSV file
    if final_files:
        # Extract "day3" from the base name
        csv_base = final_files[0][0].split('_')[1]  # Extract "day3"
        csv_filename = os.path.join(directory, f"{csv_base}.csv")

        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            for i in range(0, len(final_files) - 1, 2):
                row = [
                    "basic", 1, 1, 1, "한글", "영어", 
                    final_files[i][2],  # First file in the pair
                    final_files[i + 1][2] if i + 1 < len(final_files) else ""  # Second file in the pair or empty
                ]
                csvwriter.writerow(row)

        print(f"CSV file created: {csv_filename}")

# Example usage
directory = "."  # Replace with the path to your folder
rename_mp3_files(directory)
