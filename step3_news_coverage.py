# -*- coding: utf-8 -*-

###########################################################
# news counts for each category each year
###########################################################

# analysis the number of news at each category in each year
import pandas as pd

newsid_synonyms=pd.read_csv('output/file1_keywords_original_keywords.csv')  #output of solr_indexing_data
print(len(newsid_synonyms))

mesh_keywords=pd.read_excel('input/public_health_mesh_keywords_with_synonyms_sep052018.xlsx') #given by maryam

mesh_keywords.rename(index=str, columns={"mesh_synonym":"synonyms","mesh_keyword":"category"}, inplace=True)
newsid_synonyms.rename(index=str, columns={"disease_query":"synonyms"}, inplace=True)

temp_mesh=mesh_keywords['category'].unique()
print(len(temp_mesh))

newsid_synonyms.drop(['Unnamed: 0'],axis=1, inplace=True)
print(len(newsid_synonyms))

newsid_synonyms.drop_duplicates(inplace=True)
print(len(newsid_synonyms))

mesh_keywords.columns
newsid_synonyms_categories=pd.merge(newsid_synonyms,mesh_keywords[['synonyms', 'category']],how='left',on=["synonyms"])
print(len(newsid_synonyms_categories))

newsid_synonyms_categories.drop_duplicates(inplace=True)
print(len(newsid_synonyms_categories))

##################################################################
selected_news=pd.read_csv('output/file1output.csv')
print(len(selected_news))

newsid_synonyms_categories.columns
newsid_categories_year=pd.merge(newsid_synonyms_categories,selected_news[['doc_idx','year']], how='left', on='doc_idx')

newsid_categories_year=newsid_categories_year[['doc_idx', 'category','year']]
newsid_categories_year=newsid_categories_year.drop_duplicates()

print(len(newsid_categories_year))
newsid_categories_year['unique_news_counts']=1
results=newsid_categories_year.groupby(['category','year'])['unique_news_counts'].count().reset_index()
results_ordered=results.sort_values(by=['category','year'])
results_ordered.to_excel("output/ordered_results.xlsx", index=False)

newsid_categories_counts=results_ordered.groupby('category').agg({'unique_news_counts':'sum'}).reset_index().rename(columns={"unique_news_counts":"counts"}).sort_values(by=['counts']).tail(10)

newsid_categoris_list=newsid_categories_counts.tolist()

