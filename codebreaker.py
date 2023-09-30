def find_all(pattern : str, s : str) -> list[int]:
	import re
	return [mtch.start() for mtch in re.finditer(pattern, s)]

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
