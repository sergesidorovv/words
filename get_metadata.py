# Input: .epub file. Outputs epub metadata, a list of unique words, number
# of times each unique word occurs in the file.

import zipfile as zf
from lxml import etree


def get_metadata(fname):
	# Modified from:
	# https://stackoverflow.com/questions/3114786/python-library-to-extract-epub-information
	with zf.ZipFile(fname, 'r') as zip:
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

	    # repackage the data
		res = {}
		dict_keys = ['creator', 'title', 'description', 'publisher', 'date', 'language', 'identifier']

		# if our epub doesnt' have, say, a "language" field in its metadata,
		# we remove thatfield  from the list dict_keys (with pop) and restart
		# the iteration

		while len(dict_keys) > len(res):
			for i, s in enumerate(dict_keys):
				try:
					res[s] = p.xpath('dc:%s/text()'%(s),namespaces=ns)[0]
				except IndexError:
					dict_keys.pop(i)
					continue
	# this might only be true for the files I'm looking at:
	if (not 'author' in res) and ('description' in res):      
		res['author'] = res['description'].split("/ ")[1]

	return res