import re 		# start by loading a package we will be using, regular expressions


# Our first goal is to create a list of all of the words in the book. We should
# try to remove punctuation (and probably capitalisation) so we just have the words.
# We would end up with something like

list_of_words = ['call', 'me', 'ishmael', 'when'] # etc. (many more entries in the list)

# ^ this is one way to create a 'list' data structure in python. You can initialise an
# empty list with:
# list_name = [] # or
# list_name = list()

# then we can access a word like this:

print(list_of_words[2])    # prints 'ishmael'.
						   # python indexing starts at 0, so list_of_words[0]
						   # selects the first element in the list ('call')

# Instead of a whole book, let's start with a test:

test_string= "Maxfield's housemate told the ABC he reported him to police for keeping a \
handgun in their home. He said officers arrived and seized the gun, \
less than 48-hours before Maxfield killed Mr Martin."


# FIRST PASS
#################

# Try to remove the punctuation:
cleaned_string = re.sub('[^\w\d\s]+', '', test_string)

# this says: look in test_string and find anything that is NOT (^): a word character (\w),
# a number (\d) or a whitespace character (\s), then replace it with '' (i.e. with no
# character, i.e. delete it.). Real expressions (the "re" package) is a way to search for
# and match strings. E.g. say you wanted to find an email address in a block of text,
# you could say: "find me any number of letters or numbers, followed by @, followed by
# letters or numbers, followed by dot, (etc)".

# this is not the way I would immediately think to do this but it would work.
# ^\w\d\s might be a bit heavy handed, because we may want to keep hyphens
# between words and possessive apostrophes. We probably want to keep "'" and "-" when
# they are immediately preceded and followed by a \w or \d character.
# There might be some other edge cases we haven't thought about yet to code in as well.

print(test_string + '\n')
print("First attempt at stripping unwanted characters:\n")
print(cleaned_string)		# looks okay. I think using regular expressions is a bit
							# awkward though. There's probably an easier way.

# TAKE 2
##########################

# A better way might be to split the string into its component words, THEN clean the
# punctuation. That way we can just use the rule: "remove an apostrophe if it comes at
# the end of a word, otherwise keep it":

list_of_words = test_string.split(" ")  # split the string on every space (" ") and return a list
										# of all of the words
									 	# we're overwriting our old list_of_words object here
print('\nList of words with trailing punctuation:\n')
print(list_of_words)

print('\nLoop through the words in our list:\n')
for i, word in enumerate(list_of_words):  	# loop through the list
	print(i, word)							# i is a counter, word is an element in the list
	clean_word = word.strip(".,-'!?")		# Remove . , - or ' etc if it comes at the end
											# of 'word'. There's probably other punctuation
											# or whitespace characters to remove here?										
	clean_word = clean_word.lower()			# Make it all lower case
	list_of_words[i] = clean_word			# replace 'word' in our new list with 'clean_word'
	print(clean_word)

# A more compact way to do this would be:

# list_of_words = [word.strip(",.-'").lower() for word in list_of_words]

# which is called a list comprehension. But let's keep the code fairly explicit for now
# so that it's easier to interpret.

print('\nList of words without trailing punctuation:\n')
print(list_of_words) 		# This is is better than the previous approach using re,
							# because we deal with the edge cases more naturally.

# now we want to remove duplicates. To do this, we convert our list to a different
# data type: a set. Sets are like lists but contain only unique elements. By converting
# to a set, python will remove the duplicates for us.
# Note that sets are unordered, so it might return the words in a different order.
# But I don't think we need it to be ordered so this should be okay.

unique_words = set(list_of_words)
print("\nUnique words:\n")
print(unique_words)

# how many duplicates did we have?
print("\nNumber of duplicates removed:\n")
print(len(list_of_words)-len(unique_words))

# the other thing we might want to do here is work out how many times each
# duplicate word is repeated.

# i think that's it. Next we want to try it on a real book.
# You can take over here. Below I'll give some hints for how to do various
# things and some rough ideas on the structure of one possible program. Read the rest of this file
# before you start.

# We need to open the book then iterate over each line in it.
# you can do something like:

# filename = "path/to/book.epub"	# need quotation marks (to make it a string)

# book = open(filename) 			# This is what you would do for a .txt file, 
									# but actually I'm not sure if you can just
									# read in an epub like this. You might need
									# to look it up. You will possibly need to
									# install a package.

# Later: i have tried this and actually reading in the epub is a bit harder 
# than I thought. In the end I chose to pipe a command to the terminal which calls
# calibre. calibre has a nice function "ebook-convert" which converts epub to txt
# so that we can just read it in in a simple way.
# There are other soutions but these seemed easiest. If you can't work out how
# to convert epub -> text, look at how I do it in the file "create_book.py"
# after the comment "# Use the Calibre program..."


# Once you've opened the text file
# you loop through the lines of text in the book:

# for line in book:
#	/do stuff like splitting and stripping the text, adding to lists etc/
# book.close()		# remember to close the file once you have extracted the 
					# words in a list (or set) so it doesn't keep using your ram.
					# important if you're going to loop over 100s of books.


# if you want to loop through all the epubs in a directory, check out the
# "glob.glob" command: https://docs.python.org/3/library/glob.html
# (learning to read the documentation is quite important)
# then you just wrap all the code you have for a single epub in another big for loop
# where you loop over the different books:

# for epub in <some glob command which lists all epubs in a folder>:	# outer loop

	# < read in epub somehow as "book" >

	# for line in book:		# inner loop
	#	< do stuff>
	# book.close()

# if you're not sure how a command works, just type python3 in a terminal
# and try it out. E.g. you could (start python3 and) type

# import glob
# glob.glob("./*") # or
# glob.glob("./*.epub")

# What type of object does "glob.glob" return? you could check with
# type(glob.glob("./*"))

# just start very simple and build it up slowly, and
# always go back to very simple toy examples if something isn't behaving the way you
# expect.

# once we have a list of all unique words for various books,
# we can start thinking about doing statistics.