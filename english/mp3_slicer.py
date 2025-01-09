import os
from pydub import AudioSegment, silence
import librosa
import numpy as np

# Function to calculate the similarity between two audio files
def calculate_similarity(sample_path, target_path):
    # Load the audio files
    sample_audio, sample_sr = librosa.load(sample_path, sr=None)
    target_audio, target_sr = librosa.load(target_path, sr=None)
    
    # Resample to the same sample rate if needed
    if sample_sr != target_sr:
        target_audio = librosa.resample(target_audio, orig_sr=target_sr, target_sr=sample_sr)
    
    # Pad or trim to match the length of the sample audio
    min_length = min(len(sample_audio), len(target_audio))
    sample_audio = sample_audio[:min_length]
    target_audio = target_audio[:min_length]
    
    # Calculate normalized cross-correlation as a similarity measure
    similarity = np.corrcoef(sample_audio, target_audio)[0, 1]
    return similarity

# Load the uploaded audio file
audio_path = "basic_day1.mp3"
audio = AudioSegment.from_file(audio_path, format="mp3")

# Extract the base name of the audio file without extension
base_name = os.path.splitext(os.path.basename(audio_path))[0]

# Detect silence (longer than 2 seconds, -40 dBFS is considered silence)
silent_chunks = silence.detect_silence(audio, min_silence_len=900, silence_thresh=-40)

# Adjust start and end times for easier splitting
silent_chunks = [(start, end) for start, end in silent_chunks]

directory = "."
intro_file = "_intro.mp3"  # Path to the sample MP3 file
bell_file = "_bell.mp3"  # Path to the sample MP3 file
model_file = "_model.mp3"
small_first_file = "_small1.mp3"
small_second_file = "_small2.mp3"

similarity_threshold = 0.95  # Adjust threshold based on experiments

# Split audio based on silent chunks
output_files = []
for i, (start, end) in enumerate(zip([0] + [end for _, end in silent_chunks], [start for start, _ in silent_chunks] + [len(audio)])):
    segment = audio[start:end]
    output_path = f"{base_name}_{i+1}.mp3"
    segment.export(output_path, format="mp3")

    # Check the file size and delete if it's smaller than 11,000 bytes
    if os.path.getsize(output_path) <= 11000: 
        os.remove(output_path)
        print(f"Deleted file because it is too short: {output_path} ")
    else:
        output_files.append(output_path)


output_files

for file in os.listdir(directory):
    if file.endswith(".mp3") and file != intro_file and file != bell_file and file != model_file and file != small_first_file and file != small_second_file:  # Exclude the sample file
        file_path = os.path.join(directory, file)
        intro = calculate_similarity(intro_file, file_path)
        bell = calculate_similarity(bell_file, file_path)
        model = calculate_similarity(model_file, file_path)
        small_first = calculate_similarity(small_first_file, file_path)
        small_second = calculate_similarity(small_second_file, file_path)
        
        if intro >= similarity_threshold:
            os.remove(file_path)
            print(f"Deleted similar file: {file} (intro music: {intro:.2f})")
        elif bell >= similarity_threshold:
            os.remove(file_path)
            print(f"Deleted similar file: {file} (bell sounds: {bell:.2f})")
        elif model >= similarity_threshold:
            os.remove(file_path)
            print(f"Deleted similar file: {file} (Model sounds: {model:.2f})")
        elif small_first >= similarity_threshold:
            os.remove(file_path)
            print(f"Deleted similar file: {file} (Small 1 sounds: {small_first:.2f})")
        elif small_second >= similarity_threshold:
            os.remove(file_path)
            print(f"Deleted similar file: {file} (Small 2 sounds: {small_second:.2f})")
        else:
            print(f"Kept: {file} (intro music: {intro:.2f}) (bell sounds: {bell:.2f}) (Model sounds: {model:.2f}) (Small 1 sounds: {small_first:.2f}) (Small 2 sounds: {small_second:.2f})")
