
import sys, re, operator, pandas as pd
from collections import defaultdict
from nltk.corpus import stopwords

# self.repeated_chars = re.compile(r'([-.,\s\=])\1+')
# self.bad_chars = re.compile(r'[\*\\=\-\@\#\!\&\^\%\|]')
# self.dash_chars = re.compile(r' -')
# self.dot_chars = re.compile(r' \.')
# message_story_text = self.dash_chars.sub(' ', message_story_text)
# message_story_text = self.dot_chars.sub(' ', message_story_text)

# List of bad characters to remove: ' *', ' |', '+', ':', ';'
class clean_text_class(object):
	"""clean_text_class"""
	def __init__(self, *args):
		self.top_special_words_dict = {}
		self.repeated_chars = re.compile(r'([.,\s\*\\=\-\@\#\!\&\^\%\|])\1+')
		self.dash_chars = re.compile(r' -')
		self.dot_chars = re.compile(r' \.')
		self.alphanumeric = re.compile('[a-zA-Z\d\s:]')
		self.nonalphanumeric = re.compile('[^a-zA-Z\d\s:,]')
		self.disease_cui_df, self.cui_icd9_df, self.icd9_phewas_df, self.phewas_stdname_fn = get_disease_df()
		if len(args) == 0:
			# print 'Using default function clean_text_basic only'
			pass
		elif len(args) == 2:
			self.special_regex_dict = args[0]
			self.special_symbol_dict = args[1]
		else:
			print 'Unexpected use of clean_text_class!!'

	def clean_text_basic(self, message_story_text):
		# Remove leading and trailing spaces and newlines
		message_story_text = str(message_story_text).strip().rstrip()
		# Remove repeated space, full-stops and dashes
		message_story_text = self.repeated_chars.sub(r'\1', message_story_text)
		# message_story_text = self.dash_chars.sub(' ', message_story_text)
		# message_story_text = self.dot_chars.sub(' ', message_story_text)
		# message_story_text = self.bad_chars.sub(' ', message_story_text)
		# Lower case the document
		message_story_text = unicode(str(message_story_text), errors='ignore').lower()
		return message_story_text

	def second_clean_text(self, message_story_text):
		# Basic cleaning for the text first
		message_story_text = self.clean_text_basic(message_story_text)
		# For each special_regex
		for special_regex in self.special_regex_dict:
			# Get symbols
			special_symbols = self.special_symbol_dict[special_regex]
			# Get text between special_regex
			special_regex_str = self.special_regex_dict[special_regex]
			all_between_special_regex = special_regex_str.findall(message_story_text)
			# Get the bad sentences which needs to be removed
			for special_sentence in all_between_special_regex:
				# If special_sentence has more than 250 chars then keep
				if len(special_sentence) > 300:
					continue
				bad_sentence = special_symbols[0] + special_sentence + special_symbols[1]
				message_story_text = message_story_text.replace(bad_sentence, ' ')
		# Another basic clean to get rid of repeated spaces and full-stops
		message_story_text = self.clean_text_basic(message_story_text)
		return message_story_text
