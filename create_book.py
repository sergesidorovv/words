# functions to make 'Book' object and extract metadata
import os
import subprocess
import zipfile as zf
from lxml import etree

import classes
from shutil import copyfile

# find ./ -name *.epub -exec cp -prv '{}' './epubs/' ';'

def create_book_instance(filename):

	# note: this function will remove spaces from filenames in your epub directory
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
		# we have to pipe the command to bash (i.e. to the terminal) to execute it:
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()

	# start getting the list of words in the book
	all_words=list()
	with open(txt_path, "r", encoding="utf-8") as book:
		for line in book:
			# split on spaces and strip trailing punctuation
			line = line.split(" ")
			words_in_line = [word.strip(".,!?'\t\n").lower() for word in line]
			if words_in_line!=['']:
				all_words.append(words_in_line)		# append the words to our list,
													# unless the line was blank

	# 'all_words' is a list of (sub-)lists. We just want a list of strings
	# [each string being a (non-unqiue) word in the book], so we flatten it 
	# as follows:
	temp=list()
	for sublist in all_words:
	    for item in sublist:
	        temp.append(item)
	all_words=temp

	# remove duplicate words:
	unique_words = set(all_words)

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
	book=classes.Book(book_attributes)

	return book


def get_metadata(fname):
	# Extract as much metadata as we can from the epub file
	# Modified from:
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