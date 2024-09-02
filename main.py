import argparse
from src.VideoAudioExtractor import VideoAudioExtractor


def main(video_path, audio_path, model_path, output_path):
    extractor = VideoAudioExtractor(video_path)
    extractor.load_video()
    new_audio_path = extractor.extract_audio(audio_path)
    transcribed_text = extractor.transcribe_audio_with_vosk(new_audio_path, model_path, output_path)
    print("Vosk Transcription:\n", transcribed_text)
    extractor.close_video()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Transcribe video audio using Vosk and save to a text file.")
    parser.add_argument('--video_path', type=str, required=True, help="Path to the video file.")
    parser.add_argument('--audio_path', type=str, required=True, help="Path to save the extracted audio file.")
    parser.add_argument('--model_path', type=str, required=True, help="Path to the Vosk language model directory.")
    parser.add_argument('--output_path', type=str, required=True, help="Path to save the transcribed text file.")

    args = parser.parse_args()

    main(args.video_path, args.audio_path, args.model_path, args.output_path)
