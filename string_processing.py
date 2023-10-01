import unicodedata

def remove_accents(s: str) -> str:
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def is_lower(c : str) -> bool:
    return 'a' <= c <= 'z'

def is_upper(c : str) -> bool:
    return 'A' <= c <= 'Z'

def is_latin(c : str) -> bool:
    return is_lower(c) or is_upper(c)

def add_char(a : str, b : str) -> str:
    if not is_latin(a) or not is_latin(b):
        return a
    a_num = ord(a)-ord('a')
    b_num = ord(b)-ord('a')
    a_num = (a_num + b_num) % 26
    return chr(a_num + ord('a'))

def sub_char(a : str, b : str) -> str:
    if (not is_latin(a)) or (not is_latin(b)):
        return a
    a_num = ord(a)-ord('a')
    b_num = ord(b)-ord('a')
    a_num = (a_num - b_num) % 26
    return chr(a_num + ord('a'))

def remove_non_latin(word: str) -> str:
    return "".join(c for c in word if is_latin(c))

def get_latin_words(cipher: str) -> list[str]:
    clean_words = [remove_non_latin(word.strip()) for word in cipher.split()]
    return [word for word in clean_words if len(word) > 0]
