from frequencies import *
from functools import reduce
import os

SEP = os.path.sep
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + SEP
DATA_PATH = DIR_PATH + "data" + SEP
PORTUGUESE_WORDS_PATH = DATA_PATH + "portuguese_words.txt"
ENGLISH_WORDS_PATH = DATA_PATH + "english_words.txt"


def error_fn(value1: float, value2: float) -> float:
    return (value1-value2)**2

def frequency_table_error(
        table: dict[str, float], 
        language_table: dict[str, float],
) -> float:
    return reduce(
        lambda v, key: v + error_fn(
            table.get(key, 0), language_table[key]
        ),
        language_table.keys(), 0
    )

def load_words(words_path: str) -> set[str]:
    with open(words_path, "r") as f:
        words = set(f.read().split())

    return words

def likelihood_of_valid_text(text: str, language_words_path: str) -> float:
    language_words = load_words(language_words_path)
    text_words = text.split()
    number_of_valid_words = reduce(
        lambda v, word: v + (
            1 
            if word in language_words
            else 0
        ),
        text_words, 0
    )
    return number_of_valid_words / len(text_words)

def main() -> None:
    print(frequency_table_error(
        {"a": 0.0, "b": 3.0}, ENGLISH_LETTER_FREQUENCY
    ))
    print(likelihood_of_valid_text("arroz feijão", PORTUGUESE_WORDS_PATH))


if __name__ == "__main__":
    main()
