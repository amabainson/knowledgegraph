import numpy as np
import pandas as pd
import os
from lookup import main
from isub import isub
import re
import traceback
 


def contains_number(string):
     #function to determine which column contains numbers
    return False if set(string).intersection('0123456789') else True

def create_dataframe(countries):
    #function to extract ontologies and convert to dataframe
    list_dataframes= []
    for country in countries:

        print("Entities matching the keyword: " + country)

        dict = main(country)
        ds = []
        for kg, ontology in dict.items():
            #print(ontology)
            
            for entity in ontology:
                a = str(entity).split(',')
                #print(a)
                d = {}
                for b in a:
                    try:
                        i = b.split(': ')
                        d[i[0]] = i[1]
                    except:
                        pass
                ds.append(d)
                
                d['similarity']= (isub(country, d[' label']))
        df = pd.DataFrame(ds)
        df.columns = df.columns.astype(str).str.replace(' ', '')

        df['place'] = country
        try:
            list_dataframes.append(df[['similarity', 'place', 'source', '<id', 'types', 'label']])
        except:
            print(f"Error processing data for entity: {country}")#skip if no information can be found
            continue

    new_df = pd.concat(list_dataframes)
    result = new_df.sort_values(['place','source','similarity'], ascending=False).groupby(['place', 'source']).first().reset_index()
    final_df = result[['similarity', 'place', '<id', 'label']]

def script(file_path):
    #function to read source files and annotate entities
    # Read the CSV file
    source_data = pd.read_csv(file_path)
    file_title = file_path.split('/')[-1].split('.')[0]

    # Add row column numbers and filename
    data_copy = source_data.copy()
    source_data['row_number'] = source_data.reset_index().index + 1
    

    list_df = []
    for ind, column in enumerate(data_copy.columns):
        print(ind, column)   
        values = list(source_data[column])
        #print(values)
        try:
            if [s for s in values if contains_number(s)]:#eliminate columns that contain numbers#
                similarities = create_dataframe(values)
                similarities['column_number'] = column[-1]
                similarities = pd.merge(source_data, similarities, left_on= [column], right_on="place", how="left")
                
                list_df.append(similarities)

        #except Exception:
            #traceback.print_exc()
        except:
            print(f"Error processing column: {column}")

    final_frame = pd.concat(list_df, ignore_index=True)  
    final_frame['file_name'] = file_title
    final_frame = final_frame[['file_name','row_number', 'column_number', '<id']].dropna()
    final_frame.to_csv('sem-tab-evaluator/system_example/'+file_title+'_cea_output'+'.csv', header=False, index=False)

    print(final_frame)


if __name__ == '__main__':
    # assign directory
    directory = 'sem-tab-evaluator/tables'
    
    # iterate over files in 
    # that directory
    for file_path in os.scandir(directory):
        if file_path.is_file():
            print(file_path.path)
            script(file_path.path)










