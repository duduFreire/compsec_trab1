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

def clear_text(text: str) -> str:
    pass

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

def add_dict(dict1 : dict[int, int], dict2 : dict [int,int]) -> \
	dict[int,int]:
	for key in dict2:
		if key in dict1:
			dict1[key] += dict2[key]
		else:
			dict1[key] = dict2[key]

# Returns a dictionary D such that D[k] represents how many
# times the period key appeared as a possible candidate for the
# key size.
def trigram_period_table(text : str) -> dict[int, int]:
	result = dict()
	text = text.lower()
	for word in text.split():
		for i in range(len(word)-2):
			periods = trigram_periods(word[i:i+3], text)	
			add_dict(result, periods)	
	
	return result

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def find_key(cipher: str, key_size: int) -> str:
    key = ""
    for i in range(key_size):
        best_shift = "a"
        best_error = float("inf")
        for shift in ALPHABET:
            freq = defaultdict(int)
            total = 0
            for idx in range(i, len(cipher), key_size):
                shifted_char = vigenere.sub_char(cipher[idx], shift)
                freq[shifted_char] += 1
                total += 1

            for k in freq.keys():
                freq[k] /= total
                freq[k] *= 100

            error = frequency_table_error(freq, ENGLISH_LETTER_FREQUENCY)
            if (error < best_error):
                best_error = error
                best_shift = shift

        #print(best_shift)
        #print(error)
        key += best_shift

    return key


def break_cipher(cipher: str) -> str:
    cipher = cipher.lower()
    trigrams = trigram_period_table(cipher)
    best_trigrams = sorted(
            trigrams.keys(),
            key=lambda k: trigrams[k], 
            reverse=True
    )[:min(len(trigrams), 5)]

    possible_keys = [find_key(cipher, trigram) for trigram in best_trigrams]
    best_keys = list(sorted(
            possible_keys,
            key=lambda k: likelihood_of_valid_text(vigenere.decrypt(cipher, k), ENGLISH_WORDS_PATH),
            reverse=True
    ))
    return best_keys[0]
