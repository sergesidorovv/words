# functions to make 'Book' object and extract metadata
import os
import subprocess
import zipfile as zf
from lxml import etree

import classes
from shutil import copyfile

# Bash command to pull all epubs out of subdirectories and place in ./epubs
# find ./ -name *.epub -exec cp -prv '{}' './epubs/' ';'

def create_book_instance(filename):

	# remove spaces and full stops from filenames:
	new_filename=filename.replace(" ", "_")
	new_filename=new_filename.replace(".", "-")[:-5] + ".epub"
	
	if filename==new_filename:	# filename already had no spaces or dots in it.
		pass
	else:
		copyfile(filename, new_filename)	# otherwise rename it by copying it and
		os.remove(filename)					# deleting the original
		filename=new_filename
	metadata = get_metadata(filename)		# call the other function defined in this file

	# Use the Calibre program 'ebook-convert' to convert the .epub to .txt:
	txt_path = filename.split(".")[0] + ".txt"
	short_name = filename.split("/")[-1].split(".")[0]
	if not os.path.exists(txt_path):
		print("Converting {}.epub to .txt".format(short_name))
		bashCommand = "ebook-convert {0} {1}".format(filename, txt_path)
		# we have to pipe the command to bash to execute it:
		# (not sure why we need the split but we do)
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()

	# start getting the list of words in the book
	all_words=list()

	# since we will loop over every word, let's create a dictionary at the same time:
	# each key will be a unique word, and we increment the value every time we
	# find that word:

	# key: a unique word; value: number of times word appears in book

	# This is apparently a common technique in natural language processing,
	# called a "bag of words": https://en.wikipedia.org/wiki/Bag-of-words_model
	num_repetitions=dict()
	
	with open(txt_path, "r", encoding="utf-8") as book:
		for line in book:

			# split on spaces and strip trailing punctuation:
			# (this is called tokenization:
			# https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization)

			line = line.split(" ")
			bad_chars = "\"-”’“‘`'.•/*=+,…;:!?—><~()[]}{$#@%"
			for word in line:

				# Strip whitespace and make all characters lowercase				
				word=word.strip().lower()
				
				# strip other unwanted characters:
				word=word.strip(bad_chars)

				# if 'word' is empty after stripping chars, skip to next item in for loop
				if word=='':
					continue
				if len(word)==1 and word!='a' and word!='i':
					continue

				# otherwise, we want to add 'word' to our lists:
				else:
					# ...build our dictionary:
					try:
						# if the word is already a key in our dictionary, increment the value
						num_repetitions[word] += 1
					except KeyError:
						# if 'word' is not already in our dictionary, create an entry (i.e.
						# a key-value pair) for it.
						num_repetitions[word] = 1

					# ...and append the word to our list
					all_words.append(word)

	# remove duplicate words:
	unique_words = set(all_words)

	# find average word length
	total_chars = sum([len(word) for word in all_words])
	ave_word_length = total_chars/len(all_words)


	# gather the attributes and create a 'Book' instance:
	book_attributes=dict()
	for x in ['title', 'author']:
		try:
			book_attributes[x] = metadata[x]
		except KeyError:
			pass

	book_attributes['file_name']=short_name + ".epub"
	book_attributes['total_words']=len(all_words)
	book_attributes['unique_words']=len(unique_words)
	book_attributes['duplicates']=len(all_words)-len(unique_words)
	book_attributes['ave_word_length'] = ave_word_length
	book_attributes['num_repetitions'] = num_repetitions

	# which word appeared most frequently?
	# 'max' takes an iterable as first argument (num_repetitions.keys()). The 'key' argument (different thing to
	# the dictionary keys!) is given by a function which tells max() when a dictionary key should be considered
	# the maximum:
	# namely, when it's associated value is the maximum. This way max will return the dict key, which is what we want
	book_attributes['most_frequent']=max(num_repetitions.keys(), key=(lambda k: num_repetitions[k]))

	book=classes.Book(book_attributes)

	return book


def get_metadata(fname):
	# Extract as much metadata as we can from the epub file. Modified from:
	# https://stackoverflow.com/questions/3114786/python-library-to-extract-epub-information
	with zf.ZipFile(fname, 'r') as zip:

		# I do not really understand these next lines. But i'm not very interested in
		# what they're doing (parsing html etc), so I just copy it from stackexchange
		# and don't worry (except to test that it works correctly)

		# # #

		ns = {
	        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
	        'pkg':'http://www.idpf.org/2007/opf',
	        'dc':'http://purl.org/dc/elements/1.1/'
		}

	    # prepare to read from the .epub file
		zip = zf.ZipFile(fname)

	    # find the contents metafile
		txt = zip.read('META-INF/container.xml')
		tree = etree.fromstring(txt)
		cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

	    # grab the metadata block from the contents metafile
		cf = zip.read(cfname)
		tree = etree.fromstring(cf)
		p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]

		# # #

	    # repackage the data
		res = {}
		dict_keys = ['creator', 'author', 'title', 'description', 'publisher', 'date', 'language', 'identifier']

		# if our epub doesnt' have, say, a "language" field in its metadata,
		# we remove that field from the list dict_keys (with pop) and restart
		# the iteration
		while len(dict_keys) > len(res):
			for i, s in enumerate(dict_keys):
				try:
					res[s] = p.xpath('dc:%s/text()'%(s),namespaces=ns)[0]
				except IndexError:
					dict_keys.pop(i)
					continue

	# this if statement may only work for the particular files I'm looking at
	# (not sure if 'description = <title> / <author>' is common):
	# if (not 'author' in res) and ('description' in res):      
	# 	res['author'] = res['description'].split("/ ")[1]

	if 'creator' in res:
		res['author'] = res['creator']

	return res