import numpy as np
import pandas as pd
import seaborn as sns
import time
import matplotlib.pyplot as plt
from neo_app import load_neo_data

def plot_histogram(df):
    bins_range = np.arange(0, 0.26, 0.01)
    plt.style.use('dark_background')
    plt.rcParams.update({'font.size': 14})
    fig, ax = plt.subplots(figsize=(12, 8))
    neo_diam_array = df['NEO_Diameter'].dropna().values
    ax.hist(neo_diam_array, bins=bins_range, color='tab:orange', alpha=0.7)
    ax.set_xlabel('NEO Diameter in km')
    ax.set_ylabel('Number of NEOs')
    ax.set_xlim(0, 0.25)
    ax.grid(axis='both', linestyle='dashed', alpha=0.2)
    return plt

def plot_cumulative_distribution(df):
    neo_absmag_hist, bins_edge = np.histogram(df, bins=np.arange(10.0, 31.0, 1.0))
    cumul_neo_absmag_hist = np.cumsum(neo_absmag_hist)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(bins_edge[:-1] + 0.5, cumul_neo_absmag_hist, color='tab:orange', alpha=0.7, marker='o')
    ax.set_xlabel(f'NEO Absolute Magnitude')
    ax.set_ylabel('Cumulative number of NEOs')
    ax.grid(axis='both', linestyle='dashed', alpha=0.3)
    ax.set_yscale('log')
    return plt

def plot_distribution(df):
    bin_width = 1
    xlim_range = (15, 30)
    filtered_df = df[df["NEOClass"] != 'Other']
    sns_plt = sns.displot(
        filtered_df,
        x="AbsMag_",
        hue="NEOClass",
        element="step",
        stat="probability",
        common_norm=False,
        binwidth=bin_width
    )
    sns_plt.set(xlim=xlim_range)
    return sns_plt

def plot_kde_distribution(df):
    filtered_df = df.loc[(df["NEOClass"] != "Other") & (df["SemMajAxis_AU"] < 3.0)]
    sns_kde = sns.displot(
        filtered_df,
        x="SemMajAxis_AU",
        hue="NEOClass",
        kind="kde",
        multiple="stack"
    )
    sns_kde.set(xlim=(0.5, 3))
    return sns_kde

if __name__ == '__main__':
    neo_file_path = '../data/processed_neo_data/neo_data_au_with_neo_class_diameter.csv'
    neo_au_df = pd.read_csv(neo_file_path)
    plt = plot_histogram(neo_au_df[["NEO_Diameter"]])
    plt.show()
    time.sleep(3)
    plt = plot_cumulative_distribution(neo_au_df[['AbsMag_']])
    plt.show()
    time.sleep(3)
    sns_plt = plot_distribution(neo_au_df[['AbsMag_', 'NEOClass']])
    sns_plt.fig.show()
    time.sleep(2)
    sns_kde = plot_kde_distribution(neo_au_df)
    sns_kde.fig.show()
    time.sleep(2)

