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

		self.total_words = props['total_words']
		self.unique_words = props['unique_words']
		self.duplicates = props['duplicates']