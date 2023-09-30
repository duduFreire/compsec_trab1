def find_all(pattern : str, s : str) -> list[int]:
	import re
	return [mtch.start() for mtch in re.finditer(pattern, s)]

def trigram_periods(tri : str, text : str) -> set[int]:
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

