import pygame
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
from pydub import AudioSegment
from threading import Thread

# pip install pygame pydub mutagen tk
# choco install ffmpeg (for windows)
#    Open PowerShell as Administrator and run the following command:
#      Remove-Item -Recurse -Force C:\ProgramData\Chocolatey
#      Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
#      [System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ProgramData\Chocolatey\bin", [System.EnvironmentVariableTarget]::Machine)
# sudo apt install ffmpeg (for linux)
# 
class MP3Editor:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Editor")

        # 초기 변수 설정
        self.mp3_file = None
        self.start_time = None
        self.end_time = None
        self.total_length = 0
        self.is_playing = False

        # UI 요소 생성
        self.label = tk.Label(root, text="MP3 파일을 선택하세요!", font=("Arial", 14))
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="MP3 선택", command=self.load_mp3)
        self.select_button.pack(pady=5)

        self.play_button = tk.Button(root, text="재생", command=self.play_mp3, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="일시정지", command=self.pause_mp3, state=tk.DISABLED)
        self.pause_button.pack(pady=5)

        self.backward_button = tk.Button(root, text="⏪ 뒤로 10초", command=self.backward_10s, state=tk.DISABLED)
        self.backward_button.pack(pady=5)

        self.forward_button = tk.Button(root, text="⏩ 앞으로 10초", command=self.forward_10s, state=tk.DISABLED)
        self.forward_button.pack(pady=5)

        self.start_button = tk.Button(root, text="Start", command=self.set_start_time, state=tk.DISABLED)
        self.start_button.pack(pady=5)

        self.end_button = tk.Button(root, text="End & Auto Save", command=self.set_end_time, state=tk.DISABLED)
        self.end_button.pack(pady=5)

        self.time_label = tk.Label(root, text="재생 시간: 0.0초", font=("Arial", 12))
        self.time_label.pack(pady=10)

    def load_mp3(self):
        """ MP3 파일 선택 및 로드 """
        self.mp3_file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if self.mp3_file:
            audio = MP3(self.mp3_file)
            self.total_length = audio.info.length  # 전체 길이(초)

            self.label.config(text=f"파일: {os.path.basename(self.mp3_file)}")
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)
            self.backward_button.config(state=tk.NORMAL)
            self.forward_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.NORMAL)
            self.end_button.config(state=tk.NORMAL)

    def play_mp3(self, start_time=0):
        """ MP3 재생 (특정 위치부터 시작 가능) """
        if not self.mp3_file:
            messagebox.showerror("오류", "MP3 파일을 선택하세요.")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(self.mp3_file)
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(start_time)  # 특정 위치에서 시작

        self.is_playing = True
        Thread(target=self.update_progress).start()

    def pause_mp3(self):
        """ MP3 일시정지 / 재개 """
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.pause_button.config(text="재개")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.pause_button.config(text="일시정지")

    def update_progress(self):
        """ 현재 재생 시간을 실시간으로 업데이트 """
        while pygame.mixer.music.get_busy():
            elapsed_time = pygame.mixer.music.get_pos() / 1000  # 밀리초(ms) -> 초(s)
            self.time_label.config(text=f"재생 시간: {elapsed_time:.1f}초 / {self.total_length:.1f}초")
            time.sleep(0.5)
            self.root.update()

    def backward_10s(self):
        """ 10초 뒤로 이동 """
        if self.mp3_file:
            current_time = pygame.mixer.music.get_pos() / 1000  # 현재 시간(초)
            new_time = max(0, current_time - 10)
            pygame.mixer.music.stop()
            self.play_mp3(start_time=new_time)

    def forward_10s(self):
        """ 10초 앞으로 이동 """
        if self.mp3_file:
            current_time = pygame.mixer.music.get_pos() / 1000
            new_time = min(self.total_length, current_time + 10)
            pygame.mixer.music.stop()
            self.play_mp3(start_time=new_time)

    def set_start_time(self):
        """ Start 버튼 클릭 시 현재 재생 시간을 저장 """
        self.start_time = pygame.mixer.music.get_pos() / 1000
        #messagebox.showinfo("Start", f"시작 시간 설정: {self.start_time:.2f}초")

    def set_end_time(self):
        """ End 버튼 클릭 시 현재 재생 시간을 저장하고 자동 저장 """
        self.end_time = pygame.mixer.music.get_pos() / 1000
        if self.start_time is None:
            messagebox.showerror("오류", "먼저 'Start' 버튼을 눌러 시작 시간을 설정하세요.")
            return

        if self.end_time <= self.start_time:
            messagebox.showerror("오류", "끝 시간이 시작 시간보다 커야 합니다.")
            return

        # 자동 저장 실행
        self.auto_save_cut_audio()

    def auto_save_cut_audio(self):
        """ MP3 파일을 자동으로 자르고 저장 (파일명에 _1, _2 추가) """
        base_dir = os.path.dirname(self.mp3_file)
        base_name = os.path.splitext(os.path.basename(self.mp3_file))[0]  # 확장자 제거한 파일명
        new_file = os.path.join(base_dir, f"{base_name}_1.mp3")

        # 파일명이 겹칠 경우 자동으로 숫자 증가
        counter = 1
        while os.path.exists(new_file):
            counter += 1
            new_file = os.path.join(base_dir, f"{base_name}_{counter}.mp3")

        # MP3 자르기 및 저장
        audio = AudioSegment.from_mp3(self.mp3_file)
        cut_audio = audio[self.start_time * 1000:self.end_time * 1000]
        cut_audio.export(new_file, format="mp3")

        #messagebox.showinfo("완료", f"MP3 파일이 자동 저장되었습니다:\n{new_file}")

# Tkinter 실행
root = tk.Tk()
app = MP3Editor(root)
root.mainloop()

