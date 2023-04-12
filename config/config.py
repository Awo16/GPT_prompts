# OpenAI models.

MODELS = (
    "gpt-3.5-turbo",
    "gpt-4",
)

# Speech transcript models.

SPEECH_MODELS = [
    "google",
    "whisper",
]

# Speech defaults.

DEFAULTS = {
    "SPEECH": False,            # Whether or not speech is enabled.
    "SPEECH_DEFAULT": True,     # Whether or not voice is default (built-in) or custom.
    "SPEECH_ENGINE": "whisper", # Default transcription engine.
    "CUSTOM_VOICE": "Bella",    # Default custom voice.
}

# Add custom voice names.

VOICES = [
    # Add custom voice names from ElevenLabs.

]

# Add API keys.

API_KEYS = {
    # Add your API keys here.
    "OPENAI_API_KEY": "", # (required)
    "ELEVENLABS_API_KEY": "", # (Optional: for custom voices)
}

# Add file path for your .csv file containing your prompts (required).
# Add file path for audio cache (required).
# Add file path for this repository to create a desktop shortcut (optional).

PATHS = {
    "CSV": "",              # Add CSV file path with prompts.
    "AUDIO_CACHE": "",      # Add path to this repository.
    "SHORTCUT": "",         # Add path to this repository for desktop shortcut.
}