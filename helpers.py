from config.config import PATHS
from pyfiglet import Figlet
from pyshortcuts import make_shortcut
from elevenlabslib import ElevenLabsUser
from rich.console import Console
import speech_recognition as sr
import pyttsx3
import sys
import openai
import random
import csv
import os

def prompt_initialize(input: str) -> list[dict]:
    console = Console()
    placeholder = greetFiglet("small", "GPT_Prompts_3")
    messages = []
    try:
        user_prompt = get_prompt(input, PATHS['CSV'])
        console.print(
            f'[dim]{"=" * 100}[/]\n [bold yellow]==> {user_prompt["act"].upper()}[/]\n\n',
            f'"[bold white]{user_prompt["prompt"]}[/]"\n [dim]{"=" * 100}[/]\n',
            style="bold",
            justify="center",
        )
        ask = console.input("[bold yellow]==> Confirm: [/]").strip()
        messages.append({"role": "system", "content": user_prompt["prompt"]})
        messages.append({"role": "user", "content": ask})
        return messages
    
    except EOFError:
        console.print("[red underline]Chat Exited.[/]")
        sys.exit(f"{placeholder}")


def shortcut(filepath=None):
    """
    This function creates a shortcut to the specified file.

    Parameters:
    -----------
    - filepath (str): The path of the file for which shortcut is to be created.

    Returns:
    --------
    None
    """
    if filepath:
        make_shortcut(filepath, name="GPT_Prompts_4")

def greetFiglet(font=None, text="Hello, World"):
    """
    Create an ASCII art of the provided text using Figlet library.

    Args:
        font (str): A string containing the name of the font to be used. If no font is provided, a random font will be chosen.
        text (str): A string containing the text to be converted to ASCII art.

    Returns:
        A string containing the ASCII art created using the Figlet library.

    Raises:
        ValueError: If text arg is not provided or is an empty string.

    Usage:
        greetFiglet(font='slant')
        greetFiglet(text='Hello')
        greetFiglet(font='isometric3', text='Hello, World!')
        greetFiglet() -> Uses random font and default 'Hello, World' text.
    """
    if font != None:
        f = Figlet(font=font)
        if text != "":
            render = f.renderText(text)
        else:
            raise ValueError(
                "Usage: greetFiglet() [text argument (if provided) cannot be a blank string]"
            )
    else:
        fonts = Figlet()
        random_font = random.choice(fonts.getFonts())
        f = Figlet(font=random_font)
        if text != "":
            render = f.renderText(text)
            print(f"____Font: {random_font}____")
        else:
            raise ValueError(
                "Usage: greetFiglet() [text argument (if provided) cannot be a blank string]"
            )
    return render


def read_csv(csv_path):
    """
    Reads data from a CSV file and returns it as a list of dictionaries.

    Args:
    csv_path (str): Path of the CSV file to be read.

    Returns:
    prompts (list): List of dictionaries, with each dictionary containing the data of a row in the CSV file.

    Raises:
    FileNotFoundError: If the provided CSV file path is invalid.
    """
    try:
        prompts = []
        with open(csv_path) as file:
            reader = csv.DictReader(file, fieldnames=('act', 'prompt'))
            for row in reader:
                prompts.append(row)
        return prompts
    except FileNotFoundError:
        raise ValueError(
            'Usage: Please configure "CSV" in config.py\n'
            + 'Hint: Check file path for valid .csv file.'
        )


def get_suggestion(input: str, csv_path: str):
    """
    Takes a string input and returns a list of suggestions based on a sorted list of prompt dictionaries.
    Args:
        input (str): The input text string to base suggestions on.
    Returns:
        list: A list of suggestion strings sorted in alphabetical order.
    """
    suggester = []
    prompts = read_csv(csv_path)
    for prompt in sorted(prompts, key=lambda prompt: prompt['act']):
        if prompt['act'].lower().startswith(input.lower()):
            suggester.append(prompt['act'])
    return suggester


def get_prompt(input: str, csv_path: str):
    """
    Searches for the input string in the "act" column of a csv file and returns the corresponding 'prompt' dictionary.

    Args:
    input (str): the search string to be compared to the 'act' column of the csv file

    Returns:
    prompt (dict) : A dictionary containing "act", "prompt", keys that
    correspond to the matched 'act' in the csv file.

    Raises:
    FileNotFoundError: If the csv file path is invalid, or the given 'input' string does not match any 'act' column in the csv file.
    """
    prompts = read_csv(csv_path)
    for prompt in prompts:
        if input.lower() == prompt['act'].lower():
            return prompt
    raise FileNotFoundError


def recognize_speech(status: bool, engine: str):
    """
    Recognizes speech using the given speech recognition `engine` and returns the transcribed `text`.

    Parameters:
        status (bool): Specifies if the speech recognizer and microphone should be initialized.
        engine (str): Specifies the speech recognition engine to be used. Supported values are 'google' and 'whisper'.

    Returns:
        str: The recognized and transcribed text.

    Raises:
        IOError: The audio file could not be opened or read.
        ValueError: The audio data is empty, or the speech could not be recognized.
    """
    if status == True:
        r = sr.Recognizer()
        mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        if engine.lower() == "google":
            text = r.recognize_google(audio)

        elif engine.lower() == "whisper":
            if PATHS['AUDIO_CACHE'] == '':
                raise ValueError(
                    'Usage: Please configure "AUDIO_CACHE" in config.py to enable Whisper-1 audio transcription.'
                )
            file_path = PATHS['AUDIO_CACHE'] + '/audio_cache/audio.wav'
            with open(file_path, "wb") as f:
                f.write(audio.get_wav_data())
            audio_file = open(file_path, "rb")
            text = openai.Audio.transcribe("whisper-1", audio_file, language="en")["text"]

            if os.path.exists(file_path):
                os.remove(file_path)
        return text


def txt_speech(txt: str):
    """
    Converts the given text into speech using the pyttsx3 library.

    Parameters:
    txt (str): The text to be converted into speech

    Returns:
    None

    Usage:
    txt_speech("Hello World")
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    engine.say(txt)
    engine.runAndWait()
    engine.stop()


def txt_speech2(txt, voice="Bella", api_key=None):
    """
    Converts the given text into speech, using the ElevenLabs API.

    Parameters:
    - txt (str): the text to be converted into speech.
    - voice (str): the name of the voice to use for the speech. Default is 'Bella'.
    - api_key (str): the API key to use for authentication. If not provided, a public key will be used.

    Returns: Nothing.

    Side effects: Plays the generated audio using the selected voice, blocking until the audio finishes playing.

    Examples:

    >>> txt_speech2('Hello world!')
    # Plays the audio equivalent of the string 'Hello world!' using the 'Bella' voice.
    """
    if api_key == None or api_key == '':
        raise ValueError(
            "Usage: Please configure 'ELEVENLABS_API_KEY' in config.py to enable custom voices."
        )
    user = ElevenLabsUser(api_key)
    voice = user.get_voices_by_name(voice)[0]
    voice.generate_and_play_audio(txt, playInBackground=False)