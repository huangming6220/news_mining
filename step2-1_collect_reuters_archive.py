# coding: utf-8

######################################################
# download news articles from Reuters Archive website
######################################################

# Libraries:
# ==========

import sys, os, requests, time, pandas as pd
from datetime import timedelta, datetime, date
from bs4 import BeautifulSoup

# Functions:
# ==========
from get_article_content_archive import get_article_content

def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)+1):
		yield start_date + timedelta(n)

# Program:
# ========

# parameters
nation = sys.argv[1] # us, uk, in
first_date = sys.argv[2] # yyyymmdd eg. 20160101
last_date = sys.argv[3] # yyyymmdd eg. 20161231


print('nation: {0} first date: {1} last date: {2}'.format(nation, first_date, last_date))

start_date = datetime.strptime(first_date, '%Y%m%d').date()
end_date = datetime.strptime(last_date, '%Y%m%d').date()

start_time = time.time()

# Set reuters_health_news dir path
reuters_health_news_path ='News_data'
pickle_path = reuters_health_news_path + '{0}-{1}_{2}_reuters_archive.pickle'.format(first_date,last_date,nation)
if not os.path.exists(pickle_path):
	# make the empty pickle to be filled
	reuters_health_news_df = pd.DataFrame(columns=['msg_dt', 'message_header', 'message_story', 'msg_tag', 'msg_topic', 'msg_subtopic', 'web_dt'])
	reuters_health_news_df.to_pickle(pickle_path)
else:
	# Get the existing pickle to be appended
	reuters_health_news_df = pd.read_pickle(pickle_path)
	if len(reuters_health_news_df) > 0:
		dt_obj = datetime.strptime(reuters_health_news_df.web_dt.values[-1].strip(), '%Y%m%d')
		start_date = dt_obj.date()+timedelta(1)

print('start_page', start_date.strftime('%Y%m%d'))

# us uk in, ca af
# http://www.reuters.com/resources/archive/us/2016.html
# http://www.reuters.com/resources/archive/uk/2016.html
# http://www.reuters.com/resources/archive/in/2016.html

# http://www.reuters.com/resources/archive/us/20160128.html
# http://www.reuters.com/article/us-neos-fda-idUSKCN0V60AT
# http://www.reuters.com/article/southkorea-soil-idUSL3N15C194

# Root link for all articles and pages
root_link = 'http://www.reuters.com/'
archive_link = root_link + 'resources/archive/{0}/'.format(nation)
article_prefix = 'http://www.reuters.com/article/'

# Page range
articles_arr = []
sleep_time = 10

num_article_year = 0
for single_date in daterange(start_date, end_date):
	date_str = single_date.strftime('%Y%m%d')
	page_link = archive_link + date_str + '.html'
	print('page_link', page_link)
	# Get request object from the page link
	requests_obj = requests.get(page_link)
	# Get page content from the request object
	content_obj = requests_obj.content
	# Parse the HTML from the content using BeautifulSoup
	soup = BeautifulSoup(content_obj, 'html.parser')
	# Find all divs with class story-content
	headlineMed_div = soup.findAll('div', { 'class' : 'headlineMed' })
	# For each div get the href link for the articles to be parsed
	num_article_page = 0
	for each_div in headlineMed_div:
		# Get the article using the link
		article_link = each_div.find('a')['href']
		print(article_link)

#get article title 

		article_title = each_div.get_text()
		print("article title is", article_title)
		
		if "Following Is a Test Release" in article_title:
			continue


		if 'pictures-report' in article_link:
			continue
		elif 'videoStory' in article_link:
			continue
		num_article_page += 1
		#print 'article_link', article_link

		successful = False
		num_trial = 0
		while not successful and num_trial < 1:
			try:
				article_record, article_year = get_article_content(article_link)
				successful = True
				# print 'successful', successful
			except Exception, exception:
				successful = False
				num_trial += 1
				print('exception', exception)
				print('successful', successful)
				print('article_link', article_link)
				print('sleeping for', sleep_time, 'seconds')
				time.sleep(sleep_time)

			

		# Append article record to the array
		if not article_record:
			continue
		# print(article_record)
		articles_arr.append(article_record+[date_str])

	# Save the record into a pickle every day since the number of articles each day is different
	# Create DataFrame from the articles_arr
	articles_df = pd.DataFrame(articles_arr, columns=['msg_dt', 'message_header', 'message_story', 'msg_tag', 'msg_topic', 'msg_subtopic', 'web_dt'])
	# Join old and new DataFrames
	frames_arr = [reuters_health_news_df, articles_df]
	reuters_health_news_df = pd.concat(frames_arr)
	print('length of reuters_health_news_df', len(reuters_health_news_df))
	# Save in pickle
	reuters_health_news_df.to_pickle(pickle_path)
	# Reset articles array
	articles_arr = []
	print('num_article_date', num_article_page)
	num_article_year += num_article_page
print('num_article_year', num_article_year)

# # # Create DataFrame from the articles_arr
# # articles_df = pd.DataFrame(articles_arr, columns=['msg_dt', 'message_story'])
# # print 'articles_df', articles_df
# # # Save in pickle
# # articles_df.to_pickle(reuters_health_news_path\
# # + str(prev_year) + '_reuters_health_news.pickle')

end_time = time.time()
elapsed_time = end_time - start_time
print('elapsed_time', elapsed_time)
