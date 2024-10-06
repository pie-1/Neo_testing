import os
import math
import pandas as pd

from neo_download import save_neo_data_to_csv

def compute_aphelion_perihelion(neo_df):
    neo_df['Aphelion_AU'] = neo_df['SemMajAxis_AU'] * (1 + neo_df['Ecc_'])
    neo_df['Perihelion_AU'] = neo_df['SemMajAxis_AU'] * (1 - neo_df['Ecc_'])
    return neo_df



def neo_class(sem_maj_axis_au : float, peri_helio_au : float, ap_helio_au : float) -> str:
    if (sem_maj_axis_au > 1.0) & (1.017 < peri_helio_au < 1.3):
        neo_type = 'Amor'
    elif (sem_maj_axis_au > 1.0) & (peri_helio_au < 1.017):
        neo_type = 'Apollo'
    elif(sem_maj_axis_au < 1.0) & (ap_helio_au > 0.983):
        neo_type = 'Aten'
    elif(sem_maj_axis_au < 1.0) & (ap_helio_au < 0.983):
        neo_type = 'Atria'
    else:
        neo_type = 'Other'
        
    return neo_type
    

def comp_neo_diameter(abs_mag : float, albedo : float=0.15):
   
    neo_diam_km = ((10.0 ** (-0.2 * abs_mag))/(math.sqrt(albedo))) * 1329.0
    return neo_diam_km

def compute_stats(df):
    neo_diameter_stats = df[['NEO_Diameter']].describe()
    return neo_diameter_stats.values.flatten().tolist()

if __name__=="__main__":
    csv_file_path = '../data/raw_csv_data/neo_data.csv'
    neo_df = pd.read_csv(csv_file_path)
    neo_au_df = compute_aphelion_perihelion(neo_df)
    csv_au_file_path =  '../data/processed_neo_data/neo_data_au.csv'
    save_neo_data_to_csv(neo_df, csv_au_file_path)


    neo_au_df['NEOClass'] = neo_au_df.apply(lambda row: neo_class(row['SemMajAxis_AU'], 
                                                    row['Perihelion_AU'], 
                                                    row['Aphelion_AU']), axis=1)

    csv_au_file_path = '../data/processed_neo_data/neo_data_au_with_neo_class.csv'
    save_neo_data_to_csv(neo_df, csv_au_file_path)



    neo_au_df['NEO_Diameter'] = neo_au_df.apply(lambda row: comp_neo_diameter(row['AbsMag_']), axis=1)

    csv_au_file_path = '../data/processed_neo_data/neo_data_au_with_neo_class_diameter.csv'
    save_neo_data_to_csv(neo_df, csv_au_file_path)

    stats_list = compute_stats(neo_au_df)
    item_count, mean, _, min, _, median, _, max = stats_list

    print(f"Total number NEO data: {item_count} km")
    print(f"Known minimum NEO diameter: {min} km")
    print(f"Known maximum NEO diameter: {max} km")
    print(f"Mean NEO diameter: {mean} km")
    print(f"Median NEO diameter: {median} km")
