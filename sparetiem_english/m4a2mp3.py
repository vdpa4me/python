import os
from pydub import AudioSegment

# 현재 스크립트가 있는 디렉토리
current_dir = os.path.dirname(os.path.abspath(__file__))

# 모든 M4A 파일을 찾아 MP3로 변환
for filename in os.listdir(current_dir):
    if filename.endswith(".m4a"):  # 확장자가 .m4a인 파일만 처리
        m4a_path = os.path.join(current_dir, filename)
        mp3_path = os.path.join(current_dir, filename.replace(".m4a", ".mp3"))

        print(f"변환 중: {filename} -> {os.path.basename(mp3_path)}")

        # 변환 실행
        audio = AudioSegment.from_file(m4a_path, format="m4a")
        audio.export(mp3_path, format="mp3", bitrate="192k")