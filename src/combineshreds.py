from shred import Shred
from PIL import Image

#
# Run tests
#

def find_match(shreds):
	for i, left_shred in enumerate(shreds):
		best_match_confidence = 0
		best_match_index = None
		for j, right_shred in enumerate(shreds):
			if i == j:
				continue
			print(f"Comparing shreds {i} and {j}")
			confidence = left_shred.aligns_left_of(right_shred)
			if confidence > best_match_confidence:
				best_match_index = j
				best_match_confidence = confidence
		if best_match_index is None:
			return False
		new_shred = left_shred.attach_left_of(shreds[best_match_index])
		shreds.remove(shreds[best_match_index])
		shreds.remove(left_shred)
		shreds.insert(0, new_shred)
		return True
	return False

if __name__ == '__main__':

	# Get all shreds (adjust as necessary)
	shreds = []
	for i in range(8):
		shreds.append(Shred(Image.open(f"intermediaries/shred_{i}_example_8_shreds.png"), 800))

	lookingForMatches = True
	while lookingForMatches:
		lookingForMatches = find_match(shreds)

	for index, shred in enumerate(shreds):
		shred.image.save(f"outputs/document{index}.png")