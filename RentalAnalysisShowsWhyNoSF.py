#!/usr/bin/env python
# coding: utf-8

# In[1]:


pwd


# In[2]:


cd downloads


# ### San Francisco Housing Cost Analysis

# In[73]:


# imports
import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

import warnings
warnings.filterwarnings('ignore')


# In[80]:


#Read Mapbox API
load_dotenv()
map_box_api = os.getenv("MAPBOX_TOKEN")


# #### Load Data

# In[32]:


#Load CSV and set year
sf_data = pd.read_csv("sfo_neighborhoods_census_data.csv", index_col="year")
sf_data.head()


# #### Housing Units Per Year
# 
# Mean/Max/Min/STD

# In[33]:


#Caculate the mean number of housing units per year 

housing_units_per_year = sf_data['housing_units'].groupby(by = ('year')).mean()
housing_units_per_year


# In[29]:


housing_units_max = housing_units_per_year.max()
housing_units_max


# In[28]:


housing_units_min = housing_units_per_year.min()
housing_units_min


# In[30]:


housing_units_std = housing_units_per_year.std()
housing_units_std


# In[31]:


housing_units_per_year.to_csv(r'C:\Users\David R\Downloads\housing_units_per_year.csv', index=False)


# In[25]:


# Use the Pandas plot function to plot the average housing units per year.
housing_units_per_year.plot.bar(figsize=(8,8), x='Year', y='Housing Units',title='Housing Units in San-Francisco from 2010 to 2016')
# Optional Challenge: Use the min, max, and std to scale the y limits of the chart
# YOUR CODE HERE!
plt.ylim((360000, 385000))
plt.show()
plt.close()


# In[36]:


# Calculate the average sale price per square foot and average gross rent
sf_avg_price_rent_df = sf_data[['sale_price_sqr_foot','gross_rent']].groupby(['year'])['sale_price_sqr_foot','gross_rent'].mean()
sf_avg_price_rent_df


# In[ ]:


# Create two line charts, one to plot the average sale price per square foot and another for average montly rent

# Line chart for average sale price per square foot
#reset index to make the year as x 


# #### Average Rent Per Year

# In[43]:


sf_data[['gross_rent']].groupby(by='year').mean().plot(kind = 'line', title = "Average Gross Rent in San Fransisco", color= 'black')
#Different ways to do a graph. Line is Black because of SF Giants. 


# #### Average Price per Sqft per Year

# In[42]:


price_plot = sf_avg_price_rent_df.reset_index().plot(x='year',  y='sale_price_sqr_foot',  title='Average Price per SqFt by Year', color='orange')
price_plot.set_ylabel("Price per SqFt")
#Different ways to do a graph. Line is Orange because of SF Giants. 


# ### Average Prices by Neighborhood
# Group by year and neighborhood and then create a new dataframe of the mean values

# In[45]:


sf_df = sfo_data.groupby(by = ['year','neighborhood']).mean().reset_index()
sf_df.head(10)


# In[46]:


# Use hvplot to create an interactive line chart of the average monthly rent.
sf_df.hvplot.line(x = 'year', y = ['sale_price_sqr_foot'],groupby = 'neighborhood')


# In[48]:


# Use hvplot to create an interactive line chart of the average monthly rent.
sf_df.hvplot.line(x = 'year', y = ['gross_rent'],groupby = 'neighborhood')


# ### Top Ten Most Expensive Neighborhoods
# 

# In[49]:


Expensive = sf_data.groupby(by= 'neighborhood').mean().sort_values(by = 'sale_price_sqr_foot', ascending = False, ).reset_index().iloc[:10,:]
Expensive


# In[57]:


# Plotting the data from the top 10 expensive neighborhoods
Expensive.hvplot.bar(x = 'neighborhood', y = 'sale_price_sqr_foot', rot = 90)


# In[59]:


# Fetch the previously generated DataFrame that was grouped by year and neighborhood
sf_df.head(10)


# #### Plotting the data from the top 10 expensive neighborhoods

# In[60]:


sf_df.hvplot.bar(x = 'neighborhood', y = 'sale_price_sqr_foot', rot = 90)


# In[63]:


sf_df.hvplot.bar(x = 'neighborhood', y = 'gross_rent', rot = 90)


# In[88]:


sf_df.hvplot.bar(x='year',  y=['sale_price_sqr_foot', 'gross_rent'], xlabel='Year',ylabel='Avg price, Gross rent', 
    groupby='neighborhood', rot=90)


# ### Neighborhood Map

# In[68]:


coordinates_df = pd.read_csv("neighborhoods_coordinates.csv")
coordinates_df.head()


# #### Data Preparation

# In[69]:


# Calculate the mean values for each neighborhood
sf_neighborhood_avg = sf_data.groupby(by = 'neighborhood').mean().reset_index()
sf_neighborhood_avg


# In[71]:


# Join the average values with the neighborhood locations
combined_df = pd.concat( [coordinates_df,sf_neighborhood_avg],axis = 1, join = 'inner').drop(columns = 'neighborhood')
combined_df.head()


# In[81]:


# Set the mapbox access token
px.set_mapbox_access_token("MAPBOX_TOKEN")


# In[87]:


map_plot = px.scatter_mapbox(
    combined_df,
    lat="Lat",
    lon="Lon",
    size="sale_price_sqr_foot",
    color="gross_rent",
    color_continuous_scale=px.colors.cyclical.IceFire,
    hover_name="Neighborhood",
    title="Average Sale Price Per SqFt & Gross Rent in San Francisco",
    zoom=11
)
map_plot.show()
#The map doesn't pop up for me specifically but I can see the stats when I scroll over it?


# ### Cost Analysis-Optional Challenge

# In[ ]:




