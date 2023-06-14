import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import env
import os

from sqlalchemy import text, create_engine

import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

####################### Imports ############################
# defining function to read a sql query
def read_sql_query(query, db):
    """
    This function will 
    - accept two strings: an sql query, and the database name
    - read the query from the database into a dataframe
    - return the dataframe
    """
    # using "new" (May 2023) version of reading sql queries with pandas

    # define the database url
    url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/{db}'
    # create the connection
    engine = create_engine(url)
    connection = engine.connect()
    # create the query using text() and the string that has the sql query
    query_t = text(query)

    df = pd.read_sql(query_t, connection)

    return df

def wrangle_curriculum_logs():
    """
    This function will 
    - read in curriculum data from a txt file ('anonymized-curriculum-access.txt')
    - separate it into columns
    - set date column as the index (as a datetime) and sort the index
    - fill null values in cohort_id with 0
    - then read in data from a sql query to get cohort names and dates
    - merge the two dataframes together on cohort_id
    - return the merged df
    """
    colnames = ['date', 'endpoint', 'user_id', 'cohort_id', 'source_ip']
    df = pd.read_csv("anonymized-curriculum-access.txt", 
                     sep="\s", 
                     header=None, 
                     names = colnames, 
                     usecols=[0, 2, 3, 4, 5])
    # fill null values with 0 and make this float column into integer column
    df.cohort_id = df.cohort_id.fillna(0)
    df.cohort_id = df.cohort_id.astype('int64')
    
    # pull second dataframe from mysql database
    # define query and database to pull from 
    query = 'SELECT id, name, start_date, end_date, program_id FROM cohorts'
    db = 'curriculum_logs'
    # read in the sql query 
    cohort_df = read_sql_query(query, db)
    # add a cohort id of 0 to account for the null values in the previous df
    cohort_df.loc[len(cohort_df.index)] = [0,'Unknown cohort', '2000-01-01', '2000-01-01', 0]
    # merge the dataframes together
    new_df = pd.merge(df, cohort_df, left_on='cohort_id', right_on='id')
    # drop the repeated column
    new_df = new_df.drop(columns=['id'])
    
    # setting date column as the index
    new_df.date = new_df.date.astype('datetime64')
    new_df = new_df.set_index('date')
    new_df = new_df.sort_index()
    
    return new_df
    