# Text to Audio Conversion Tool

This Python script utilizes the Google Text-to-Speech API to convert **text from the clipboard** into an audio file and copies the file to the clipboard.

## Usage

1. Copy any text to your clipboard.
2. Run the script:

```bash
python text2audio.py
```

3. The script will detect the text from the clipboard, convert it to audio, save it in the specified directory, and copy the file path to the clipboard.

## Requirements

- Python 3
- `requests` library for making API calls.
- `pyperclip` library for clipboard operations.
- `yaml` library to parse configuration files.
- `langdetect` library to detect the language of the text.
- Internet connection for API access.

## Setup

1. Install the required Python libraries:

```bash
pip install requests pyperclip yaml langdetect
```

2. Create a `config.yaml` file in the same directory as the script with the following structure:

```yaml
key: YOUR_GOOGLE_API_KEY
audio_dir: "~/Downloads"
```

Replace `YOUR_GOOGLE_API_KEY` with your actual API key from Google Cloud. 
You will receive a $300 credit upon signing up, which should be sufficient for a large number of requests. Please see the [Google Cloud documentation](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries) for more information.

## Supported Languages

Currently, the script supports the following languages:
- Cantonese (`zh-HK`)
- Japanese (`ja-JP`)
- English (`en-US`)

## Notes

- The audio file is named `synthesize.mp3` and will be saved in the user's Downloads directory by default. If the file already exists, a new file with an incremented number will be created to avoid overwriting.
- The saved audio file will be copied to the clipboard on macOS, Windows, and Linux. Ensure that clipboard utilities like `xclip` or `xsel` are installed on Linux.
- The script requires a valid Google API key set in the `config.yaml` file to function properly.