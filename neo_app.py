
from flask import Flask, render_template, redirect, url_for
from neo_download import count_neos_risks, count_neos_impactors  
import pandas as pd
import os
import subprocess

app = Flask(__name__)


def load_neo_data():
    csv_file_path = '../data/processed_neo_data/neo_data_au_with_neo_class_diameter.csv'
    if os.path.exists(csv_file_path):
        return pd.read_csv(csv_file_path)
    return None
@app.route('/')
@app.route('/index')
def home():
    risk_neos_count = count_neos_risks()
    past_impactors_count = count_neos_impactors()
    return render_template('index.html', 
                           risk_neos=risk_neos_count,
                           impacted_neos=past_impactors_count)

@app.route('/summery')
def summery():
    neo_data = load_neo_data()
    total_neos = len(neo_data) if neo_data is not None else 0
    
    
    
    
    
    neo_data_to_display = neo_data if neo_data is not None else None
    return render_template('summery.html', neo_data=neo_data_to_display.head(), total_neos=total_neos)

@app.route('/download')
def download():
    subprocess.run(['python', 'neo_download.py']) 
    return redirect(url_for('summery'))

@app.route('/process')
def process():
    subprocess.run(['python', 'neo_data_processor.py']) 
    return redirect(url_for('summery'))

@app.route('/visualize')
def visualize():
    subprocess.run(['python', 'neo_data_visualization.py']) 
    return redirect(url_for('visualize'))

@app.route('/final_visual')
def final_visual():
    subprocess.run(['python', 'final_output.py'])
    return redirect(url_for('final_visual'))

if __name__ == '__main__':
    app.run(debug=True)

