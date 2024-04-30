import requests
import os
import subprocess
import platform
import pyperclip
import yaml
import fasttext

from urllib.parse import urlencode
from pathlib import Path


def get_config():
    config_file = Path(__file__).with_name("config.yaml")
    with open(config_file) as file:
        config = yaml.safe_load(file)
    return config


def detect_clipboard_text():
    language_map = {
        "ja": "ja-JP",
        "en": "en-US",
        "yue": "zh-HK",
        "zh": "zh-HK",
        "zh-tw": "zh-HK",
    }

    def detect_language(text):
        """Detect the language of the text using FastText."""
        # 使用FastText模型检测语言
        model = fasttext.load_model("lid.176.ftz")
        predictions = model.predict(text, k=1)  # k=1表示返回概率最高的一种语言
        language = predictions[0][0].split("__")[
            -1
        ]  # 格式是__label__zh, 需要取最后一部分

        print("FastText: ", language)

        return language_map.get(language, None)

    try:
        content = pyperclip.paste()
    except Exception as e:
        print(f"No access to clipboard: {e}")
        return

    if isinstance(content, str):
        print("CLIPBOARD CONTENT: ")
        print("------------------")
        print(content)
        print("------------------")

        language = detect_language(content)
        if language:
            print(f"Language of text: {language}")
            return (content, language)
        else:
            print(
                "No support for the language of the text, supported languages are: {}".format(
                    ", ".join(language_map.keys())
                )
            )
    else:
        print("Not a text content in the clipboard.")


def get_audio_url(content, language, key):
    params = {
        "enc": "mpeg",
        "client": "chromium",
        "key": key,
        "text": content,
        "lang": language,
        "name": "fis",
    }
    base_url = "https://www.google.com/speech-api/v2/synthesize"
    return f"{base_url}?{urlencode(params)}"


def save_audio(response, directory, base_filename):
    filename = base_filename
    filepath = Path(directory) / filename
    count = 1

    while filepath.exists():
        filepath = Path(directory) / f"{base_filename.split('.')[0]}_{count}.mp3"
        count += 1

    with open(filepath, "wb") as file:
        file.write(response.content)
    return filepath


def copy_to_clipboard(filepath):
    try:
        os_type = platform.system()
        if os_type == "Darwin":

            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'tell app "Finder" to set the clipboard to ( POSIX file "{filepath}" )',
                ],
                check=True,
            )
        elif os_type == "Windows":
            # Windows
            subprocess.run(
                ["clip"], input=filepath.strip().encode("utf-16"), check=True
            )
        elif os_type == "Linux":
            # Linux
            try:
                subprocess.run(
                    ["xclip", "-selection", "c", "-t", "text/uri-list", "-i"],
                    input=filepath.encode(),
                    check=True,
                )
            except FileNotFoundError:
                # Fallback to xsel
                subprocess.run(
                    ["xsel", "--clipboard", "--input"],
                    input=filepath.encode(),
                    check=True,
                )
        else:
            raise OSError("Unsupported operating system")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy to clipboard: {e}")


def main():
    config = get_config()
    content, language = detect_clipboard_text()
    url = get_audio_url(content, language, config["key"])
    response = requests.get(url)
    if response.status_code == 200:

        audio_dir = os.path.expanduser(config["audio_dir"])
        base_filename = "synthesize.mp3"

        filepath = save_audio(response, audio_dir, base_filename)
        print(f"The audio file has been saved as {filepath}")

        copy_to_clipboard(filepath)
        print("The file path has been copied to the clipboard.")
    else:
        print("Failed to retrieve the audio data.")


if __name__ == "__main__":
    main()
