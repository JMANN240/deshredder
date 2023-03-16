from shred import Shred
from PIL import Image

#
# Run tests
#

def find_match(shreds, confidence_threshold = 0.2):
	shred = shreds[0]
	best_match_confidence = 0
	best_match_side = None
	best_match_index = None
	for i, test_shred in enumerate(shreds[1:]):
		i += 1
		left_confidence = shred.aligns_left_of(test_shred)
		print(f"\t{left_confidence}")
		if left_confidence > confidence_threshold and left_confidence > best_match_confidence:
			best_match_confidence = left_confidence
			best_match_side = 'L'
			best_match_index = i
		right_confidence = shred.aligns_right_of(test_shred)
		print(f"\t{right_confidence}")
		if right_confidence > confidence_threshold and right_confidence > best_match_confidence:
			best_match_confidence = right_confidence
			best_match_side = 'R'
			best_match_index = i
	print(best_match_confidence)
	if best_match_index is None:
		shreds.remove(shred)
		return shred
	if best_match_side == 'L':
		new_shred = shred.attach_left_of(shreds[best_match_index])
	elif best_match_side == 'R':
		new_shred = shred.attach_right_of(shreds[best_match_index])
	shreds.remove(shreds[best_match_index])
	shreds.remove(shred)
	shreds.insert(0, new_shred)
	return None

if __name__ == '__main__':

	# Get all shreds (adjust as necessary)
	shreds = []
	for i in range(8):
		shreds.append(Shred(Image.open(f"intermediaries/shred_{i}_example_8_shreds.png"), 600, search_depth=3, black_threshold=3))

	documents = []
	while len(shreds) > 0:
		new_document = find_match(shreds)
		if new_document is not None:
			documents.append(new_document)

	for index, document in enumerate(documents):
		document.image.save(f"outputs/document{index}.png")