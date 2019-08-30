# coding: utf-8

###################################################################
# Step 2-2-1: further clean news
###################################################################

# Libraries:
# ==========

import re
import pandas as pd

# Functions:
# ==========

### clean data
def clean_message_more(msg):
    imsg = True
    if msg.strip():
        # remove heading
        if msg[0] == '*':
            if imsg: print(msg)
            msg = re.sub('\(reuters\) - ', '. ', msg)
            if imsg: print(msg)
        else:
            if re.search('^.*?\(reuters.*?\) -', msg):
                if imsg: print(msg)
                msg = re.sub('^.*?\(reuters.*?\) - ', '', msg)
                if imsg: print(msg)
        if re.search('^\(the following.*?(agency|company)\)', msg):
            msg = re.sub('^\(the following.*?(agency|company)\)', '', msg)
            if imsg: print(msg)

        if re.search('^multimedia versions of reuters', msg):
            if imsg: print(msg)
            msg = re.sub('^multimedia versions of reuters.*top stories \>', '', msg)
            msg = re.sub('page editor:.*\.', '', msg)
            if imsg: print(msg)
        if 'note to subscribers' in msg:
            if imsg: print(msg)
            msg = re.sub('^note to subscribers.*top stories \>', '', msg)
            if imsg: print(msg)
        if 'msg terminated multimedia' in msg:
            if imsg: print(msg)
            msg = re.sub('^msg terminated multimedia.*top stories \>', '', msg)
            if imsg: print(msg)
        if 'click on the codes in brackets' in msg:
            if imsg: print(msg)
            msg = re.sub('click on the codes in brackets.*latest stories > ', '', msg)
            if imsg: print(msg)

        if  'for latest top breaking news across all markets' in msg:
            if imsg: print(msg)
            msg = re.sub('for latest top breaking news across all markets.*$','',msg)
            if imsg: print(msg)
        if  'top news summaries on other subjects' in msg:
            if imsg: print(msg)
            msg = re.sub('top news summaries on other subjects.*$','',msg)
            if imsg: print(msg)
        if re.search('\(?(additonal|additional)?(\s|\()?(report|edit|writ)ing.*by.*$', msg):
            if imsg: print(msg)
            msg = re.sub('\(?(additonal|additional)?(\s|\()?(report|edit|writ)ing by.*$','',msg)
            if imsg: print(msg)
        if re.search('\(for full', msg):
            if imsg: print(msg)
            msg = re.sub('\(for full.*$','',msg)
            if imsg: print(msg)

        # replace
        if ' > ' in msg:
            msg = msg.replace(' > ', '. ')
            if imsg: print(msg)
        if '*' in msg[0]:
            if '*' == msg[0]:
                msg = msg[1:].replace(' * ', '. ')
            else:
                msg = msg.replace(' * ', '. ')
            if imsg: print(msg)
        if ' * ' in msg:
            msg = msg.replace(' * ', '. ')
            msg = msg.replace(":.", ": ")

        # remove tailing
        return msg

# Program:
# ========
news_name = 'news'
news_func = clean_message_more
# input
news_clean_path = 'input/{0}_clean.pickle'.format(news_name)
# output
news_ready_path = 'input/{0}_ready.pickle'.format(news_name)
print(news_name)
print(news_func.__name__)

news_clean_df = pd.read_pickle(news_clean_path)
news_clean_df['message_story_clean'] = news_clean_df['message_story_clean'].apply(lambda x: news_func(x))
news_clean_df.to_pickle(news_ready_path)
news_clean_df.to_excel("input/selected_news.xlsx")
print('news_ready', len(news_clean_df))

# ### test
# msg = """hong kong, jan 3 (reuters) - two international studies of a new drug, telbivudine, have produced potentially good news for hepatitis b patients, showing that it suppresses the virus that damages the liver faster and better than other treatments. chronically infected people are at high risk of death from cirrhosis of the liver and liver cancer, diseases that kill about one million people a year, the world health organisation says. reducing the amount of hepatitis b virus in the blood is critical to limiting the adverse effects of chronic hepatitis b, which affects at least 360 million people and is the 10th leading cause of death worldwide. '(the drug) would actually hopefully help to decrease the number of people who are already suffering from hepatitis b from dying from the disease,' said professor c.l. lai, chair of hepatology at the university of hong kong medical school. hepatitis b is preventable by vaccination, but 25-40 percent of people suffering from chronic infection eventually die of liver cancer or cirrhosis, which is scarring of the liver, lai said. symptoms of hepatitis b, such as jaundice, fatigue, abdominal pain, loss of appetite, nausea and joint pain might not surface in 30 percent of all cases, and they are less common in children. almost all chronic hepatitis b sufferers were infected before they were born or when they were very young and nearly 80 percent are in asia. lai estimated that 10 percent or fewer hepatitis b sufferers worldwide took medication. one study, involving 1,367 hepatitis b patients from 20 countries, compared a group treated with telbivudine to another treated with the drug lamivudine. it showed that telbivudine, produced jointly by novartis ag and idenix pharmaceuticals , reduced the virus more quickly and after 52 weeks, those taking telbivudine achieved 10 times more reduction of the virus per millilitre of blood than those using lamivudine. in addition, a higher percentage of patients in the telbivudine group achieved non-detectable hepatitis b dna level in blood serum than the group taking lamivudine, which is made by galaxosmithklein plc . the results were published in the december issue of the new england journal of medicine. a separate study published in the december issue of annals of internal medicine compared 135 hepatitis b patients from eight countries taking telbivudine or another drug commonly prescribed for hepatitis b, adefovir, or both. again, the telbivudine group had more reduction in mean serum hepatitis b dna virus than that of the adefovir group in early, middle and late stages of the test, results showed. telbivudine was also found to effectively reduce the virus in patients who switched. adefovir is made by gilead sciences inc. (reporting by john ruwitch; editing by david fogarty) keywords: hepatitis drug/ hong kong, jan 3 (reuters) - two international studies of a new drug, telbivudine, have produced potentially good news for hepatitis b patients, showing that it suppresses the virus that damages the liver faster and better than other treatments. chronically infected people are at high risk of death from cirrhosis of the liver and liver cancer, diseases that kill about one million people a year, the world hea",5201, new drug found better at suppressing hep b virus"""
# clean_message_more(msg)
