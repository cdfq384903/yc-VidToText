import unittest
from unittest import TestCase
import os
from src.VideoAudioExtractor import VideoAudioExtractor


class TestVideoAudioExtractor(TestCase):
    def setUp(self):
        """
        测试前的初始化操作
        """
        self.video_path = '../resources/video/demo_video.mp4'
        self.audio_path = '../resources/audio/extracted_audio.wav'
        self.model_path = '../resources/language_models/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15'
        self.output_path = '../output/transcription.txt'

        self.extractor = VideoAudioExtractor(self.video_path)
        self.extractor.load_video()

    def tearDown(self):
        """
        測試結束後的清理操作
        """
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)
        self.extractor.close_video()

    def test_extract_audio(self):
        """
        測試語音擷取功能
        """
        self.extractor.extract_audio(self.audio_path)
        self.assertTrue(os.path.exists(self.audio_path), "Audio file was not created.")

    def test_transcribe_audio_with_vosk(self):
        """
        測試使用Vosk進行語音轉文字
        """
        audio_path = self.extractor.extract_audio(self.audio_path)
        transcribed_text = self.extractor.transcribe_audio_with_vosk(audio_path, self.model_path, self.output_path)
        self.assertIsInstance(transcribed_text, str, "Transcribed text should be a string.")
        self.assertGreater(len(transcribed_text), 0, "Transcribed text should not be empty.")


if __name__ == '__main__':
    unittest.main()
