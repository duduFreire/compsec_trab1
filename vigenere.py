from string_processing import is_latin, add_char, sub_char

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


