# GPT_Prompts_4

### Description:
 
   This project provides a terminal based chat interface where the user can enter a keyword (Prompt), and the system retrieves the corresponding prompt from a `CSV` file.
   The chatbot uses [_OpenAI's GPT model_](https://openai.com) to generate responses to user inputs based on prompt and user input. 

   If the keyword (Prompt) is not found, the program suggests alternative keywords from the provided CSV file. Alternatively, the user can type the beginning characters followed by the `return` key.

   Then, using [_OpenAI's API_](https://openai.com), the system generates a response based on the messages exchanged so far between the user and the system. 

   The program can also generate speech-to-text and text-to-speech responses allowing user to interact with the chat bot via voice. This feature is has a built-in or default voice interface, however the program has support for users who want to create custom voice responses using [__ElevenLabs API__](https://beta.elevenlabs.io).

Optionally, the program can automatically generate a desktop shortcut for convenient access.


### Installation:

   * To install __GPT_Prompts4__ all you need to do is, clone this repository with `git clone https://github.com/Awo16/GPT_prompts.git`. Alternatively download the zip file [here](https://github.com/Awo16/GPT_prompts/archive/refs/heads/master.zip).

   * On Mac, install PortAudio using [Homebrew](http://brew.sh/): `brew install portaudio`.
   (For enabling microphone support).

   * Finally you will need to run `pip install -r requirements.txt`.


### Configuration:

   In a file called `config.py`, you can configure the program with your API keys and add necessary 
   file paths for the program to run correctly. You can also configure the custom voices if desired.

### Usage:

   Users can specify which of [_OpenAI's](https://openai.com) LLM models to use by passing the model name as a command line argument. If no command line argument is provided, default: gpt-3.5-turbo.
   
   __Example:__ 
                ```$: python3 gpt_prompts.py gpt-3.5-turbo```
                ```$: python3 gpt_prompts.py gpt-4```
   
   _Watch the demo video for complete examples._

   #### DEMO: [![Watch the video](https://img.youtube.com/vi/zGgqm7ftGv0/maxresdefault.jpg)](https://youtu.be/zGgqm7ftGv0)
 
 [Youtube demo](https://youtu.be/zGgqm7ftGv0)

   Finally, if the user wants to __Exit__ the chat, they can type `exit` to end the chat or `CTRL + D`.


