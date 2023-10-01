def is_lower(c : chr) -> bool:
    return 'a' <= c <= 'z'

def is_upper(c : chr) -> bool:
    return 'A' <= c <= 'Z'

def is_latin(c : chr) -> bool:
    return is_lower(c) or is_upper(c)

# adds two lower case latin characters
def add_char(a : chr, b : chr) -> chr:
    if not is_latin(a) or not is_latin(b):
        return a
    a_num = ord(a)-ord('a')
    b_num = ord(b)-ord('a')
    a_num = (a_num + b_num) % 26
    return chr(a_num + ord('a'))

def sub_char(a : chr, b : chr) -> chr:
    if (not is_latin(a)) or (not is_latin(b)):
        return a
    a_num = ord(a)-ord('a')
    b_num = ord(b)-ord('a')
    a_num = (a_num - b_num) % 26
    return chr(a_num + ord('a'))

def encrypt(text : str, key : str) -> str:
    cipher = ""
    key_idx = 0
    for i in range(len(text)):
        if not is_latin(text[i]): 
            cipher += text[i]
            continue
        
        new_c = add_char(text[i], key[key_idx % len(key)])
        cipher += new_c
        key_idx += 1
    
    return cipher

def decrypt(text : str, key : str) -> str:
    cipher = ""
    key_idx = 0
    for i in range(len(text)):
        if not is_latin(text[i]): 
            cipher += text[i]
            continue
        
        new_c = sub_char(text[i], key[key_idx % len(key)])
        cipher += new_c
        key_idx += 1
    
    return cipher


