from functools import reduce
import os
import vigenere
from frequencies import *
from collections import defaultdict

SEP = os.path.sep
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + SEP
DATA_PATH = DIR_PATH + "data" + SEP
PORTUGUESE_WORDS_PATH = DATA_PATH + "portuguese_words.txt"
ENGLISH_WORDS_PATH = DATA_PATH + "english_words.txt"

def remove_non_latin(word: str) -> str:
    return "".join(c for c in word if vigenere.is_latin(c))

def get_cipher_words(cipher: str) -> list[str]:
    clean_words = [remove_non_latin(word.strip()) for word in cipher.split()]
    return [word for word in clean_words if len(word) > 0]

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

def load_words(words_path: str) -> list[str]:
    with open(words_path, "r") as f:
        words = set(f.read().split())

    return list(words)

def likelihood_of_valid_text(text: str, language_words: list[str]) -> float:
    text_words = get_cipher_words(text)
    number_of_valid_words = reduce(
        lambda v, word: v + (
            1 
            if word in language_words
            else 0
        ),
        text_words, 0
    )
    return number_of_valid_words / len(text_words)

def find_all(pattern : str, s : str) -> list[int]:
    pos = []
    for i in range(len(s) - len(pattern)+1):
        if s[i: i+len(pattern)] == pattern:
            pos.append(i)

    return pos

# Returns a dictionary whose keys are the possible periods of a 
# trigram (i.e the divisors of the differences between occurrences
# of the trigram) whose values are the frequency of the occurrence 
# of each key.
def trigram_periods(tri : str, text : str) -> dict[int, int]:
    occurrences = find_all(tri, text)
    differences = list()
    for i in range(len(occurrences)):
        for j in range(i+1, len(occurrences)):
            differences.append(occurrences[j] - occurrences[i])
    
    periods = dict()
    for diff in differences:
        for d in range(1, diff + 1):
            if diff % d == 0:
                if d in periods:
                    periods[d] += 1
                else:
                    periods[d] = 1
    
    return periods

def add_dict(
        dict1 : dict[int, int], 
        dict2 : dict [int,int]
    ) -> dict[int,int]:
    for key in dict2:
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]

# Returns a dictionary D such that D[k] represents how many
# times the period key appeared as a possible candidate for the
# key size.
def trigram_period_table(
        words: list[str], text : str, 
    ) -> dict[int, int]:
    result = dict()
    text = text.lower()
    for word in words:
        for i in range(len(word)-2):
            periods = trigram_periods(word[i:i+3], text)    
            add_dict(result, periods)   
    
    return result

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def find_key(
        cipher: str, key_size: int, 
        language_letter_frequency: dict[str, float]
    ) -> str:
    key = ""
    for i in range(key_size):
        best_shift = "a"
        best_error = float("inf")
        for shift in ALPHABET:
            freq = defaultdict(int)
            total = 0
            for idx in range(i, len(cipher), key_size):
                if vigenere.is_latin(cipher[idx]):
                    shifted_char = vigenere.sub_char(cipher[idx], shift)
                    freq[shifted_char] += 1
                    total += 1

            for k in freq.keys():
                freq[k] *= 100/total

            error = frequency_table_error(freq, language_letter_frequency)
            if (error < best_error):
                best_error = error
                best_shift = shift

        #print(best_shift)
        #print(error)
        key += best_shift

    return key

def break_language(
        language_valid_words: list[str], 
        language_letter_frequency: str,
        cipher_text: str,
        cipher_words: list[str],
        trigrams: list[int],
    ) -> tuple[str, float]:

    possible_keys = [
            find_key(cipher_text, trigram, language_letter_frequency) 
            for trigram in trigrams
    ]
    cipher = " ".join(cipher_words)
    best_keys = list(sorted(
            possible_keys,
            key=lambda k: likelihood_of_valid_text(
                vigenere.decrypt(cipher, k), language_valid_words
            ),
            reverse=True
    ))
    best_key = best_keys[0]
    return best_key, likelihood_of_valid_text(
            vigenere.decrypt(cipher, best_key), language_valid_words
            )

def break_cipher_in_en(cipher: str) -> str:
    only_letter_text = remove_non_latin(cipher)
    cipher_words = get_cipher_words(cipher)

    trigrams = trigram_period_table(cipher_words, only_letter_text)
    best_trigrams = sorted(
            trigrams.keys(),
            key=lambda k: trigrams[k], 
            reverse=True
    )[:min(len(trigrams), 5)]

    en_words = load_words(ENGLISH_WORDS_PATH)
    en_key, en_value = break_language(
            en_words, 
            ENGLISH_LETTER_FREQUENCY,
            only_letter_text,
            cipher_words,
            best_trigrams,
    )
    return en_key

def break_cipher_in_pt(cipher: str) -> str:
    only_letter_text = remove_non_latin(cipher)
    cipher_words = get_cipher_words(cipher)

    trigrams = trigram_period_table(cipher_words, only_letter_text)
    best_trigrams = sorted(
            trigrams.keys(),
            key=lambda k: trigrams[k], 
            reverse=True
    )[:min(len(trigrams), 5)]

    pt_words = load_words(PORTUGUESE_WORDS_PATH)
    pt_key, pt_value = break_language(
            pt_words, 
            PORTUGUESE_LETTER_FREQUENCY,
            only_letter_text,
            cipher_words,
            best_trigrams,
    )
    return pt_key


def break_cipher_in_all_languages(cipher: str) -> str:
    only_letter_text = remove_non_latin(cipher)
    cipher_words = get_cipher_words(cipher)

    trigrams = trigram_period_table(cipher_words, only_letter_text)
    best_trigrams = sorted(
            trigrams.keys(),
            key=lambda k: trigrams[k], 
            reverse=True
    )[:min(len(trigrams), 5)]

    pt_words = load_words(PORTUGUESE_WORDS_PATH)
    en_words = load_words(ENGLISH_WORDS_PATH)
    pt_key, pt_value = break_language(
            pt_words, 
            PORTUGUESE_LETTER_FREQUENCY,
            only_letter_text,
            cipher_words,
            best_trigrams,
    )
    en_key, en_value = break_language(
            en_words, 
            ENGLISH_LETTER_FREQUENCY,
            only_letter_text,
            cipher_words,
            best_trigrams,
    )
    if (en_value > pt_value):
        return en_key

    return pt_key
