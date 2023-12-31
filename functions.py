######IMPORTS#####

# Ignore Warnings
import warnings
warnings.filterwarnings("ignore")

# Basics:
import pandas as pd
import numpy as np
import numpy as np
import os

# Data viz:
import matplotlib.pyplot as plt
import seaborn as sns

## local
import wrangle



###### Functions for Questions ########

# defining a function for explore.py to get lower and upper bounds using IQR method
def get_lower_and_upper_bounds(s, multiplier=1.5):
    """
    This function will
    - accept a numeric series, s; and a float, multipler with the default value of 1.5
    - calculate the lower and upper limit, for example:
        - upper = Q3 + 1.5*IQR
        - lower = Q1 - 1.5*IQR
        - Q1 and Q3 are the quartile values for the 1st/3rd quartiles
        - IQR is the Interquartile range which is Q3-Q1
    - this method works for non-normally distributed data (according to curriculum / Tukey)
    - returns lower_bound and upper_bound
    """
    Q1 = s.quantile(.25)
    Q3 = s.quantile(.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR  
    return lower, upper


# defining a function to get the top or bottom page counts by program
def question1_7(df, number=5, bottom=False):
    """
    This function will 
    - accept a df from wrangle_curriculum_logs and a boolean bottom (True if user wants bottom 5, False if top 5)
    - print out the top or bottom 5 most accessed pages per program
    - returns nothing
    """
    # 50313 rows with '/' as the endpoint. This is what the text file has.
    # I will ignore these for the sake of exploration
    
    # get a count of the unique program_id - endpoint combinations
    endpoints_by_program = df[df.endpoint != '/'].groupby(['program_id', 'endpoint']).endpoint.count()
    # make a list of program_ids to iterate over
    program_id_list = sorted(df.program_id.unique())

    if bottom:
        top_or_bottom = 'Bottom'
    else:
        top_or_bottom = 'Top'
    # printing the top/bottom programs in each of the program ids
    for id in program_id_list:
        print (f'{top_or_bottom} {number} page access counts for program {id}: ')
        print (endpoints_by_program.loc[id].sort_values(ascending = bottom).head(number))
        print('---------------------------')
        
        
# defining a function to get lower and upper bounds and compare pages across cohorts
def question2(df, multiplier=3):
    """
    This function will
    - accept a dataframe from wrangle_curriculum_logs, preferably separated by program_id to reduce 
       runtime and for results readability
    - looks for high/low page visits per cohort
    - returns a dataframe of pages that were visited a lot by some cohorts by very litte by other cohorts
    """
    # initialize lists for top and bottom page counts
    top_page_list = []
    bottom_page_list = []

    # loop through cohorts and get most/least accessed pages
    for c_name in df.name.unique():
        # get the page counts for each cohort
        cohort_pages = df[df.name == c_name].endpoint.value_counts()
        # get the lower, upper bounds of page counts using IQR multiplier from function call
        lower, upper = get_lower_and_upper_bounds(cohort_pages, multiplier)
        if lower <= 0: lower = 1
        # add top/bottom pages to top/bottom_page_list
        top_page_list += list(cohort_pages[cohort_pages > upper].index)
        bottom_page_list += list(cohort_pages[cohort_pages <= lower].index)

    # make a list of the bottom pages that are found in the top pages
    # this will tell me what pages are glossed over by one cohort that are higher views in other cohorts
    bottom_in_top_list = []
    for p in bottom_page_list:
        if p in top_page_list:
            bottom_in_top_list.append(p)       

    ## initialize the df we will return our results in : mismatch_pages_df
    # set columns for df containing results: endpoint + the cohort names 
    name_list = list(df.name.unique())
    columns = ['endpoint'] + name_list
    mismatch_pages_df = pd.DataFrame(columns=columns)
    # for each page in the bottom_in_top_list, see what the page count is for each cohort & add it to mismatch_pages_df
    for p in bottom_in_top_list:
        p_count_list = []
        # for each cohort get pagecount and append to p_count_list
        for cohort in mismatch_pages_df.columns[1:]:
            p_count = df[(df.name == cohort) & (df.endpoint == p)].endpoint.count()
            p_count_list.append(p_count)
        # make a new row and add it to the bottom of mismatch_pages_df
        new_entry = [p] + p_count_list
        mismatch_pages_df.loc[len(mismatch_pages_df)] = new_entry
    
    return mismatch_pages_df


def question3(df, limit=10):
    """
    This function will 
    - accept the dataframe from wrangle_curriculum_logs
    - accept a limit, which is the max number of page access's for a user, default value = 10
    - look at page access's that occur between a cohort's start_date and end_date
    - returns a dataframe of page accesses grouped by user_id, where the total number of page access's is <= limit
    """
    # first extract from the df only those page accesses that occurred during a user's class start and end dates
    in_class_access_df = df[(df.index>=df.start_date) & (df.index<=df.end_date)]
    # get value_counts of users (number of page accesses per user)
    in_class_user_page_counts = in_class_access_df.user_id.value_counts()
    # get only the users that, while in class, accessed curriculum pages <= 'limit' times
    low_access_in_class = in_class_user_page_counts[in_class_user_page_counts<=limit]
    # get all page accesses by users who accessed the curriculum <= limit times
    results_df = in_class_access_df[in_class_access_df['user_id'].isin(low_access_in_class.index)]
    return results_df




def question6(df):
    '''
    This function creates a list of web dev and data science programs
    It then finds the Top 10 lessons most commonly accessed post graduation
    Finally it creates a visualization of them 
    '''
    # selecting post grad access rows
    df_postgrad= df[df.index>df.end_date]
    # splitting to web dev (prog 0-2) and data science (prog 3)
    web_dev = df_postgrad[df_postgrad.program_id <3]
    data_science = df_postgrad[df_postgrad.program_id ==3]
    data_frames = [web_dev, data_science]

    # Create a figure and axes for the subplots
    fig, axes = plt.subplots(nrows=len(data_frames), figsize=(12, 8 * len(data_frames)))
    
    # Iterate over the DataFrames and plot the scatter plots
    for i, df in enumerate(data_frames):
        # Calculate the top 10 endpoint value counts (ignoring first row which is '/')
        top_10 = df['endpoint'].value_counts().head(11)[1:]
    
        # Convert the value counts to a DataFrame for easier plotting
        df_top_10 = pd.DataFrame({'Endpoint': top_10.index, 'Count': top_10.values})
    
        # Plot the scatter plot
        ax = sns.scatterplot(data=df_top_10, x='Endpoint', y='Count', ax=axes[i])
    
        # Set plot title
        if i == 0:
            title = 'Web Dev'
        else:
            title = 'Data Science'
        # Set plot title and axis labels
        ax.set_title(f'Top 10 Endpoint Value Counts - {title}')
        ax.set_xlabel('Endpoint')
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=90)
    # Adjust spacing between subplots
    plt.tight_layout()
    # Show the plot
    plt.show()







