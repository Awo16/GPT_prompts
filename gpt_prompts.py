from helpers import *
from config.config import *
from rich.console import Console
import speech_recognition as sr
from pick import pick
import openai
import sys
import os

# Add csv path.
csv_path = PATHS["CSV"]

# Add API keys.
openai.api_key = API_KEYS['OPENAI_API_KEY']
elevenlabs_api_key = API_KEYS['ELEVENLABS_API_KEY']

# Add speech defaults.
SPEECH = DEFAULTS['SPEECH'] 
SPEECH_DEFAULT = DEFAULTS['SPEECH_DEFAULT'] 
SPEECH_ENGINE = DEFAULTS['SPEECH_ENGINE'] 
CUSTOM_VOICE = DEFAULTS['CUSTOM_VOICE']

# Add custom voices.
voices = VOICES

# Add model.
models = MODELS
temperature = TEMP

def main():
# The __main()__ function first generates a formatted greeting using __ASCII__ art, 
#  prompts the user for input, and retrieves the corresponding prompt to generate an initial response. 

#  It uses a while loop to continue generating new responses based on user inputs, appending the system's and
#  user's messages to a list, until the user prompts the chatbot to exit. 

#  If any exceptions are raised by [_OpenAI's API_](https://openai.com), the program logs the error and exits gracefully.

    console = Console()
    messages = []
    
    if PATHS['SHORTCUT'] != "":
        if not os.path.exists(PATHS['SHORTCUT'] + "/shortcut.txt"):
            shortcut(PATHS['SHORTCUT'] + "/gpt_prompts.py")
            path = PATHS['SHORTCUT'] + "/shortcut.txt"
            with open(path, 'w') as f:
                f.write(f'SHORTCUT = TRUE\nSELF = {path}')

    if len(sys.argv) == 2:
        if sys.argv[1] in models:
            engine = sys.argv[1]
        else:
            console.print("[bold]==> Available models: [/]")
            for model in models:
                console.print(f"{model.upper()}", style="bold green")
            sys.exit()
    elif len(sys.argv) < 2:
        engine = models[0]

    placeholder = greetFiglet("small", "GPT_Prompts_4")
    greet = greetFiglet("slant", "GPT_Prompts_4")
    console.print(
        f"[blue underline]Model: ==> {engine.upper()}[/]\n\n",
        f"{greet}",
        style="blue",
        justify="center",
    )

    speech_io = console.input("[green]Activate speech? {yes/no} ").strip().lower()
    if speech_io in ["yes", "y"]:
        global SPEECH
        global SPEECH_ENGINE
        SPEECH = True
        custom_q = console.input("[green]Custom voice? {yes/no} ").strip()
        if custom_q.lower() in ["yes", "y"]:
            if API_KEYS['ELEVENLABS_API_KEY'] == "":
                sys.exit(
                    "Usage: Please configure 'ELEVENLABS_API_KEY' in config.py to enable custom voices."
                )
            global SPEECH_DEFAULT
            SPEECH_DEFAULT = False
            custom_voice, _ = pick(
                voices,
                "<--CHOOSE CUSTOM VOICE-->",
                indicator="==>"
            )
            global CUSTOM_VOICE
            CUSTOM_VOICE = custom_voice.capitalize()
        speech_engine, _ = pick(SPEECH_MODELS, "<--CHOOSE SPEECH TRANSCRIPTION MODEL-->", indicator="==>") 
        SPEECH_ENGINE = speech_engine
    else:
        pass

    while True:
        try:
            user_input = (
                console.input(
                    "[bold underline]Press 'Enter' for suggestions.[/]\n"
                    + "[yellow]Enter Keyword: [/]"
                )
                .strip()
            )
            m = prompt_initialize(user_input)
            for message in m:
                messages.append(message)
            break

        except FileNotFoundError:
            suggestion = get_suggestion(user_input, csv_path)
            if len(suggestion) > 0:
                suggestion.append('>>> GO BACK')
                u_pick, _ = pick(
                    suggestion,
                    "** Try one of the following **",
                    indicator="==>"
                )
                if u_pick == '>>> GO BACK':
                    continue
                else:
                    m = prompt_initialize(u_pick)
                    for message in m:
                        messages.append(message)
                    break
            else:
                console.print(
                    "** No suggestions found ** ⛔",
                    style="red underline"
                )
                continue

    while True:
        try:
            with console.status("Thinking...", spinner="dots12"):
                response = openai.ChatCompletion.create(
                    model=engine,
                    messages=messages,
                    temperature=temperature
                )

            content = response["choices"][0]["message"]["content"]
            console.print(
                f"[dim]{'=' * 100}[/]\n[bold green]==> RESPONSE:[/]\n\n",
                f"[bold white]{content}[/]\n[dim]{'=' * 100}[/]",
                style="bold",
                justify="center",
            )

            if SPEECH == True:
                with console.status("Responding...", spinner="dots12"):
                    if SPEECH_DEFAULT == True:
                        txt_speech(content)
                    else:
                        try:
                            txt_speech2(content, CUSTOM_VOICE, elevenlabs_api_key)
                        except ValueError as error:
                            sys.exit(f"Error: {error}")

            while True:
                if SPEECH == True:
                    ask2 = (
                            console.input(
                            "[bold underline]Press 'Enter' for speech.[/]\n"
                            + "[bold yellow]==> Ask: [/]"
                        )
                        .strip()
                        .lower()
                    )
                else:
                    ask2 = (
                            console.input(
                            "[bold yellow]==> Ask: [/]"
                        )
                        .strip()
                        .lower()
                    )
                if ask2 != "":
                    break

                if ask2 == "" and SPEECH == True:
                    with console.status("Listening...", spinner="dots12"):
                        try:
                            ask2 = recognize_speech(SPEECH, SPEECH_ENGINE)
                            console.print(
                                f"[bold yellow]==> {SPEECH_ENGINE.capitalize()}: {ask2}[/]"
                            )
                            break

                        except sr.UnknownValueError:
                            console.print(
                                f"[bold yellow]==>[/] I didn't understand. Try saying it again?"
                            )
                        except ValueError as error:
                            sys.exit(f"Error: {error}")

            if ask2.upper() == "EXIT" or ask2.upper() == "EXIT.":
                console.print("[red underline]Chat Exited.[/]")
                sys.exit(f"{placeholder}")

            messages.append(
                {
                    "role": response["choices"][0]["message"]["role"],
                    "content": response["choices"][0]["message"]["content"],
                }
            )
            messages.append(
                {
                    "role": "user",
                    "content": ask2,
                }
            )
            continue

        except EOFError:
            console.print("[red underline]Chat Exited.[/]")
            sys.exit(f"{placeholder}")

        except openai.error.APIError as error:
            sys.exit(f"OpenAI API returned an API Error: {error}")

        except openai.error.APIConnectionError as error:
            sys.exit(f"Failed to connect to OpenAI API: {error}")

        except openai.error.AuthenticationError as error:
            sys.exit(f"OpenAI API key or token was invalid, expired, or revoked: {error}")

        except openai.error.InvalidRequestError as error:
            sys.exit(f"OpenAI API request was invalid: {error}")

        except openai.error.RateLimitError as error:
            sys.exit(f"OpenAI API returned RateLimit error: {error}")

if __name__ == "__main__":
    main()
