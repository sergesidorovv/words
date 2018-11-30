# Input: .epub file. Output: 'Book' object with the following attibutes:
# 'title', 'author', total_words', 'unique_words', 'duplicates'

import argparse, sys
import create_book as cb
import glob
import time
import classes

start = time.time()

# could be good https://en.wikipedia.org/wiki/Cloud_Atlas_(novel)

# # #

# To include:

# - compute average word length 	done
# - number of times each word appears in book 	done
# - Create set of 1000 most common words 	done

# - compute average sentence length
# - check word in common_words for every word in book,
#	and find % which are uncommon.
#	seems like word in set should be fast enough:
#	https://stackoverflow.com/questions/5993621/fastest-way-to-search-a-list-in-python
# - characterise book complexity based on number (or %) of unique words,
#	average word length, % words which are uncommon etc.
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
# path = "/main_1TB/Downloads/all_epubs"
path = "/Users/Jack/Dropbox/other/all_epubs"
# with open("summary.txt", "a") as myfile:

bp = 0.
bt = 'Unknown'
ba = 'Unknown'

bookshelf=classes.Bookshelf()
for filename in glob.glob(path + "/*.epub"):

	book = cb.create_book_instance(filename)
	bookshelf.add_book_data(book)
	if bookshelf.num_books%10==0:
		print(bookshelf.num_books)
	# print(bookshelf.total_words)
	# print("\n")
	# print("Title: " + book.title)
	# print("Average word length: " + str(book.ave_word_length) + "\n")
	# print("Author: " + book.author)
	# print("Length: " + str(book.total_words) + " words")
	# print("Number of unique words: {}".format(book.unique_words))
	# print("Most frequent: {}".format(book.most_frequent))

	# myfile.write("Title: " + book.title + "\nAuthor: " + book.author \
	# 	+ "\nLength: " + str(book.total_words) + " words" + \
	# 	"\nNumber of unique words: {}".format(book.unique_words) + \
	# 	"\nPercentage unique: {:.1f}%".format(100*book.unique_words/book.total_words))
	# myfile.write("\n\n")

	# print(filename)

	# if 100*book.unique_words/book.total_words > bp:
	# 	bp = 100*book.unique_words/book.total_words
	# 	bt = book.title
	# 	ba = book.author

	# if book.most_frequent!='the':
	# 	print(book.title)
	# 	print(book.most_frequent)

n=1000
most_frequent = bookshelf.n_least_frequent_words(n)

with open("bookshelf_least.txt", "w") as myfile:
	# myfile.write(	"Number of books: " + str(bookshelf.num_books) + \
	# 				"\nAverage book length: {:.2f} words".format(bookshelf.ave_words_per_book) + \
	# 				"\nTotal length: " + str(bookshelf.total_words) + " words" + \
	# 				"\nUnique words: " + str(bookshelf.unique_words)
				# )
	myfile.write("~~~~\nThe {} least frequent words:\n~~~~\n".format(n))

	# print(most_frequent)
	myfile.write("\nRank\t\\ttWord\t\t\tNumber of occurences\n\n")
	for i, pair in enumerate(most_frequent): 
		# print("{0}.\t\t\t{1}\t\t\t{2}\n".format(i+1, pair[1], pair[0])	)
		# myfile.write(pair[1] + " " + str(len(pair[1]))+"\n")
		myfile.write("{0}.\t\t\t{1}\t\t\t{2}\n".format(i+1, pair[1], pair[0]))

# print(most_frequent[5])
# print(most_frequent)
end =time.time()
runtime=end-start
print("Run time: {:.2f}s".format(runtime))
print("done")