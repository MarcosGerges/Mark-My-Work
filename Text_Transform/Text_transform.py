# Invert all cases
def invert_case(text):
	return text.swapcase()

# Swap the first and last letters of the string
def swap_first_last_letters(text):
	characters = list(text)
	letter_positions = [
		index for index, character in enumerate(characters) if character.isalpha()
	]
	first_letter = letter_positions[0]
	last_letter = letter_positions[-1]
	characters[first_letter], characters[last_letter] = (
		characters[last_letter],
		characters[first_letter],
	)
	return "".join(characters)

# Add a comma after the first 5 characters of the string
def add_comma(text):
	if len(text) <= 5:
		return text + ","
	return text[:5] + "," + text[5:]


def transform_text(text):
	text = invert_case(text)
	text = swap_first_last_letters(text)
	return add_comma(text)


def get_valid_input():
	while True:
		text = input("Enter a string: ")
		if sum(character.isalpha() for character in text) > 1:
			return text
		print("Please re-enter a string with at least two letters.")


print(transform_text(get_valid_input()))

"""
Enter a string:  
Please re-enter a string with at least two letters.
Enter a string:    
Please re-enter a string with at least two letters.
Enter a string: a
Please re-enter a string with at least two letters.
Enter a string: jeff
FEFJ,

Enter a string: BjFOOF
fJfoo,b
"""