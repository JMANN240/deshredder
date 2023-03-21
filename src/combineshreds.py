from shred import Shred
from PIL import Image

#
# Run tests
#

# Combine the leftmost shred with it's right neighbor
# Return True if a match was found, False otherwise
def find_match_right(shreds):
	# Get the first shred
	shred = shreds[0]

	# If it is a right edge, there will be no match on the right, return False
	if shred.is_right_edge():
		return False
	
	best_match_confidence = 0
	best_match_index = None
	for i, test_shred in enumerate(shreds[1:]):
		i += 1
		left_confidence = shred.aligns_left_of(test_shred)
		if left_confidence > best_match_confidence:
			best_match_confidence = left_confidence
			best_match_index = i
	
	# Create the new shred, replace the old ones
	new_shred = shred.attach_left_of(shreds[best_match_index])
	shreds.remove(shreds[best_match_index])
	shreds.remove(shred)
	shreds.insert(0, new_shred)
	return True # Return True beacuse we found a match

# Combine the leftmost shred with it's left neighbor
# Return True if a match was found, False otherwise
def find_match_left(shreds):
	# Get the first shred
	shred = shreds[0]

	# If it is a left edge, there will be no match on the left, return False
	if shred.is_left_edge():
		return False
	
	best_match_confidence = 0
	best_match_index = None
	for i, test_shred in enumerate(shreds[1:]):
		i += 1
		right_confidence = shred.aligns_right_of(test_shred)
		if right_confidence > best_match_confidence:
			best_match_confidence = right_confidence
			best_match_index = i
	
	# Create the new shred, replace the old ones
	new_shred = shred.attach_right_of(shreds[best_match_index])
	shreds.remove(shreds[best_match_index])
	shreds.remove(shred)
	shreds.insert(0, new_shred)
	return True # Return True beacuse we found a match

if __name__ == '__main__':

	# Get all shreds (adjust as necessary)
	shreds = []
	for i in range(20):
		shreds.append(Shred(Image.open(f"intermediaries/shred_{i}_generated_shreds.png"), 2000, search_depth=1, black_threshold=1))

	# Connect all of the shreds to the right of the first shred
	while find_match_right(shreds):
		pass
	
	# Connect all of the shreds to the left of the first shred
	while len(shreds) > 1:
		find_match_left(shreds)

	for index, document in enumerate(shreds):
		document.image.save(f"outputs/document{index}.png")