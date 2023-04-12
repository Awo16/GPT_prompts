import pytest
from gpt_prompts import read_csv, get_prompt, get_suggestion

def test_get_suggestion():
    assert get_suggestion('hustle gpt') == ['Hustle GPT']
    assert get_suggestion('this doesnt exist') == []

def test_get_prompt():
    with pytest.raises(FileNotFoundError):
        get_prompt('hustle')

def test_read_csv():
    with pytest.raises(FileNotFoundError):
        read_csv('')
