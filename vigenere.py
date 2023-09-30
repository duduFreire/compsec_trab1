def is_lower(c : chr) -> bool:
	return 'a' <= c <= 'z'

def is_upper(c : chr) -> bool:
	return 'A' <= c <= 'Z'

def is_latin(c : chr) -> bool:
	return is_lower(c) or is_upper(c)

# adds two lower case latin characters
def add_char(a : chr, b : chr) -> bool:
	a_num = ord(a)-ord('a')
	b_num = ord(b)-ord('a')
	a_num = (a_num + b_num) % 26
	return chr(a_num + ord('a'))

def sub_char(a : chr, b : chr) -> bool:
	a_num = ord(a)-ord('a')
	b_num = ord(b)-ord('a')
	a_num = (a_num - b_num) % 26
	return chr(a_num + ord('a'))

def encrypt(text : str, key : str) -> str:
	lower_text = text.lower()
	cipher = ""
	for i in range(len(text)):
		if not is_latin(lower_text[i]): 
			cipher += lower_text[i]
			continue
		
		new_c = add_char(lower_text[i], key[i % len(key)])
		if is_upper(text[i]):
			cipher += new_c.upper()
		else:
			cipher += new_c
	
	return cipher

def decrypt(text : str, key : str) -> str:
	lower_text = text.lower()
	cipher = ""
	for i in range(len(text)):
		if not is_latin(lower_text[i]): 
			cipher += lower_text[i]
			continue
		
		new_c = sub_char(lower_text[i], key[i % len(key)])
		if is_upper(text[i]):
			cipher += new_c.upper()
		else:
			cipher += new_c
	
	return cipher
