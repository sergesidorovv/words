# Input: .epub file. Output: 'Book' object with the following attibutes:
# 'title', 'author', total_words', 'unique_words', 'duplicates'

import argparse, sys
import create_book as cb
import glob


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
for filename in glob.glob("test/*.epub"):

	book = cb.create_book_instance(filename)
	print("\n")
	print("Book title: " + book.title)
	print("Author: " + book.author)
	print("Length: " + str(book.total_words) + " words")
	print("Number of unique words: {}".format(book.unique_words))