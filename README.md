# GPT_Prompts_4

### Description:
 
   This project provides a terminal based chat interface where the user can enter a keyword (Prompt), and the system retrieves the corresponding prompt from a `CSV` file.
   The chatbot uses [_OpenAI's GPT model_](https://openai.com) to generate responses to user inputs based on prompt and user input. 

   If the keyword (Prompt) is not found, the program suggests alternative keywords from the provided CSV file. Alternatively, the user can type the beginning characters followed by the `return` key.

   Then, using [_OpenAI's API_](https://openai.com), the system generates a response based on the messages exchanged so far between the user and the system. 

   The program can also generate speech-to-text and text-to-speech responses allowing user to interact with the chat bot via voice. This feature is has a built-in or default voice interface, however the program has support for users who want to create custom voice responses using [__ElevenLabs API__](https://beta.elevenlabs.io).

   Optionally, the program can automatically generate a desktop shortcut for convenient access.
---

### Installation:

   * To install __GPT_Prompts4__ all you need to do is, `git clone` this repository. Alternatively download the zip file here.

   * On Mac, install PortAudio using [Homebrew](http://brew.sh/): `brew install portaudio`.
   (For enabling microphone support).

   * you will need to run `pip install -r requirements.txt`.

   * configure the program by adding required data in the `config.py` file.

   * make sure you have a valid [_OpenAI API key_](https://platform.openai.com).

   * optionally you can add a valid [_ElevenLabs API key_](https://beta.elevenlabs.io).


### Configuration:

   In a file called `config.py`, you can configure the program with your API keys and add necessary 
   file paths for the program to run correctly. You can also configure the custom voices if desired.
   Default voices from [__ElevenLabs__](https://beta.elevenlabs.io) are provided out of the box.

### Usage:

   Users can specify which of [_OpenAI's](https://openai.com) LLM models to use by passing the model name as a command line argument. If no command line argument is provided, default: gpt-3.5-turbo.
   __Example:__ ```$: python3 gpt_prompts.py gpt-3.5-turbo```
                ```$: python3 gpt_prompts.py gpt-4```
   
   _Watch the demo video for complete examples._

   #### DEMO: [![Watch the video](https://img.youtube.com/vi/zGgqm7ftGv0/maxresdefault.jpg)](https://youtu.be/zGgqm7ftGv0)

   [Youtube Demo](https://youtu.be/zGgqm7ftGv0)

   Finally, if the user wants to __Exit__ the chat, they can type `exit` to end the chat or `CTRL + D`.

### Updates:

   * Added selectable menu for better user interaction.

   * Added temperature parameter in the `config.py` file.

   For example:
               if user wants to activate speech recognition by typing `y` or `yes`.

![Screenshot-2023-04-19-at-7-49-21-PM.png](https://i.postimg.cc/Bn7xhbrD/Screenshot-2023-04-19-at-7-49-21-PM.png)

After inputting the command the user will see a menu like this:

[![Screenshot-2023-04-19-at-7-49-37-PM.png](https://i.postimg.cc/RVySXzPh/Screenshot-2023-04-19-at-7-49-37-PM.png)](https://postimg.cc/QHgZdvZZ)

Then the user will select a speech engine:

[![Screenshot-2023-04-19-at-7-50-04-PM.png](https://i.postimg.cc/g0GfKSPr/Screenshot-2023-04-19-at-7-50-04-PM.png)](https://postimg.cc/fVg2zvyh)

This feature also work with keyword suggestions. For example if a user inputs the letter `a`:

[![Screenshot-2023-04-19-at-7-50-31-PM.png](https://i.postimg.cc/pVnRrSVt/Screenshot-2023-04-19-at-7-50-31-PM.png)](https://postimg.cc/SjqwtDzZ)

The suggestion feature will provide suggestions via select menu:

[![Screenshot-2023-04-19-at-7-51-31-PM.png](https://i.postimg.cc/MKdPS6kZ/Screenshot-2023-04-19-at-7-51-31-PM.png)](https://postimg.cc/YhLfNwqT)


