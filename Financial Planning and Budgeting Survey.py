
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
 
sns.set() 
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('ticks')

import warnings
warnings.filterwarnings('ignore')

pd.options.display.html.table_schema = True # Data Explorer On!
pd.options.display.max_rows = None # Send all the data! (careful!)


# In[5]:


# Import Data
df=pd.read_csv('Financial Planning and Budgeting.csv')

# Remove any unwanted data 
df=df[df.Age!='Under 18']  #remove responses from Under 18 population

# display first 10 rows
df.head(10)


# In[9]:


# Display available columns
df.columns.tolist()


# In[35]:


""" USE FOR EXAMINING THE MUTLI-CHOICE ANSWERS AS A FUNCTION OF VARIOUS CONTROLS (AGE, INCOME, ETC)"""

# Filter data to only one select subset for one parameter
Filterby = 'None'  #eg 'Age', 'None'
Filter = ''        #eg '45-54'

if 'None' in Filterby:
    df2=df.copy()
else:
    df2=df[df[Filterby]==Filter]

# Control_on determines the y-axis and the groups are the various bars you want to display
Control_On = 'Age'   #eg Income
Groups ='Online_Advice'   #eg InvestmentTools
column_set= [col for col in df.columns if Groups in col]

# remove the "describe" data from the plots here since it is not interesting
# this could also be done for "other" or any answer type you don't care for
if 'Describe' in column_set[-1]:
    column_set=column_set[:-1]

# extract subset of columns that are in the "control_on" category
column_set= np.append(Control_On,column_set)
print(column_set)

# count all response types for each column
test_grouped = df2[column_set]
test_grouped = test_grouped.groupby([Control_On]).count()
print(test_grouped)

# Normalize all answers by total number of respondents in "control_on" category
numberofentries=df2[Control_On].value_counts()
test_grouped=test_grouped.div(numberofentries,axis=0)
test_grouped=test_grouped.multiply(100)

# plot
ax=test_grouped.sort_index(ascending=True).plot(
    kind='barh',
    figsize=(10, 15),
    cmap='Spectral',
    width=0.7,
    edgecolor='black',
    fontsize=17,
    grid='On')
    
ax.set_xlabel('Percent of Responses',fontsize=16)
ax.set_ylabel(Control_On,fontsize=16)
ax.set_title('Percent of ' + Groups + ' Responses Grouped by ' + Control_On + ' (Filter: ' + Filterby + '=' + Filter + ')',fontsize=18)


# In[56]:


""" BETTER SUITED TOWARD MUTLIPLE CHOICE ANSWERS WHERE THERE IS ONLY ONE ANSWER PER QUESTION """

# This is the question we will look at in bar charts with the y axis
Examine='OnTrack'
examine_unique=df[Examine].unique()

# each subplot will be for a different set of responses to this other multiple-choice question
Var='Income'
Filters=np.sort(df[Var].unique())
nplots1 = int((len(Filters)+np.mod(len(Filters),2))/2)

# prepare plots
fig, ax = plt.subplots(nplots1,2,sharex=True,sharey=True)
axs=ax.ravel()

#cycle through all sub-categories for each subplot
Q=0
for Filter in Filters:
    d3=df[df[Var]==Filter].sort_values(Examine)
    
    # normalize all answers by the number of respondents in this "Var" subgroup
    numberofentries=d3[Examine].value_counts(normalize=True)
    numberofentries=numberofentries.sort_index(ascending=False)
    numberofentries=numberofentries.multiply(100)
    
    ### Fold in all options so y axes are common
    examine_unique=df[Examine].unique()  #find unique options for variable being examined
    a=pd.DataFrame(np.zeros(len(examine_unique))) #construct a dataframe
    a.index=examine_unique #reindex using the options
    a.columns=[Examine] #rename columns

    #covert numberofentries to dataframe
    b=pd.DataFrame(numberofentries)

    #merge the two on all unique options (a) and fillna with 0
    C=a.merge(b,how='left', left_index=True, right_index=True)
    C=C.iloc[:,[-1]]
    C.columns=[Examine]
    C=C.fillna(0)

    
    # PLOT    
    AX2=C.plot(
        ax=(axs[Q]),
        kind='barh',
        figsize=(15, 15),
        cmap='Spectral',
        width=0.7,
        edgecolor='black',
        fontsize=17,
        grid='On',
        ).yaxis.label.set_visible(False)
    
    title_str=Var + ' = ' + Filter
    title_str=title_str.replace('and'," - ")
    axs[Q].set_xlabel('Percent of Responses',fontsize=16)
    axs[Q].set_title(title_str,fontsize=16)
        
    Q+=1
fig.tight_layout()

