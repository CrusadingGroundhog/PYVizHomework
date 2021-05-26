#!/usr/bin/env python
# coding: utf-8

# ### San Francisco Rental Prices Dashboard

# In[16]:


# imports
import panel as pn
pn.extension('plotly')
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
import os
from pathlib import Path
from dotenv import load_dotenv


# In[17]:


# Read the Mapbox API key
load_dotenv()
map_box_api = os.getenv("MAPBOX_TOKEN")
px.set_mapbox_access_token(map_box_api)


# #### Data

# In[18]:


sf_data = pd.read_csv("sfo_neighborhoods_census_data.csv", index_col="year")
coordinates_df = pd.read_csv("neighborhoods_coordinates.csv")


# In[47]:


#housing_units_per_year
def get_housing_units_per_year():
    housing_units_per_year = sf_data.groupby('year')['housing_units'].mean().hvplot.bar(xlabel="Year", ylabel="Housing Units",ylim=(370000,385000), title="Housing Units Per Year")
    return housing_units_per_year


# In[48]:


#average_gross_rent
def average_gross_rent():
    average_gross_rent = sf_data.groupby('year')['gross_rent'].mean().hvplot.line(xlabel='Year', ylabel='Gross Rent', title='Average Gross Rent in SF')
    return average_gross_rent


# In[49]:


#average_sales_price
def get_average_sales_price():
    average_sales_price = sf_data.groupby('year')['sale_price_sqr_foot'].mean().hvplot.line(xlabel='Year', ylabel='Average Sales Price', title='Average Sale Price Per Year')
    return average_sales_price


# In[50]:


#Average_Price_by_Neighborhood
multiple_neighborhood = sf_data.groupby(['year','neighborhood']).mean()
def get_average_price_by_neighborhood():
    average_price_by_neighborhood = multiple_neighborhood.hvplot.line(x='year', y='sale_price_sqr_foot', groupby='neighborhood')
    return average_price_by_neighborhood


# In[51]:


#top_most_expensive_neighborhood
multiple_neighborhood_mean = multiple_neighborhood.groupby(['neighborhood']).mean()
multiple_neighborhood_mean_plot = multiple_neighborhood_mean.sort_values('sale_price_sqr_foot', ascending=False).head(10)

#most expensive neighborhoods function
def get_top_most_expensive_neighborhoods():
    top_most_expensive_neighborhoods = multiple_neighborhood_mean_plot.head(10).plot(kind='bar', y='sale_price_sqr_foot', title="Top 10 Most Expensive Neighborhoods.")
    return top_most_expensive_neighborhoods


# In[52]:


#parallel_coordinates

def get_parallel_coordinates():
    parallel_coordinates = px.parallel_coordinates(multiple_neighborhood_mean_plot, color='sale_price_sqr_foot', title="Parallel Coordinates Plot.")
    return parallel_coordinates


# In[53]:


#parallel categories function
def get_parallel_categories():
    parallel_categories = px.parallel_categories(
    multiple_neighborhood_mean_plot,
    dimensions=["sale_price_sqr_foot", "housing_units", "gross_rent"],
    color="sale_price_sqr_foot",
    color_continuous_scale=px.colors.sequential.Inferno,
    labels={
        "sale_price_sqr_foot": "Sale Price/sqft",
        "housing_units": "Housing Units",
        "gross_rent": "Gross Rent",
    },
)


# In[54]:


#mean values for each neighborhood
coordinates_df_mean = coordinates_df.groupby(['Neighborhood']).mean()

#combine two neighborhoods 
joined_df = pd.concat([multiple_neighborhood_mean, coordinates_df_mean], axis='columns', join='inner')

#neighorhood function
def get_neighborhood_map(): 
    neighborhood_map = px.scatter_mapbox(joined_df, lat="Lat", lon="Lon", size="gross_rent", color="gross_rent")
    return neighborhood_map


# In[55]:


#Basic data column
basic_column = pn.Column(
    "##SF Housing Data", 
    get_housing_units_per_year(), 
    get_average_gross_rent(), 
    get_average_sales_price(),
)

#Neighborhood column
neigborhood_column = pn.Column(
    "##SF Neighborhood Data",
    get_average_price_by_neighborhood(), 
    get_top_most_expensive_neighborhoods(),
)

#Interactive column
interactive_column = pn.Column(
    "SF Interactive Data",
    get_parallel_coordinates(),
    get_parallel_categories()
)

#Map column
map_column = pn.Column(
    "SF Map",
    get_neighborhood_map(),
)

# Create tabs
dashboard = pn.Tabs(
    ("Housing Data", basic_column), ("Neighborhood Data", neigborhood_column), ("Interactive Data", interactive_column), ("SF Map", map_column)
)


# In[57]:


dashboard.servable()


# ### Test

# In[56]:


housing_units_per_year


# In[60]:


average_sales_price


# In[ ]:




