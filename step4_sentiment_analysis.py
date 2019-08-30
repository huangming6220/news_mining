# -*- coding: utf-8 -*-

###################################################################
# For selected news by solar we are going to do sentiment analysis
###################################################################

############################################
# import section
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import sent_tokenize
import numpy as np

from functions import  stem_string

##############################################
# search a given text for the given phrases, and returns the sentences which have any of the phrases (target_text)
# trash_text contains the sentences without given phrases
def search_for_phrases(text, phrases, target_text):
    sent=sent_tokenize(text)
    trash_text=""
    
    for s in sent:
          flag=0     
          for phrase in phrases: # if we can find either of the synonyms in the sentence, flag would be 1 and 0 otherwise
              if s.lower().find(phrase.lower())!=-1:
                  flag=1
                  break
          if flag==1:
              target_text=target_text+" "+s
          else :
              trash_text=trash_text+" "+s
    return trash_text,target_text        
    

############################################## 
# For a given text and list of synonyms, the score is the average of sentiments of the sentenses which include the synonyms
# The below function returns the sentiment of a given text for its sentences that includes the given synonyms 
def sentiment_text(text, synonyms):
    analyzer = SentimentIntensityAnalyzer()
    scores=[]  # stores the scores  of text sentences
    
    stem_synonyms=[]  #  to store stemmed synonyms
    lemma_synonyms=[]  # to store lemmatized synonyms
    
    # ge the stemmed and lemmatized synonyms
    for synonym in synonyms:
         stem_synonym, lemma_synonym=stem_string(synonym)
         stem_synonyms.append(stem_synonym)
         lemma_synonyms.append(lemma_synonym)
#    print(stem_synonyms)
#    print(lemma_synonyms)
   
    trash_text, target_text=search_for_phrases(text,synonyms, "")
#    print(trash_text,target_text)
    
    stem_text, lemma_text=stem_string(trash_text)  
    trash_text, target_text=search_for_phrases(stem_text,stem_synonyms,target_text)
#    print(trash_text,target_text)
#    
    stem_text, lemma_text=stem_string(trash_text)
    trash_text, target_text=search_for_phrases(lemma_text,lemma_synonyms,target_text)
#    print(trash_text,target_text)
    
    # Calculate the sentiment, just for the target sentences 
    sents =sent_tokenize(target_text)
    for s in sents:
            sentiment=analyzer.polarity_scores(s)
            scores.append(sentiment['compound'])
            
#    print("target text: "+target_text)    
#   print("trash text: "+trash_text)     
    
#    print("scores")
#    print(scores)
   
    return(np.std(scores), np.mean(scores),len(scores)) 


##############################################
    
# =============================================================================
#                        Main section of program    
# =============================================================================
newsid_categories_year=pd.read_excel("output/final_selected_news_by_upcategories.xlsx")  #input: from mergeI
newsid_categories_year.columns
print(len(newsid_categories_year))
#22966 categories

# get the news with their  synonyms 
news_synonyms=pd.read_excel("output/after_solr_all_selected_news_with_synonyms_and_categories.xlsx") # input: 
news_synonyms.columns
print(len(news_synonyms))
#442701

# get the list of unique categories of the news
categories=news_synonyms['category'].unique()
print(len(categories))
#92

news_sentiments=pd.DataFrame()

for category in categories: 
    temp_news= newsid_categories_year[newsid_categories_year['category']==category] # for each specific category
    print(category)       
    for index , row in temp_news.iterrows():
        
    synonyms_for_a_news=news_synonyms[ (news_synonyms['doc_idx']== row['doc_idx']) &           # get the assinged synonyms for each news at each category
                                      (news_synonyms['category']==category)]['synonyms']

    std, mean, sentences_count= sentiment_text(row['text'],synonyms_for_a_news)
    temp_news.at[index,'sentiment']=mean
    temp_news.at[index,'sentiment_std']=std
    temp_news.at[index,'sentiment_counts']=sentences_count
     
    if mean>=0.05:
        temp_news.at[index,'sentiment_flag']=1   # positive sentiment
    elif mean<=-0.05:
        temp_news.at[index,'sentiment_flag']=-1 # negative sentiment
    else :
        temp_news.at[index,'sentiment_flag']=0 # neutral sentiment  
                              
    temp_news.to_excel("output/sentiments/"+category+"_sentiment.xlsx"  )   
    news_sentiments=news_sentiments.append(temp_news)                   
    if len(temp_news[temp_news['sentiment_counts']==0])>0 :
        print("Errors *******check your output files for the texts without any found synonyms :"+ category)
        
         
################################################################################    
missing_sentiment=news_sentiments[news_sentiments['sentiment_counts']==0]   
print(len(missing_sentiment))       
#1357

print(len(news_sentiments))
#226966    

results2=news_sentiments[news_sentiments['sentiment_counts']!=0]       
results=results2.groupby(['category','year', 'sentiment_flag']).agg({"doc_idx":"count"}).reset_index().rename(columns={"doc_idx":"counts"}).sort_values(by=['category','year'])
results.to_excel("output/sentiments/sentiment_results.xlsx", index=False)
results2.to_excel("output/sentiments/sentiment_raw_results.xlsx", index=False   )

# attentine to run or skip below line
results2=pd.read_excel("output/sentiments/sentiment_raw_results.xlsx" )
print(len(results2))
#225609

result3=results2.groupby (['category','year']).agg({"sentiment":"mean","doc_idx":"count"}).reset_index().rename(columns={"sentiment":"sentiment_mean","doc_idx":"News_counts"}).sort_values(by=['category','year'])
result4=results2.groupby (['category','year']).agg({"sentiment":"std"}).reset_index().rename(columns={"sentiment":"sentiment_std"}).sort_values(by=['category','year'])
result5=pd.merge(result3,result4, how='outer', on=['category','year'])
result5.to_csv("output/sentiments/sentiment_summary_results.csv", index=False)
