# Input: .epub file. Output: 'Book' object with the following attibutes:
# 'title', 'author', total_words', 'unique_words', 'duplicates'

import argparse, sys
import create_book as cb
import glob
import time

start = time.time()

# looks good https://en.wikipedia.org/wiki/Cloud_Atlas_(novel)

# # #

# To include:
# - compute average word length
# - number of times each word appears in book
# - Create set of 1000 most common words
# - check word in common_words for every word in book,
#	and find % which are uncommon.
#	seems like word in set should be fast enough:
#	https://stackoverflow.com/questions/5993621/fastest-way-to-search-a-list-in-python
# - characterise book complexity based on number (or %) of unique words,
#	average word length, % words which are uncommon.
# - scifi probably scores high on last test.


# if len(sys.argv) < 2:
# 	filename = 'test/frankenstein.epub'
# 	book_dir = "test/" + filename.split('/')[1].split(".")[0]
# 	short_name = filename.split('/')[1].split(".")[0]

# # in case we want to pass in the ebook filename as an argument:
# else:
# 	parser=argparse.ArgumentParser(description="description of program",
# 								   usage="...")
# 	# execute in a terminal with e.g. python3 main.py --filename "1984.epub" 
# 	parser.add_argument("-f", "--filename",
# 						help="File to open.",
# 						type=argparse.FileType('r'))
# 	args = parser.parse_args()


# loop over all ebooks in our catalogue:
path = "/main_1TB/Downloads/epubs"
# with open("summary.txt", "a") as myfile:

bp = 0.
bt = 'Unknown'
ba = 'Unknown'

for filename in glob.glob(path + "/*.epub"):

	book = cb.create_book_instance(filename)
	# print("\n")
	# print("Title: " + book.title)
	# print("Author: " + book.author)
	# print("Length: " + str(book.total_words) + " words")
	# print("Number of unique words: {}\n".format(book.unique_words))

	# myfile.write("Title: " + book.title + "\nAuthor: " + book.author \
	# 	+ "\nLength: " + str(book.total_words) + " words" + \
	# 	"\nNumber of unique words: {}".format(book.unique_words) + \
	# 	"\nPercentage unique: {:.1f}%".format(100*book.unique_words/book.total_words))
	# myfile.write("\n\n")

	# print(filename)

	if 100*book.unique_words/book.total_words > bp:
		bp = 100*book.unique_words/book.total_words
		bt = book.title
		ba = book.author

	if book.author=="Thomas Jefferson":
		print("Title: " + book.title)
		print("Author: " + book.author)
		print("Length: " + str(book.total_words) + " words")
		print("Number of unique words: {}\n".format(book.unique_words))


print("\n")
print("Highest percentage of unique words in {0} by {1}, at {2}".format(bt, ba, bp))

end =time.time()
runtime=end-start

print("Run time: " + str(runtime))
print("done")