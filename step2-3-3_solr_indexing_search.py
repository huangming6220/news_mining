# -*- coding: utf-8 -*-

######################################################################################
# For given news and given synonyms, it gives us the news which contain the synonyms.
######################################################################################

### library
import pandas as pd
from solrcloudpy import SolrConnection

### function
def solr_query(pa_coll, disease_record):
    # coll information
    response = pa_coll.search({'q': '*:*'})
    num_records = response.result['response']['numFound']
    # print 'Num record: ', num_records
    # disease information
    disease_idx = disease_record[0]
    #disease_name = disease_record[1]['name']
    disease_query = disease_record[1]['keyword']
    #disease_clean_query = disease_query.strip('\"')
    #phewas = disease_record[1]['phewas']
    if disease_idx % 100 == 0: print ('disease_idx ', disease_idx)

    # disease query
#    response_obj = pa_coll.search({'q': "text:{0}".format(disease_query), 'rows': 0}).result['response']
    response_obj = pa_coll.search({'q': 'text:"{0}"'.format(disease_query), 'rows': 0}).result['response']   # 'text:"{0}"' instead of "text:{0}" to search for exact phrases
    response_num = response_obj['numFound']
    # print 'response num ', response_num

    result_arr = []
    if response_num > 0:
        response_obj = pa_coll.search({'q': 'text:"{0}"'.format(disease_query), 'rows': num_records}).result['response']  # 'text:"{0}"' instead of "text:{0}" to search for exact phrases
        response_docs = response_obj['docs']
        # print 'response docs', response_docs
        # query results

        for pa_doc in response_docs:
            doc_index = pa_doc['doc_idx'][0]
            meta_doc = {'doc_idx': doc_index, \
                        'disease_query': disease_query, \
                        }
            result_arr.append(meta_doc)

    return result_arr

def disease_query(coll_name, disease_phewas_df):
    # check solr collection
    conn = SolrConnection(timeout=6000)
    pa_coll = conn[coll_name]
    print ('Num disease: ', len(disease_phewas_df))

    # query solr with each disease name
    # serial
    disease_docidx_arr = []
    for disease_record in disease_phewas_df.iterrows():
        result_arr = solr_query(pa_coll, disease_record)   
        
        for res in result_arr:
            disease_docidx_arr.append(res)

    return disease_docidx_arr


def filter_data(disease_phewas_path, clean_path, disease_docidx_path, filter_path):    
    # get disease-phewas mapping
    time_start = time.time()
    
    disease_phewas_df = pd.read_csv(disease_phewas_path,engine='python')    
    
    coll_name = 'pa{0}'.format(0)
        
    disease_docidx_arr = disease_query(coll_name, disease_phewas_df)
    # print 'disease_docidx len', len(disease_docidx_arr)
    # print disease_docidx_arr[0]
    # save disease disease_docidx data
    disease_docidx_df = pd.DataFrame(disease_docidx_arr)
    print ('disease_docidx_df len', len(disease_docidx_df))
    # print disease_docidx_df
    disease_docidx_df.to_csv(disease_docidx_path, index=False)

#    disease_docidx_df=pd.read_csv(disease_docidx_path)
    # filter patent data
    docidx_list = list(disease_docidx_df['doc_idx'].unique())
    clean_df = pd.read_excel(clean_path)
    
    clean_df=clean_df.dropna(how='any')
      
#    clean_df['doc_idx'] = range(len(clean_df))
    print ('clean_df len', len(clean_df))
    filter_df = clean_df[clean_df['doc_idx'].isin(docidx_list)]
    print ('filter_df len', len(filter_df))
    filter_df.to_csv(filter_path, index=False)
    # print filter_df
    time_end = time.time()
    print ("Time: ", (time_end-time_start)/60.0)

### program
if  __name__=="__main__":
        # input
#    disease_phewas_path = 'input/public_health_mesh_keywords_with_synonyms_sep052018.csv'  # input file: output of step1-3 program after edition and also we just kept one column "keyword"  for original keyword
#    disease_phewas_path = 'input/public_health_mesh_keywords_with_synonyms_sep052018_stemmed.csv'  # input file: output of step1-3 program after edition and also we just kept one column "keyword" for stemmed keyword
    disease_phewas_path = 'input/public_health_mesh_keywords_with_synonyms_sep052018_lemmatized.csv'  # input file: output of step1-3 program after edition and also we just kept one column "keyword" for lemmatized keyword

    # output
#    clean_path = "output/selected_news_original_with_doc_idx.xlsx"  #input file :selected news file as another input with text and doc_idx columns for original news
#    clean_path="output/selected_news_stemmed_with_doc_idx.xlsx"  #input file :selected news file as another input with text and doc_idx columns for stemmed news
    clean_path="output/selected_news_lemmatized_with_doc_idx.xlsx"  #input file :selected news file as another input with text and doc_idx columns for lemmatized news
    
#    disease_docidx_path = "output/file1_keywords_original_keywords.csv"  # output for original news 
#    disease_docidx_path = "output/file1_keywords_stemmed_keywords.csv"  # output for stemmed news 
    disease_docidx_path = "output/file1_keywords_lemmatized_keywords.csv"  # output for lemmatized news 
    
#    filter_path="output/file1output_origin_news.csv"  #outptu for original news
#    filter_path="output/file1output_stemmed_news.csv"  #outptu for stemmed news
    filter_path="output/file1output_lemmatized_news.csv"  #outptu for lemmatized news
    
    filter_data(disease_phewas_path, clean_path, disease_docidx_path, filter_path)
    