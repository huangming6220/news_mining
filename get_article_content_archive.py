# http://IN.reuters.com/article/turkey-erdogan-hitler-idINKBN0UF1XU20160101
# there are many stories in the page and we only get the first one
# date, story, tag, or nation

import requests, re
from bs4 import BeautifulSoup

repeated_chars = re.compile(r'([.,\s\*\\=\-\@\#\!\&\^\%\|])\1+')

def get_article_content(article_link):
	# Get request object from the page link
	requests_obj = requests.get(article_link)
	# Get page content from the request object
	content_obj = requests_obj.content
	# Parse the HTML from the content using BeautifulSoup
	soup = BeautifulSoup(content_obj, 'html.parser')
	#print soup.contents
	# Get the tag
	article_tag_field = soup.findAll('div', { 'class' : 'channel_4KD-f' })
	article_tag = article_tag_field[0].getText().replace('#','')
	print 'article tag :', article_tag
	# Get the topic
	article_topic_field = soup.findAll('meta', { 'name' : 'analyticsAttributes.topicChannel' })
	article_topic = article_topic_field[0]['content'].encode('utf-8')
	# Get the subtopic
	print 'article topic :', article_topic
	article_subtopic_field = soup.findAll('meta', { 'name' : 'analyticsAttributes.topicSubChannel' })
	article_subtopic = article_subtopic_field[0]['content'].encode('utf-8')
	print 'article subtopic : ', article_subtopic
	# Get the date
	article_header_date = soup.findAll('div', { 'class' : 'date_V9eGk' })
	try:
		article_date = article_header_date[0].getText().split('/')[0]
	except Exception, exception:
		print 'soup', soup
	article_time = article_header_date[0].getText().split('/')[1]
	article_date_time = article_date + article_time
	article_year = int(article_date.split(', ')[1])
	# print 'article_date_time', article_date_time
	# print 'article_year', article_year

	# Find all divs with class story-content
	article_header = soup.findAll('h1', { 'class' : 'headline_2zdFM' })[0].text
	# print 'article_header', article_header
	article_body = soup.findAll('div', { 'class' : 'body_1gnLA' })
	# Get all p tags in the article body, to avoid images, tables, etc...
	paragraphs = article_body[0].findAll('p')
	# Iterate on the paragraphs to join in on string and avoid reporter and writer info
	article_arr = []
	for each_par in paragraphs:
		if each_par.has_attr("class"):
			if each_par.get("class")[0] == 'Attribution_content_27_rw':
				continue
		# Append paragraph to the array
		article_arr.append(each_par.getText())
	# Join article array into one string
	article_header = article_header.encode('ascii','ignore')
	article_str = ' '.join(article_arr).encode('ascii','ignore')
	article_header = repeated_chars.sub(r'\1', article_header).lower()
	article_str = repeated_chars.sub(r'\1', article_str).lower()

	article_str = article_header + ' ' + ' '.join(article_arr)
	# Remove unicode from text
	article_str = article_str.encode('ascii', 'ignore')
	# Remove repeated spaces, punctuation and other meaningless characters
	# And lower case all string
	article_str = repeated_chars.sub(r'\1', article_str).lower()
	# print 'article_str', article_str
	# article_record = [article_date_time, article_str, article_tag]
	article_record = [article_date_time, article_header, article_str, article_tag, article_topic, article_subtopic]
	# print 'article_record', article_record
	# print
	return article_record, article_year

if  __name__=="__main__":
	article_link = 'https://www.reuters.com/article/us-frutarom-inds-algae/frutarom-invests-in-algae-startup-for-food-cosmetic-products-idUSKBN0UI0P520160104'
	article_record, article_year = get_article_content(article_link)
	print article_record
	print article_year
