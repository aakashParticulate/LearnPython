
# coding: utf-8

# In[32]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy.random as np
import sys
import matplotlib.dates as mdates
import os

get_ipython().magic(u'matplotlib inline')


# In[ ]:


# The Following Function is to collect the names of all the .csv files 
def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


# In[ ]:

# Folder where all the csv files are present
path = os.getcwd();
csv_path = os.path.join(path, 'nobelprize_trends')
plots_path = os.path.join(path, 'plots')

if not os.path.exists(plots_path):
    os.mkdir(plots_path)

# Function called to fetch all file names
filenames = find_csv_filenames(csv_path)
for name in filenames:
    try:
        df = pd.read_csv(os.path.join(csv_path, name), skiprows=4, error_bad_lines=True)
        if not df.empty:
            time = df.columns.values[0]
            scientist = df.columns.values[1]
            if time == 'Month':
                # This pattern is used only to read columns with date values
                # since the csv files also contained a lot other data
                pattern = r'[0-9][0-9][0-9][0-9][^a-zA-Z0-9][0-9][0-9]'
                df = df[df[time].str.contains(pattern)]
                #df[time] = time.strptime(df[time].str, "%Y-%m")
                df[scientist]=df[scientist].astype(float)
                df[time] = pd.to_datetime(df[time].astype(str), format="%Y-%m")
            elif time == 'Week':
                # This pattern is used only to read columns with date values
                # since the csv files also contained a lot other data.
                pattern = r'[0-9][0-9][0-9][0-9][^a-zA-Z0-9][0-9][0-9][^a-zA-Z0-9][0-9][0-9][^a-zA-Z0-9][^a-zA-Z0-9][^a-zA-Z0-9][0-9][0-9][0-9][0-9][^a-zA-Z0-9][0-9][0-9][^a-zA-Z0-9][0-9][0-9]'
                df = df[df[time].str.contains(pattern)]
                # The dates here are weekly, hence taking only the first date for simplicity
                df[time] = df[time].str.split(' - ').str.get(0)
                df[scientist]=df[scientist].astype(float)
                df[time] = pd.to_datetime(df[time].astype(str), format="%Y-%m-%d")
            ax = df.plot(x=df[time],figsize=(15,5))
            fig = ax.get_figure()
            filename = scientist
            fig.savefig(os.path.join(plots_path, "{}.png".format(filename)))
            plt.clf()
    except ValueError as e:
        e.message
        print str(name)
        plt.clf()
    except IndexError as e:
        e.message
        print str(name)
        plt.clf()
    except Exception as e:
        e.args
        print str(name)
        plt.clf()
print "Done"


# In[ ]:



