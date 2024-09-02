from moviepy.editor import VideoFileClip
import wave
import json
import os

from pydub import AudioSegment
from vosk import Model, KaldiRecognizer


class VideoAudioExtractor:
    def __init__(self, video_path):
        """
        初始化時設定影片路徑
        """
        self.video_path = video_path
        self.video = None

    def load_video(self):
        """
        載入影片
        """
        self.video = VideoFileClip(self.video_path)

    def check_audio_format(self, audio_path):
        """
        檢查音訊檔案是否為單聲道PCM WAV格式
        """
        with wave.open(audio_path, "rb") as wf:
            print(f"Channels: {wf.getnchannels()}")
            print(f"Sample Width: {wf.getsampwidth()}")
            print(f"Frame Rate: {wf.getframerate()}")
            print(f"Compression Type: {wf.getcomptype()}")

    def extract_audio(self, output_audio_path):
        """
        將影片中的音訊提取並儲存為音訊檔案(儲存為單聲道PCM WAV file)
        """
        if self.video is None:
            raise ValueError("Video not loaded. Call load_video() first.")

        self.video.audio.write_audiofile(output_audio_path, codec='pcm_s16le')

        audio = AudioSegment.from_file(output_audio_path)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)

        output_audio_path_wav = os.path.splitext(output_audio_path)[0] + "_mono.wav"
        audio.export(output_audio_path_wav, format="wav")

        self.check_audio_format(output_audio_path_wav)

        return output_audio_path_wav

    def transcribe_audio_with_vosk(self, audio_path, model_path, output_path):
        """
        使用 Vosk 將音訊檔案轉換為文字
        """
        print(f"Transcribing audio file: {audio_path}")
        self.check_audio_format(audio_path)  # 再次确认文件格式

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}. Please download it from https://alphacephei.com/vosk/models")

        model = Model(model_path)

        with wave.open(audio_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                raise ValueError("Audio file must be WAV format mono PCM.")

            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)

            results = []

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    results.append(json.loads(result))

            final_result = rec.FinalResult()
            results.append(json.loads(final_result))

            transcript = ""
            for result in results:
                if "text" in result:
                    transcript += result["text"] + " "

            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcript)

            return transcript

    def close_video(self):
        """
        關閉影片檔案以釋放資源
        """
        if self.video:
            self.video.close()
            self.video = None
