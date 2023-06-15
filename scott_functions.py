######IMPORTS#####

# Ignore Warnings
import warnings
warnings.filterwarnings("ignore")

# Basics:
import pandas as pd
import numpy as np
import math
import numpy as np
import scipy.stats as stats
import os

# Data viz:
import matplotlib.pyplot as plt
import seaborn as sns


# Sklearn stuff:
import sklearn
from sklearn.metrics import accuracy_score
from sklearn.metrics import mutual_info_score
from sklearn.cluster import KMeans

from sklearn.model_selection import train_test_split

## Regression Models
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor
from sklearn.preprocessing import PolynomialFeatures

## Classification Models
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix

## local
import wrangle



###### VISUALIZATIONS ########

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
    fig, axes = plt.subplots(nrows=len(data_frames), figsize=(12, 4 * len(data_frames)))
    
    # Iterate over the DataFrames and plot the scatter plots
    for i, df in enumerate(data_frames):
        # Calculate the top 10 endpoint value counts
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
        plt.xticks(rotation=90)
    # Adjust spacing between subplots
    plt.tight_layout()
    # Show the plot
    plt.show()



######## Anomaly Detection ###########







####### Clustering #########


