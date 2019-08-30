# -*- coding: utf-8 -*-

###########################################################################
# we have searched for keywords in the original news
#                 for stemmed keywords in the stemmed news
#                 for lemmatized keywords int the lemmatized news
#                now, want to merge all the results to see whats happening
###########################################################################

import pandas as pd
import numpy as np
from functions import  add_stem

newsid_synonyms_origin=pd.read_csv('output/file1_keywords_original_keywords.csv')  #input: output of solr_indexing_data
print(len(newsid_synonyms_origin))
#287199

newsid_synonyms_stem=pd.read_csv('output/file1_keywords_stemmed_keywords.csv')  #input: output of solr_indexing_data
print(len(newsid_synonyms_stem))
#639888

newsid_synonyms_lemma=pd.read_csv('output/file1_keywords_lemmatized_keywords.csv')  # input: output of solr_indexing_data
print(len(newsid_synonyms_lemma))
#484864

newsid_synonyms=newsid_synonyms_origin.copy()
newsid_synonyms=newsid_synonyms.append(newsid_synonyms_stem)
newsid_synonyms=newsid_synonyms.append(newsid_synonyms_lemma)
newsid_synonyms=newsid_synonyms.drop_duplicates()
print(len(newsid_synonyms))
#514806

newsid_synonyms.rename(index=str, columns={"disease_query":"synonyms"}, inplace=True)



####################################################
selected_news_origin=pd.read_csv('output/file1output_origin_news.csv') #input:  output of solr_indexing_data
print(len(selected_news_origin))
#81003

selected_news_stem=pd.read_csv('output/file1output_stemmed_news.csv')  #input:  output of solr_indexing_data
print(len(selected_news_stem))
#104489

selected_news_lemma=pd.read_csv('output/file1output_lemmatized_news.csv')  #input:  output of solr_indexing_data
selected_news_lemma.columns
print(len(selected_news_lemma))
#94512

selected_news=selected_news_origin.copy()
selected_news=selected_news.append(selected_news_stem, sort=True)
selected_news=selected_news.append(selected_news_lemma, sort=True)
selected_news.drop('text', axis=1, inplace=True)
selected_news=selected_news.drop_duplicates()
print(len(selected_news))
#104912

####
#add the text of the news from original text

# read the original news
news=pd.read_excel("output/selected_news_original_with_doc_idx.xlsx")  # output of before solr program
print(len(news))
#199230

temp_selected_news= pd.merge(selected_news,news[["text", "doc_idx"]], how="left", on='doc_idx')
temp_selected_news.sort_values(by=['doc_idx'], inplace=True)
print(len(temp_selected_news))
#104912
selected_news=temp_selected_news.copy()
print(len(selected_news))
#104912


#Did you see any changes in the number of News selected before and after “lemmatizing and stemming” ?
origin_doc_idx=selected_news_origin[['doc_idx']].drop_duplicates()
stem_doc_idx=selected_news_stem[['doc_idx']].drop_duplicates()
lemma_doc_idx=selected_news_lemma[['doc_idx']].drop_duplicates()
print(len(origin_doc_idx))
#81003
print(len(stem_doc_idx))
#104489
print(len(lemma_doc_idx))
#94512



#########################################################################
## From selected news exclude those with the given tags
#tags_to_delete=pd.read_excel("input/list of health related tags_to_delete.xlsx")
#print(len(tags_to_delete))
##8
#selected_news_final=selected_news[~selected_news["trimmed_tag"].isin(tags_to_delete["Tags"])]
#print(len(selected_news_final))
##82091

##########################################################################
# Add category to each assigned synonyms
mesh_keywords1=pd.read_excel('input/public_health_mesh_keywords_with_synonyms_sep052018.xlsx') # input: given by maryam
mesh_keywords1.rename(index=str, columns={"mesh_synonym":"synonyms","mesh_keyword":"category"}, inplace=True)
mesh_keywords1.columns
mesh_keywords2=add_stem(mesh_keywords1, "synonyms")
mesh_keywords2.columns
mesh_keywords2.rename(index=str, columns={"mesh_synonym":"synonyms","mesh_keyword":"category"}, inplace=True)

temp_mesh_stem=mesh_keywords2[['category','stem_synonyms']]
temp_mesh_lemma=mesh_keywords2[['category','lemma_synonyms']]

temp_mesh_stem.rename(index=str, columns={"stem_synonyms":"synonyms"}, inplace=True)
temp_mesh_lemma.rename(index=str, columns={"lemma_synonyms":"synonyms"}, inplace=True)

mesh_keywords=mesh_keywords2[['synonyms','category']]
mesh_keywords=mesh_keywords.append(temp_mesh_stem, sort=True)
mesh_keywords=mesh_keywords.append(temp_mesh_lemma, sort=True)
mesh_keywords=mesh_keywords.drop_duplicates()
print(len(mesh_keywords))
#1900



####################################################################################
newsid_synonyms_categories=pd.merge(newsid_synonyms,mesh_keywords[['synonyms', 'category']],how='left',on=["synonyms"])
print(len(newsid_synonyms_categories))
#516309

# Merge some categories together and create new column (upcategory)
smoking=['smoking', 'smoking cessation','smoking prevention',
         'tobacco industry', 'tobacco products', 'tobacco smoke pollution',
         'tobacco use disorder','nicotine']
risk=['risk assessment', 'risk factors','risk-taking','risk']
health_behavior=['health behavior','health promotion','attitude to health', 'health knowledge, attitudes, practice']
occupational=['occupational diseases', 'occupational exposure'] 
mortality=['mortality','cause of death']
psychology=['stress, psychological','psychology']
Air_pollution=['air pollution', 'air pollution, indoor','environmental pollutants',
               'air pollutants','isolation & purification']

newsid_synonyms_categories['upcategory']=newsid_synonyms_categories['category']

newsid_synonyms_categories['upcategory']=np.where(newsid_synonyms_categories['category'].isin(smoking),'Smoking_tobaccoproducts_industry_prevention',newsid_synonyms_categories['upcategory'])
b=newsid_synonyms_categories[newsid_synonyms_categories['upcategory']=='Smoking_tobaccoproducts_industry_prevention']

newsid_synonyms_categories['upcategory']=np.where(newsid_synonyms_categories['category'].isin(risk),'risk',newsid_synonyms_categories['upcategory'])
b=newsid_synonyms_categories[newsid_synonyms_categories['upcategory']=='risk']

newsid_synonyms_categories['upcategory']=np.where(newsid_synonyms_categories['category'].isin(health_behavior),'health behavior_attitude',newsid_synonyms_categories['upcategory'])
b=newsid_synonyms_categories[newsid_synonyms_categories['upcategory']=='health behavior_attitude']

newsid_synonyms_categories['upcategory']=np.where(newsid_synonyms_categories['category'].isin(occupational),'occupational',newsid_synonyms_categories['upcategory'])
newsid_synonyms_categories['upcategory']=np.where(newsid_synonyms_categories['category'].isin(mortality),'mortality',newsid_synonyms_categories['upcategory'])
newsid_synonyms_categories['upcategory']=np.where(newsid_synonyms_categories['category'].isin(psychology),'psychology',newsid_synonyms_categories['upcategory'])
newsid_synonyms_categories['upcategory']=np.where(newsid_synonyms_categories['category'].isin(Air_pollution),'air_pollution',newsid_synonyms_categories['upcategory'])

### verification
temp_categories=newsid_synonyms_categories[['upcategory','category']].drop_duplicates().sort_values(by='upcategory')



##########
selected_news_with_categories=pd.merge(selected_news_final,newsid_synonyms_categories,how='left',on='doc_idx')
print(len(selected_news_with_categories))
#442701

temp_mesh=mesh_keywords['category'].unique()
print(len(temp_mesh))
#100

newsid_synonyms.columns
print(len(newsid_synonyms))
#514806

newsid_synonyms.drop_duplicates(inplace=True)
print(len(newsid_synonyms))
#514806

newsid_synonyms_categories.drop_duplicates(inplace=True)
print(len(newsid_synonyms_categories))
#516309

selected_news_with_categories2=selected_news_with_categories[[ 'doc_idx', 'text',  'year', 'synonyms','upcategory']]
selected_news_with_categories2.drop_duplicates(inplace=True)
print(len(selected_news_with_categories2))
# 442701 for category
# 442389       for upcategory

selected_news_with_categories2.to_excel("output/after_solr_all_selected_news_with_synonyms_and_upcategories.xlsx")
selected_news_with_categories_2=selected_news_with_categories[[ 'doc_idx', 'text',  'year', 'synonyms','category']]
selected_news_with_categories_2.drop_duplicates(inplace=True)
print(len(selected_news_with_categories_2))
# 442701 for category

selected_news_with_categories_2.to_excel("output/after_solr_all_selected_news_with_synonyms_and_categories.xlsx")



######################################################################
# add message header and trimmed_tag to news

print(len(selected_news_with_categories2))
#442701
selected_news_with_categories2.columns
news_with_tags= pd.merge(selected_news_with_categories2,news[["message_header","trimmed_tag","doc_idx"]], how="left", on='doc_idx').sort_values(by=['upcategory'])
news_with_tags.sort_values(by=['upcategory','doc_idx'], inplace=True)
print(len(news_with_tags))
#442701
#442389

news_with_tags.to_excel('output/news_with_tags.xlsx', index=False)



#####################################################################
#do analysis for number of news per concept per year

newsid_synonyms_categories.columns
newsid_categories_year=pd.merge(newsid_synonyms_categories,selected_news[['doc_idx','year']], how='left', on='doc_idx')

newsid_categories_year=newsid_categories_year[['doc_idx', 'category','year']]
newsid_categories_year=newsid_categories_year.drop_duplicates()

print(len(newsid_categories_year))
#267614

newsid_categories_year['unique_news_counts']=1
results=newsid_categories_year.groupby(['category','year'])['unique_news_counts'].count().reset_index()
results_ordered=results.sort_values(by=['category','year'],ascending=False)
results_ordered.to_excel("output/ordered_results_exact_search_stem_lemma_origin.xlsx", index=False)

news_per_category_average=results_ordered.groupby('category').agg({'unique_news_counts':'sum','year':'count'}).reset_index().rename(columns={'unique_news_counts':'sum_of_number_of_news','year':"number_of_years"}).sort_values(by=['sum_of_number_of_news'], ascending=False)
news_per_category_average['average_per_year']=news_per_category_average['sum_of_number_of_news']/news_per_category_average['number_of_years']
news_per_category_average.to_excel("output/most popular categories.xlsx", index=False)



###########################################################################################
# change the non- standard upcategory names 
selected_news_with_categories2['upcategory']=np.where(selected_news_with_categories2['upcategory']=='Smoking/tobacco products/industry/prevention','Smoking_tobaccoproducts_industry_prevention',selected_news_with_categories2['upcategory'])
selected_news_with_categories2['upcategory']=np.where(selected_news_with_categories2['upcategory']=='health behavior/attitude','health_behavior_attitude',selected_news_with_categories2['upcategory'])
### verification
temp_categories=selected_news_with_categories2[['upcategory']].drop_duplicates().sort_values(by='upcategory')
temp_categories

#############################################################
#selected_news__with_mesh_keywords2.to_excel("output/selected_news__with_mesh_keywords.xlsx")

years=selected_news_with_categories2['year'].unique()
categories_temp=selected_news_with_categories2['upcategory'].unique()
temp_c=pd.DataFrame(categories_temp)
temp_c.dropna(how='any', inplace=True)
categories1=temp_c.values
categories=np.concatenate(categories1, axis=0)
print(len(categories))
#72


print(categories.sort())
categories2=categories.tolist()
categories2.sort()
print(categories2)
#categories=[ 'Smoking_tobaccoproducts_industry_prevention', 'drug effects',
# 'pharmacology', 'mental disorders' ,'diet' 'obesity',
# 'world health organization', 'sexual behavior' ,'public health',
# 'health policy' ,'toxicity', 'psychology', 'incidence', 'social support',
# 'pregnancy' ,'environmental monitoring' ,'socioeconomic factors',
# 'therapeutic use' ,'health services accessibility', 'epidemiology',
# 'prevalence' ,'body mass index', 'health_behavior_attitude',
# 'palliative care' ,'physiopathology', 'global health', 'virology',
# 'adolescent behavior' ,'health surveys', 'pathology', 'social class',
# 'comorbidity' ,'microbiology', 'environmental exposure',
# 'evidence-based medicine', 'mass screening', 'occupational',
# 'substance-related disorders', 'maternal exposure', 'time factors',
# 'ethnology']


# =============================================================================
# prepare files for topic modeling
selected_news_with_categories3=selected_news_with_categories2[['doc_idx', 'text',  'year','upcategory']]
selected_news_with_categories3.drop_duplicates(inplace=True)
print(len(selected_news_with_categories3))
#226966
#220083

selected_news_with_categories3.to_excel("output/final_selected_news_by_upcategories.xlsx")

if not os.path.exists("output/selected_news_by_categories_year"):
             os.mkdir("output/selected_news_by_categories_year")

if not os.path.exists("output/all_files"):
             os.mkdir("output/all_files")

# categories=['diet','obesity']
for category in categories:
    
    if not os.path.exists("output/selected_news_by_categories_year/"+category):
             os.mkdir("output/selected_news_by_categories_year/"+category)
                      
    for year in years:
         print (category+"  "+str(year)) 
         if not os.path.exists("output/selected_news_by_categories_year/"+category+"/"+str(year)):
             os.mkdir("output/selected_news_by_categories_year/"+category+"/"+str(year))
         temp_file=selected_news_with_categories3[(selected_news_with_categories3['upcategory']==category)&
                                                  (selected_news_with_categories3['year']==year) ]
         temp_file.to_excel("output/all_files/"+category+str(year)+".xlsx")
         
         for i, row in temp_file.iterrows():
             
             temp_news=pd.DataFrame({'col':[row['text']]})
             temp_news.to_csv("output/selected_news_by_categories_year/"+category+"/"+str(year)+"/"+str(row["doc_idx"])+" "+category+str(year)+".txt", sep="\t", header=False, index=False) 
    