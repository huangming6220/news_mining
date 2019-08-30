# -*- coding: utf-8 -*-

######################################################################################################################################
# This program assigns a doc_idx to each news.
# We also creates one file that the text of the news are stemmed and in the other the text of the news are lammetaized.
# Selected news (i.e., news in the health related fields), would be changed in the correct format to use in the solr_import_data.py. 
######################################################################################################################################

import pandas as pd
from functions import add_stem

# input
#input file and should have a column message_story which will be imported  ** for original news 
inpfile = "input/selected_news.xlsx"
#outfile = "output/selected_news_original_with_doc_idx.xlsx"
outfile0 = "output/selected_news_before_solr_stem_lemma.xlsx"
#outfile1 = "input/selected_news_lemmatized.xlsx"
#outfile2 = "input/selected_news_stemmed.xlsx"
outfile = "output/selected_news_original_with_doc_idx.xlsx" #input for original news
outfile1 = "output/selected_news_stemmed_with_doc_idx.xlsx" #input for stemmed news 
outfile2 = "output/selected_news_lemmatized_with_doc_idx.xlsx" #input for lemmatized news
    
# to add doc_idx to the health related news
pa_df = pd.read_excel(inpfile)
pa_df=pa_df.reset_index(drop=True)
pa_df=pa_df.reset_index()
pa_df.rename(index=str, columns={"index":"doc_idx", "message_story":"text"},inplace=True)
pa_df.to_excel(outfile, index=False)  # output for original news

# stem and lemmatize the news text and save the file
pa_df_stem_lemma=add_stem(pa_df, "text")
pa_df_stem_lemma.toexel(outfile0, index=False)

pa_df_lemma=pa_df_stem_lemma.rename(index=str, columns={"text":"original_text"})
pa_df_lemma.rename(index=str, columns={"lemma_text":"text"}, inplace=True)
pa_df_lemma=pa_df_lemma.drop(['stem_text','original_text'], axis=1) 
pa_df_lemma.to_excel(outfile1, index=False)    

pa_df_stem=pa_df_stem_lemma.rename(index=str, columns={"text":"original_text"})
pa_df_stem.rename(index=str, columns={"stem_text":"text"}, inplace=True)
pa_df_stem=pa_df_stem.drop(['lemma_text','original_text'], axis=1) 
pa_df_stem.to_excel(outfile2, index=False)    
