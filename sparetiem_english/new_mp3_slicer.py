import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import time
import numpy as np
import librosa
from spleeter.separator import Separator
from parselmouth import Sound
from pydub import AudioSegment

class MP3SplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 분리기 - 남자/여자 음성 분리")

        # 메인 레이블
        self.label = tk.Label(root, text="MP3 파일을 선택하세요!", font=("Arial", 14, "bold"))
        self.label.pack(pady=10)

        # MP3 선택 버튼
        self.select_button = tk.Button(root, text="MP3 선택", command=self.select_mp3)
        self.select_button.pack(pady=5)

        # 분리 및 분석 시작 버튼
        self.start_button = tk.Button(root, text="분리 및 분석 시작", command=self.start_processing_thread, state=tk.DISABLED)
        self.start_button.pack(pady=5)

        self.mp3_file = None
        self.output_dir = None
        self.vocals_path = None  # 자동으로 설정될 vocals.wav 경로

    def select_mp3(self):
        """ MP3 파일 선택 """
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.mp3_file = os.path.abspath(file_path)  # 절대 경로 변환
            self.output_dir = os.path.abspath(os.path.join(os.path.dirname(self.mp3_file), "output"))
            self.start_button.config(state=tk.NORMAL)  # MP3 파일 선택 시 버튼 활성화
            self.label.config(text="선택된 파일: " + os.path.basename(file_path))

    def start_processing_thread(self):
        """ MP3 분리 및 음성 분석을 별도 스레드에서 실행하여 UI가 멈추지 않도록 함 """
        threading.Thread(target=self.split_and_analyze, daemon=True).start()

    def split_and_analyze(self):
        """ MP3 분리 후 자동으로 `vocals.wav` 분석 및 음성 분리 실행 """
        if not self.mp3_file:
            messagebox.showerror("오류", "MP3 파일을 먼저 선택하세요.")
            return

        try:
            self.label.config(text="MP3 분리 중... 잠시 기다려 주세요.")
            separator = Separator('spleeter:2stems')  # 보컬과 반주 분리 (2 stems)

            # Spleeter 실행 (오디오 분리)
            separator.separate_to_file(self.mp3_file, self.output_dir)

            # MP3 파일명에서 확장자 제거 (Spleeter가 생성하는 폴더 찾기)
            mp3_filename = os.path.splitext(os.path.basename(self.mp3_file))[0]
            vocals_dir = os.path.join(self.output_dir, mp3_filename)  # "output/eaw_track2"
            self.vocals_path = os.path.join(vocals_dir, "vocals.wav")  # "output/eaw_track2/vocals.wav"

            # 파일이 완전히 생성될 때까지 대기
            time.sleep(2)
            if not os.path.exists(self.vocals_path):
                messagebox.showerror("오류", f"보컬 파일이 존재하지 않습니다.\n경로 확인: {self.vocals_path}")
                return

            # UI 업데이트
            self.label.config(text="MP3 분리 완료!")

            # 남자/여자 음성 분리 및 저장
            self.split_male_female()

        except Exception as e:
            messagebox.showerror("오류", f"MP3 분리 중 오류 발생: {e}")

    def split_male_female(self):
        """ 남자/여자 음성을 구별하여 별도의 MP3로 저장 """
        if not os.path.exists(self.vocals_path):
            messagebox.showerror("오류", "보컬 파일이 존재하지 않습니다.")
            return

        try:
            # 음성 로드
            y, sr = librosa.load(self.vocals_path, sr=None)
            sound = Sound(self.vocals_path)
            pitch = sound.to_pitch()
            pitch_values = pitch.selected_array['frequency']
            pitch_values = pitch_values[pitch_values > 0]  # 0Hz 값(무음 구간) 제거

            avg_pitch = np.mean(pitch_values)

            # 음성 분리 (남자 < 180Hz, 여자 >= 180Hz)
            male_segments = []
            female_segments = []
            frame_length = len(y) // len(pitch_values)

            for i, freq in enumerate(pitch_values):
                start_time = i * frame_length / sr
                end_time = (i + 1) * frame_length / sr

                if freq < 180:
                    male_segments.append((start_time, end_time))
                else:
                    female_segments.append((start_time, end_time))

            # MP3 변환을 위해 원본 오디오 불러오기
            audio = AudioSegment.from_wav(self.vocals_path)

            male_file = os.path.join(self.output_dir, "male_voice.mp3")
            female_file = os.path.join(self.output_dir, "female_voice.mp3")

            # 남자 음성 파일 저장
            if male_segments:
                male_audio = sum(audio[int(start * 1000):int(end * 1000)] for start, end in male_segments)
                male_audio.export(male_file, format="mp3")

            # 여자 음성 파일 저장
            if female_segments:
                female_audio = sum(audio[int(start * 1000):int(end * 1000)] for start, end in female_segments)
                female_audio.export(female_file, format="mp3")

            # 생성된 파일이 존재하는지 확인
            if os.path.exists(male_file) and os.path.exists(female_file):
                messagebox.showinfo("완료", f"남자/여자 음성 분리 완료!\n출력 폴더: {self.output_dir}")
            else:
                messagebox.showerror("오류", "음성 분리된 파일이 정상적으로 생성되지 않았습니다.")

        except Exception as e:
            messagebox.showerror("오류", f"남자/여자 음성 분리 중 오류 발생: {e}")

# Tk()는 한 번만 생성
if __name__ == "__main__":
    root = tk.Tk()
    app = MP3SplitterApp(root)
    root.mainloop()

