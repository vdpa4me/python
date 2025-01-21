from pydub import AudioSegment
import sys

def merge_mp3(file1, file2, output_file=None):
    # Load MP3 files
    audio1 = AudioSegment.from_mp3(file1)
    audio2 = AudioSegment.from_mp3(file2)
    
    # Concatenate the audio files
    combined = audio1 + audio2

    # If no output file is specified, generate it based on the first file
    if output_file is None:
        base_name = file1.rsplit(".", 1)[0]  # Remove the file extension
        output_file = f"m{base_name}.mp3"

    # Export the combined audio to a new MP3 file
    combined.export(output_file, format="mp3")
    print(f"Files merged successfully into: {output_file}")


if len(sys.argv) > 2:
    print(f"1st : {sys.argv[1]}")
    print(f"2nd : {sys.argv[2]}")
    file1 = sys.argv[1]
    file2 = sys.argv[2]
else:
    print("ERROR:NO files")
    exit(2)

merge_mp3(file1, file2)