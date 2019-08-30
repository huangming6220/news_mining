# coding: utf-8

###################################################################
# Step 2-2-1: clean news
###################################################################

# Libraries:
# ==========

import re, time, pandas as pd
from clean_text_basic import clean_text_class

# Functions:
# ==========

# Get news_df from the saved pickle:
####################################
news_name = 'news' # news (for all)
news_fn = 'input/{0}_df.pickle'.format(news_name)
news_df = pd.read_pickle(news_fn)

# Setup special regex dictionaries for collecting unwanted text and cleaning docs:
##################################################################################
special_regex_dict = {\
	# 'parenthesis': re.compile(r'\((.*?)\)'),\
	'parentheses': re.compile(r'\(\((.*?)\)\)'),\
	'brackets': re.compile(r'\[(.*?)\]'),\
	'tags': re.compile(r'<(.*?)>')
}

special_symbol_dict = {\
	# 'parenthesis': ('(', ')'),\
	'parentheses': ('((', '))'),\
	'brackets': ('[', ']'),\
	'tags': ('<', '>')
}

# Clean text of the filtered documents:
#######################################

print('Clean text of the filtered documents')
start_time = time.time()

# Create a clean_text_obj
clean_text_obj = clean_text_class(special_regex_dict, special_symbol_dict)

row_count = 0
clean_docs_arr = []
# Iterate over the news_df to clean it
for each_doc in news_df.iterrows():
	# Print progress or break
	row_count += 1
	if row_count % 1000 == 0:
		print('row_count', row_count, round(row_count / float(len(news_df)), 2) * 100, '%')
		# break
	# Get msg_dt, message and story_text
	primary_index = each_doc[0]
	msg_dt = each_doc[1]['msg_dt']
	message = str(each_doc[1]['message'])
	# story_text = str(each_doc[1]['story'])
	story_text = unicode(str(each_doc[1]['story']), errors='replace').encode('utf-8')
	# Merge message (title) and story_text (article) in the same string
	message_story_text = message + ' ' + story_text
	# if 'top news' in message_story_text:
	# 	print 'has top news:', message_story_text
	# 	continue
	# Clean the message_story_text and append it to the collection
	# message_story_clean = clean_text_obj.second_clean_text(message_story_text)
	message = clean_text_obj.clean_text_basic(message)
	story_text = clean_text_obj.second_clean_text(story_text)
	# remove_meta(story_text)
	# print 'message_story_clean', message_story_clean
	clean_docs_arr.append({\
		'primary_index': primary_index, \
		# 'msg_dt': msg_dt, \
		'message':message, \
		# 'message_story_clean': message_story_clean
		'message_story_clean': story_text
		})

# Store clean documents in a pickle
clean_docs_df = pd.DataFrame(clean_docs_arr)
clean_docs_df.index = clean_docs_df['primary_index']
pickle_path = 'input/{0}_clean.pickle'.format(news_name)
clean_docs_df.to_pickle(pickle_path)

end_time = time.time()
elapsed_time = end_time - start_time
print('elapsed_time', round(elapsed_time / 60.0, 2))
