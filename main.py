# Input: .epub file. Outputs epub metadata, a list of unique words in the book.
import argparse
import sys
import os
import subprocess
import get_metadata as md
import time
import classes

# def create_book_instance(filename):

if len(sys.argv) < 2:
	filename = 'test/1984.epub'
	book_dir = "test/" + filename.split('/')[1].split(".")[0]
	short_name = filename.split('/')[1].split(".")[0]

# we might later want to feed in the filename as an argument when we
# run the script. The code in this block accomplishes that.
else:
	parser=argparse.ArgumentParser(description="description of program",
								   usage="...")
	parser.add_argument("-f", "--filename",
						help="File to open.",
						type=argparse.FileType('r'))
	args = parser.parse_args()


# Get the metadata:
metadata = md.get_metadata(filename)



# Use Calibre to convert .epub to .txt:
txt_path = filename.split('.')[0] + ".txt"
if not os.path.exists(txt_path):
	print("Converting to .txt")
	bashCommand = "ebook-convert test/{0}.epub test/{0}.txt".format(short_name)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

all_words=list()

with open(txt_path, "r") as book:
	for line in book:
		line = line.split(" ")
		words_in_line = [word.strip(".,!?'\t\n").lower() for word in line]
		if words_in_line!=['']:
			all_words.append(words_in_line)

# 'all_words' is a list of (sub-)lists. We just want a list of strings
# [each string being a (non-unqiue) word in the book], so we flatten it 
# as follows:
temp=list()
for sublist in all_words:
    for item in sublist:
        temp.append(item)
all_words=temp
unique_words = set(all_words)

print("Number of words in book:", len(all_words))
print("Number of duplicate words:", len(all_words)-len(unique_words))
print("Number of unique words: ", len(unique_words))

print(metadata.keys())
properties=dict()
for x in ['title', 'author']:
	try:
		properties[x] = metadata[x]
	except KeyError:
		pass
properties['total_words']=len(all_words)
properties['unique_words']=len(unique_words)

book=classes.Book(properties)
print(book.unique_words, book.total_words)

end = time.time()
print("Build time: ", end-start)
print("done")
