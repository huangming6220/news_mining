# -*- coding: utf-8 -*-

##########################################################################################
# This program imports the selected news (News in the health related tags) into the solr.
##########################################################################################

#Keywords= [mental health, public health, "epidemiology"  ]

### library
from  solrcloudpy import *
import sys, time
import numpy as np
import pandas as pd

### function
def import_group(pa_coll, group_docs):
    group_num = group_docs[0]
    group_df  = group_docs[1]
    print ('group_num:', group_num)
    group_arr = group_df.to_dict(orient='records') # "how you converted to record ?"
    pa_coll.add(group_arr)
    pa_coll.commit()

def import_data(filename):    
    coll_name = 'pa{0}'.format(0)
    
    # connecting to solr 
    conn = SolrConnection(timeout=12000)
    # check the collection
    
    if coll_name in conn.list():
        # print coll_name, 'exists and remove old records'
        print (coll_name, 'exists and drops')
        pa_coll = conn[coll_name]
        response = pa_coll.search({'q': '*:*'})
        num_records = response.result['response']['numFound']
        print ('Num record: ', num_records)
        pa_coll.delete({'q': '*:*'})
        # pa_coll.drop()
    else:
        print ('creat the collection ', coll_name)
        pa_coll = conn[coll_name].create()
  
    pa_df=pd.read_excel(filename)  
    
    pa_df=pa_df.dropna(how='any')
#    pa_df['text']=pa_df['text'].str.translate(str.maketrans('','','?:!.,;()$'))    
    
    pa_df.drop(['msg_dt', 'message_header', 'msg_tag', 'msg_topic','msg_subtopic', 'web_dt', 'year', 'trimmed_tag'],axis=1, inplace=True)
#    pa_df.columns = ['doc_idx', 'text']
    print ('Patent len', len(pa_df))

    # Divide the pa_df into groups to import group by group
    time_start = time.time()
    # group_size = 10000
    # num_gruops = len(pa_df) / group_size
    # print 'Num gruops', num_gruops
   
    
    # this is just for big data
    num_groups = 5
    group_size = len(pa_df) / num_groups
    print ("Group size", group_size)
    pa_groups = pa_df[['doc_idx','text']].groupby(np.arange(len(pa_df)) // group_size) # different group labels

    [import_group(pa_coll, group_docs) for group_docs in pa_groups]

    response = pa_coll.search({'q': '*:*'})
    num_records = response.result['response']['numFound']
    print ('Num record: ', num_records)
    time_end = time.time()
    print ("Time: ", ((time_end-time_start)/60.0))
    
### program
if  __name__=="__main__":
    """ start Solr before run the importing script
    bin/solr stop -all
    bin/solr start -e cloud -noprompt 
    """

    conn = SolrConnection(["localhost:8983","localhost:7574"],timeout=12000)
    #conn.create('test1',num_shards=1,replication_factor=2)
    conn['test1'].create(num_shards=1,replication_factor=2)
    
#    filename = "output/selected_news_original_with_doc_idx.xlsx" #input for original news
#    filename = "output/selected_news_stemmed_with_doc_idx.xlsx" #input for stemmed news 
    filename = "output/selected_news_lemmatized_with_doc_idx.xlsx" #input for lemmatized news

    import_data(filename)
    