# a single book
class Book(object):
	def __init__(self, props):
		try:
			self.title = props['title']
		except KeyError:
			self.title = "Unknown"
		try:
			self.author = props['author']
		except KeyError:
			self.author = "Unknown"
		self.file_name=props['file_name']
		self.total_words = props['total_words']
		self.unique_words = props['unique_words']
		self.duplicates = props['duplicates']
		self.ave_word_length = props['ave_word_length']
		self.most_frequent = props['most_frequent']
		self.num_repetitions = props['num_repetitions']


# a collection of books
class Bookshelf(object):
	def __init__(self):
		self.num_books = 0
		self.total_words = 0
		self.ave_word_length = 0
		self.ave_words_per_book = 0

		# dictionary of all words, with val=number of occurences in bookshelf
		self.num_repetitions = dict()
		self.unique_words=0

	def add_book_data(self, book):
		self.num_books = self.num_books + 1
		total_chars = self.total_words*self.ave_word_length + book.total_words*book.ave_word_length	
		self.total_words += book.total_words
		self.ave_word_length = total_chars/book.total_words
		self.ave_words_per_book = self.total_words/self.num_books
	
		# print(book.num_repetitions.keys())
		for word in book.num_repetitions.keys():
			try:
				self.num_repetitions[word] += book.num_repetitions[word]
			except KeyError:
				self.num_repetitions[word] = book.num_repetitions[word]

		self.unique_words=len(self.num_repetitions)
		

	# returns a tuple of length n:
	# most_frequent = ((number of occurences, 'word'), ...)
	# ordered by number of occurences (large to small)
	def n_most_frequent_words(self, n):
		most_frequent = tuple()
		most_frequent = sorted([(value, key) for (key,value) in self.num_repetitions.items()], reverse=True)
		return most_frequent[:n]

	def n_least_frequent_words(self, n):
		most_frequent = tuple()
		most_frequent = sorted([(value, key) for (key,value) in self.num_repetitions.items()], reverse=False)
		return most_frequent[:n]