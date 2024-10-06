# download.py
import os
import requests
import pandas as pd

def get_request(url):
    http_response = requests.get(url)
    return http_response

def save_neo_data(http_response, file_path):
    dir = os.path.dirname(file_path)
    os.mkdir(dir) if not os.path.isdir(dir) else None
    with open(file_path, 'wb') as file:
        file.write(http_response.content)

def save_neo_data_to_csv(neo_df, file_path):
    neo_df.to_csv(file_path, index=False, header=True)

def process_cat_file(file):
    with open(file, 'r') as f_temp:
        neo_dict = [
            {
                "Name": line.split()[0].replace("'", ""),
                "Epoch_MJD": float(line.split()[1]),
                "SemMajAxis_AU": float(line.split()[2]),
                "Ecc_": float(line.split()[3]),
                "Incl_deg": float(line.split()[4]),
                "LongAscNode_deg": float(line.split()[5]),
                "ArgP_deg": float(line.split()[6]),
                "MeanAnom_deg": float(line.split()[7]),
                "AbsMag_": float(line.split()[8]),
                "SlopeParamG_": float(line.split()[9]),
            }
            for line in f_temp.readlines()[6:]
        ]
        neo_df = pd.DataFrame(neo_dict)
        return neo_df

def count_neos(file_path):    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    data = pd.read_csv(file_path)
    return data


def count_neos_risks():
    return count_neos('../data/raw_csv_data/riskList.csv')


def count_neos_impactors():
    return count_neos('../data/raw_csv_data/pastImpactorsList.csv')

if __name__ == '__main__':
    base_url = "https://newton.spacedys.com/~neodys2/neodys.cat"
    http_response = get_request(base_url)
    cat_file_path = '../data/raw_cat/neo_data.cat'
    save_neo_data(http_response, cat_file_path)

    csv_file_path = '../data/raw_csv_data/neo_data.csv'
    neo_df = process_cat_file(cat_file_path)
    save_neo_data_to_csv(neo_df, csv_file_path)

    

    
