# coding: utf-8

###################################################################
# Step 1-3: find synonyms for mesh keywords 
###################################################################

# library
import pandas as pd
import numpy as np

# function
# importing the mesh public health terms and normalizing the dataset
def mesh_term_data(file1):
    inpfile = file1
    mesh_term_df = pd.read_excel (inpfile )
    return(mesh_term_df['Mesh Terms '])

# identifying the synonyms of the imported Mesh terms
def mesh_synonyms(file1, cui_mesh):
    mesh_term = mesh_term_data(file1)
    
    out_df = pd.read_csv(cui_mesh, sep='\t',encoding='utf-8' )
    cui_mesh = out_df[out_df['name'].isin(mesh_term)]
    
    cui_mesh = cui_mesh ['cui'].drop_duplicates()

    # identying the synonyms of the imported Mesh tersm in the selected cui_synonym
    cui_synonym = out_df[out_df['cui'].isin (cui_mesh)].drop_duplicates()
    i=0;
    for term in mesh_term:
        temp_term=out_df.loc[out_df['name']==term]
        if len(temp_term)==0:
             print(term)
        else :
            i=i+1        
    print(i)        

    return cui_synonym

# exporting the synonym for each mesh term to a dataframe
def df_synonyms(file1, cui_mesh):
    df_export = pd.DataFrame()

    term=mesh_term_data(file1)
    i=0
    terms=term.tolist()
    cui_synonym = mesh_synonyms(file1, cui_mesh)
    for term in terms:
        msh = cui_synonym [cui_synonym.name == terms[i]]
        if len(msh)==0 :
              print(term)
        synonym = cui_synonym[cui_synonym['cui'].isin(msh['cui'])]
       
        term_repeat = np.repeat (terms [i], len (synonym.index))
        se = pd.Series (term_repeat)
        synonym['term'] = se.values
    
        df_export= df_export.append (synonym)
        i = i +1

        # removing the exported cui_synonym from the synonyms
        cui_synonym = cui_synonym[~cui_synonym['cui'].isin(synonym['cui']) ]
    
    
    df_export.columns = ['cui','mesh','synonym', 'mesh_keyword']
    print(i)
    return(df_export)

# Delete the punctuations, delete extra space between the words, delete the terms less than 3 length
# Delete the words less than 3 characters from the start of the term
def modify_synonyms(inpfile, outfile):
    df_input=pd.read_csv(inpfile, sep="\t" )
    df_input_modified=df_input.copy()
    
    chars = ",;()[]1234567890.{}/-_?:'"
    df_input_modified['m_synonym']=df_input['synonym'].str.translate(str.maketrans(chars," "*len(chars))).str.strip()
    df_input_modified['m_synonym']=df_input_modified['m_synonym'].str.split()
    
    for index , row in df_input_modified.iterrows():
         print (row['m_synonym'])
         df_input_modified.at[index,'new']=row['m_synonym'][0]
    
    df_input_modified['m_synonym']=df_input_modified['m_synonym'].str.join(' ')
    
    df_input_modified2=df_input_modified.loc[df_input_modified['m_synonym'].str.len()>=3]
    df_input_modified2=df_input_modified2.loc[df_input_modified2['new'].str.len()>=3]
    df_input_modified2.drop(['new'],axis=1,inplace=True)
    df_input_modified2.to_excel(outfile)

# program
if  __name__=="__main__":
    # input files
    inpfile='input/df_keywords_selected610.xlsx'
    cui_mesh="input/cui_mesh_name.txt"
    # output files
    outfile='output/public_health_mesh_synonyms610.txt'
    outfile2="output/public_health_mesh_synonyms610_modified.xlsx"
#    outfile2 = 'input/public_health_mesh_keywords_with_synonyms_sep052018.csv'  # we just kept one column "keyword" for original keyword
#    outfile2 = 'input/public_health_mesh_keywords_with_synonyms_sep052018_stemmed.csv'  # we just kept one column "keyword" for stemmed keyword
#    outfile2 = 'input/public_health_mesh_keywords_with_synonyms_sep052018_lemmatized.csv'  # we just kept one column "keyword" for lemmatized keyword

    df_modified=df_synonyms(inpfile, cui_mesh)
    df_modified['synonym']=df_modified['synonym'].str.lower().str.strip()
    df_modified=df_modified.drop_duplicates()
    df_modified.to_csv(outfile,sep='\t', index=None, encoding='utf-8' )

    modify_synonyms(outfile, outfile2)
    
