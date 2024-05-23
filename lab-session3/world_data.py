import numpy as np
import pandas as pd
import os
from lookup import main
from isub import isub




world_data = pd.read_csv("data/worldcities-free-100.csv")

# Copy the data, add row numbers, dataset name
world_data['row_number'] = world_data.reset_index().index + 1
world_data['dataset'] = 'WORLDCITIES'
result_df = world_data.copy()

#find distinct values for cities and countries
cities = list(result_df.city.drop_duplicates())
countries = list(result_df.country.drop_duplicates())



def create_dataframe(countries):
#function to extract ontologies and convert to dataframe

    list_dataframes= []
    for country in countries:
        print("Entities matching the keyword: " + country)

        dict = main(country)
        ds = []
        for kg, ontology in dict.items():
            #subs = '<id'
            #print(kg)
            
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
        df.columns = df.columns.str.replace(' ', '')

        df['place'] = country
        list_dataframes.append(df[['similarity', 'place', 'source', '<id', 'types', 'label']])

    new_df = pd.concat(list_dataframes)
    result = new_df.sort_values(['place','source','similarity'], ascending=False).groupby(['place', 'source']).first().reset_index()
    result['newtypes'] = result['types'].str.rsplit('/').str[-1].str.strip("'")
    final_df = result[['similarity', 'place', '<id','newtypes']]
    return final_df

#format the final dataframe
source_df = result_df[['dataset', 'city', 'country']]
country_frame = create_dataframe(countries).drop_duplicates()
country_frame['actual_type'] = 'Country'
city_frame = create_dataframe(cities).drop_duplicates()
city_frame['actual_type'] = 'City'

merged_country = pd.merge(source_df, country_frame, left_on = ['country'], right_on=["place"],\
                           how="left").rename(columns={'<id' : 'URI','newtypes': 'predicted_type'})\
                            [['dataset','similarity', 'place', 'URI', 'predicted_type', 'actual_type']]

merged_city = pd.merge(source_df, city_frame, left_on = ['city'], right_on=["place"],\
                           how="left").rename(columns={'<id' : 'URI','newtypes': 'predicted_type'})\
                            [['dataset', 'similarity', 'place', 'URI', 'predicted_type', 'actual_type']]

final_frame = pd.concat([merged_city, merged_country], ignore_index=True)                                                                            


final_frame.to_csv('data/worldcities_output.csv', index=False)

print(final_frame[['dataset', 'similarity','place', 'predicted_type','actual_type', 'URI']])









