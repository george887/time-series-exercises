import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import requests
import os
from datetime import timedelta, datetime as dt

from acquire import get_store_data, opsd_germany_daily

######################### Plotting column distributions ##########################

def hist_plot(df, col, unit_label='', bins=10):
    """
    This function takes in a DataFrame, 
    a string for column name or list,
    a string for unit label, default empty,
    and an integer for number of bins, default 10, and
    displays the distribution of the column.
    """
    plt.rc('figure', figsize=(11, 9))
    plt.rc('font', size=13)
    plt.hist(df[col], bins=bins, color='tomato', ec='black')
    plt.title('Distribution of ' + col)
    plt.xlabel(unit_label)
    plt.ylabel('Count')
    plt.show()

########################### Plotting numeric distributions ##########################

def numeric_hists(df, bins=20):
    """
    Function to take in a DataFrame, bins default 20,
    select only numeric dtypes, and
    display histograms for each numeric column
    """
    plt.rc('figure', figsize=(11, 9))
    plt.rc('font', size=13)
    num_df = df.select_dtypes(include=np.number)
    num_df.hist(bins=bins, color='teal', ec='black')
    plt.tight_layout()
    plt.show()

################################## Acquires and prepares store data ############################

def prep_store_data(df):
    '''This function takes in a df, converts sales date to date time, creates a column for
    month and weekday, renames sale_anount to quantity, and calculates sales total and sales differential. 
    Changes data types to objects. Plots histograms of numeric data and Returns a df
    '''

    df = get_store_data()
    
    # Converting sale_date to datetime
    df['sale_date'] = pd.to_datetime(df.sale_date, format = '%a, %d %b %Y %H:%M:%S %Z')
    df = df.set_index('sale_date').sort_index()
    
    # Creating month and day_of_week column 
    df['month'] = df.index.month
    df['day_of_week'] = df.index.day_name()
    
    # Renaming sale_amount to quantity
    df = df.rename(columns = {'sale_amount': 'quantity'})
    
    # Creating calculated columns
    df = df.assign(sales_total = df.quantity * df.item_price)
    df = df.assign(sales_diff = df.sales_total.diff(periods=1))
    
    # Change dtypes of numeric columns to object and category
    df = (df.astype({'sale_id': object, 'store_id': object,
                    'store_zipcode': object, 'item_id': object, 
                    'item_upc12': object, 'item_upc14': object, 
                    'month': 'category', 'day_of_week': 'category'}))
    
    # Creating histograms of numeric data
    numeric_hists(df)
                
    return df

################################## Acquires and prepares german data ############################

def prep_german_data(df):
    ''' This function acquires german data, converts the date into datetime format, creates numeric histograms,
    sets the index to the datetime variable, adds a month and year column and fills
    nulls with 0s
    '''

    # Lower casing columns
    df.columns = [column.lower() for column in df]

    # Adding my own wind and solar column
    df['wind_&_solar'] = df['wind'] + df['solar']

    # Dropping wind + solar column
    df = df.drop(columns =['wind+solar'])

    #converting date to datetime format
    df.date = pd.to_datetime(df.date, format = '%Y-%m-%d')
    
    # Creating histograms of numeric data
    numeric_hists(df)
    
    # Setting index to the datetime variable
    df = df.set_index("date").sort_index()
    
    # Adding month and year 
    df['month'] = df.index.month
    df['year'] = df.index.year
    
    # Filling nulls 
    df = df.fillna(0)
    
    return df