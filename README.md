# VidToText

該專案是一個用於從影片文件中提取音訊並進行語音轉文字的 Python 工具。它使用 [MoviePy](https://github.com/Zulko/moviepy) 提取音訊，使用 [Vosk](https://alphacephei.com/vosk/) 進行離線語音識別，將語音內容轉換為文字並保存到指定文件中。

## 功能

- 從影片文件中提取音訊
- 將提取的音訊轉換為單聲道 PCM WAV 格式
- 使用 Vosk 進行語音識別，將音訊轉錄為文字
- 自動創建輸出目錄並將轉錄文字保存為文件

## 模組介紹

### `VideoAudioExtractor`

`VideoAudioExtractor` 是核心類，提供了以下方法：

- `__init__(self, video_path)`: 初始化類實例，設置影片文件路徑。
- `load_video(self)`: 加載影片文件。
- `extract_audio(self, output_audio_path)`: 從影片中提取音訊並轉換為單聲道 PCM WAV 格式。
- `transcribe_audio_with_vosk(self, audio_path, model_path, output_path)`: 使用 Vosk 進行語音轉文字，並將結果保存到指定路徑。
- `close_video(self)`: 關閉影片文件以釋放資源。

## 環境依賴

- Python 3.6+
- `MoviePy`：用於處理影片和音訊文件
- `pydub`：用於音訊文件格式轉換
- `Vosk`：用於離線語音識別
- `FFmpeg`：用於音訊編碼（`MoviePy` 和 `pydub` 的依賴）

## 安裝步驟

1. **clone項目**：
    ```bash
    git clone https://github.com/your-repository/yc-vidtotext.git
    cd yc-vidtotext
    ```

2. **創建虛擬環境**：
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows 上為 venv\Scripts\activate
    ```

3. **安裝依賴**：
    ```bash
    pip install -r requirements.txt
    ```

4. **安裝 FFmpeg**：
   - 請根據您的操作系統安裝 FFmpeg，確保 `ffmpeg` 可在系統路徑中訪問。
   - 您可以參考 [FFmpeg 官網](https://ffmpeg.org/download.html) 獲取安裝方法。

5. **下載您所需要的 Vosk 語言模型**：
   - 您可以從 [Vosk 模型頁面](https://alphacephei.com/vosk/models) 下載適合的語言模型，例如英文模型：
     ```bash
     wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
     unzip vosk-model-small-en-us-0.15.zip -d resources/language_models/
     ```

## 使用說明

您可以通過以下命令從影片中提取音訊並將其轉錄為文字。

### 直接運行 Python 腳本

```bash
python main.py `
    --video_path resources/video/demo_video.mp4 `
    --audio_path resources/audio/extracted_audio.wav `
    --model_path resources/language_models/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15 `
    --output_path output/transcription.txt
