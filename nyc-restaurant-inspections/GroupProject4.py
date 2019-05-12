#!/usr/bin/env python
# coding: utf-8

# # Group Project 2

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os

from bokeh.plotting import figure, output_file
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool, Select
from bokeh.io import show, output_notebook, push_notebook, curdoc
from bokeh.transform import dodge, factor_cmap
from bokeh.core.properties import value
from bokeh.palettes import Spectral10
from bokeh.layouts import Row, Column
from scipy.interpolate import interp1d
from ipywidgets import interact
#from datetime import datetime

output_notebook()


# In[2]:


data_df = pd.read_csv("DOHMH_New_York_City_Restaurant_Inspection_Results.csv")


# In[3]:


# column names of dataset
data_df.columns
print(data_df['CUISINE DESCRIPTION'].unique())


# In[4]:


# summary of dataset
data_df.info()


# In[5]:


def upBoroLine(attr, old, new):
    print(old, new)
    dfCuisine = df2[df2.CUISINE_DESCRIPTION == CSelect.value]
    cds.data=dict(INSPECTION_DATE=dfCuisine['INSPECTION_DATE'],
                                 BRONX=dfCuisine['BRONX'],
                                 BROOKLYN=dfCuisine['BROOKLYN'],
                                 MANHATTAN=dfCuisine['MANHATTAN'],
                                 QUEENS=dfCuisine['QUEENS'],
                                 STATEN_ISLAND=dfCuisine['STATEN_ISLAND'],
                                 CUSINE_DESCRIPTION=dfCuisine['CUISINE_DESCRIPTION'],
                                 DATESTRING=dfCuisine['DATESTRING']
                                 )

#Used as a set list for drop down
df3 = data_df    
df3['CUISINE DESCRIPTION']= df3['CUISINE DESCRIPTION'].replace("Latin (Cuban, Dominican, Puerto Rican, South & Central American)","Latin").replace("CafÃ©/Coffee/Tea","Cafe/Coffe/Tea")    


df2 = df3
df2['INSPECTION DATE'] = pd.to_datetime(df2['INSPECTION DATE'], format = '%m/%d/%Y')
df2 = df2.groupby(['INSPECTION DATE','CUISINE DESCRIPTION','BORO'])['VIOLATION CODE'].count()
df2 = df2.unstack()
df2 = df2.fillna(0)

df2 = df2.reset_index()
df2 = df2[df2['INSPECTION DATE'].dt.year >= 2015]
df2 = df2.groupby(['CUISINE DESCRIPTION', pd.Grouper(key='INSPECTION DATE', freq='W')])['BRONX', 'BROOKLYN', 
                                                               'MANHATTAN', 'QUEENS', 'STATEN ISLAND'].sum()
df2 = df2.reset_index()
df2.rename(columns={'INSPECTION DATE': 'INSPECTION_DATE', 'STATEN ISLAND': 'STATEN_ISLAND', 'CUISINE DESCRIPTION' : 'CUISINE_DESCRIPTION'}, inplace=True)
df2['DATESTRING'] = df2["INSPECTION_DATE"].dt.strftime("%m-%d-%Y")
#df2.set_index('INSPECTION_DATE')
df6 = df2[df2.CUISINE_DESCRIPTION == 'American']
cds = ColumnDataSource(data=dict(INSPECTION_DATE=df6['INSPECTION_DATE'],
                                 BRONX=df6['BRONX'],
                                 BROOKLYN=df6['BROOKLYN'],
                                 MANHATTAN=df6['MANHATTAN'],
                                 QUEENS=df6['QUEENS'],
                                 STATEN_ISLAND=df6['STATEN_ISLAND'],
                                 CUSINE_DESCRIPTION=df6['CUISINE_DESCRIPTION'],
                                 DATESTRING=df6['DATESTRING']
                                 ))

#df2 = df2/1000
print(df2)


# # Building Line Chart

# In[6]:


p = figure(title = '# OF INSPECTIONS BY YEAR', x_axis_label = 'YEAR', y_axis_label = '# OF INSPECTIONS', 
           plot_width=900, plot_height=500, x_axis_type='datetime')
p.line(x='INSPECTION_DATE', y='BRONX', color = 'red', alpha = 0.5, line_width = 2, 
       legend=value('BRONX'), source = cds)

p.line(x='INSPECTION_DATE', y='BROOKLYN', color = 'blue', alpha = 0.5, line_width = 2, 
       legend=value('BROOKLYN'), source = cds)

p.line(x='INSPECTION_DATE', y='MANHATTAN', color = 'orange', alpha = 0.5, line_width = 2, 
       legend=value('MANHATTAN'), source = cds)

p.line(x='INSPECTION_DATE', y='QUEENS', color = 'green', alpha = 0.5, line_width = 2, 
       legend=value('QUEENS'), source = cds)

p.line(x='INSPECTION_DATE', y='STATEN_ISLAND', color = 'black', alpha = 0.5, line_width = 2, 
       legend=value('STATEN ISLAND'), source = cds)

p.legend.location = "top_left"

#hover = p.select(dict(type=HoverTool))
HoverMe = [
    ('Bronx #of Insp','@BRONX'),
    ('Brooklyn #of Insp','@BROOKLYN'),
    ('Manhattan #of Insp','@MANHATTAN'),
    ('Queens #of Insp','@QUEENS'),
    ('Staten Island #of Insp','@STATEN_ISLAND'),
    ('Week Ending','@DATESTRING')
    ]

#Adding Dropdown widget for use with line chart
CSelect=Select(title="Select to filter by Borough",
                 options=list(sorted(df3['CUISINE DESCRIPTION'].unique())),
                 value='American')

CSelect.on_change('value', upBoroLine)

p.add_tools(HoverTool(tooltips=HoverMe))
#output_file('inspections-by-year.html')
#show(p)
#show(CSelect)


# # LINE CHART 2

# # Line Chart with Widgets

# In[7]:


def updateLine(attr, old, new):
    print(old, new)
    dfNew = df4[(df4.BORO == lineSelect.value) & (df4.CUISINE_DESCRIPTION == CSelect.value)]
    cds2.data=dict(BORO=dfNew['BORO'],
                                 CUISINE_DESCRIPTION=dfNew['CUISINE_DESCRIPTION'],
                                 INSPECTION_DATE=dfNew['INSPECTION_DATE'],
                                 A=dfNew['A'],
                                 B=dfNew['B'],
                                 C=dfNew['C'],
                                 P=dfNew['P'],
                                 Z=dfNew['Z'],
                                 DATESTRING=dfNew['DATESTRING']
                                 )
    #push_notebook(handle=t)
df4 = df3
df4['INSPECTION DATE'] = pd.to_datetime(df4['INSPECTION DATE'], format = '%m/%d/%Y')
df4 = df4.groupby(['INSPECTION DATE','CUISINE DESCRIPTION','BORO','GRADE'])['VIOLATION CODE'].count()
df4 = df4.unstack()
df4 = df4.fillna(0)

df4 = df4.reset_index()
df4 = df4[df4['INSPECTION DATE'].dt.year >= 2015]
df4 = df4.groupby(['BORO', 'CUISINE DESCRIPTION', pd.Grouper(key='INSPECTION DATE', freq='W')])['A', 'B', 
                                                               'C', 'P','Z'].sum()
df4 = df4.reset_index()
df4.rename(columns={'INSPECTION DATE' : 'INSPECTION_DATE', 'CUISINE DESCRIPTION' : 'CUISINE_DESCRIPTION'}, inplace=True)
df4['DATESTRING'] = df4["INSPECTION_DATE"].dt.strftime("%m-%d-%Y")

df5 = df4[(df4.BORO == 'MANHATTAN') & (df4.CUISINE_DESCRIPTION == 'American')]
cds2 = ColumnDataSource(data=dict(BORO=df5['BORO'],
                                 CUISINE_DESCRIPTION=df5['CUISINE_DESCRIPTION'], 
                                 INSPECTION_DATE=df5['INSPECTION_DATE'],
                                 A=df5['A'],
                                 B=df5['B'],
                                 C=df5['C'],
                                 P=df5['P'],
                                 Z=df5['Z'],
                                 DATESTRING=df5['DATESTRING']
                                 ))


# # Setup Figure

# In[8]:


p3 = figure(title = '# OF INSPECTIONS BY YEAR', x_axis_label = 'YEAR', y_axis_label = '# OF INSPECTIONS', 
           plot_width=900, plot_height=500, x_axis_type='datetime', x_range=p.x_range)
p3.line(x='INSPECTION_DATE', y='A', color = 'red', alpha = 0.5, line_width = 2, 
       legend=value('A'), source = cds2)

p3.line(x='INSPECTION_DATE', y='B', color = 'blue', alpha = 0.5, line_width = 2, 
       legend=value('B'), source = cds2)

p3.line(x='INSPECTION_DATE', y='C', color = 'orange', alpha = 0.5, line_width = 2, 
       legend=value('C'), source = cds2)

p3.line(x='INSPECTION_DATE', y='P', color = 'yellow', alpha = 0.5, line_width = 2, 
       legend=value('P'), source = cds2)

p3.line(x='INSPECTION_DATE', y='Z', color = 'purple', alpha = 0.5, line_width = 2, 
       legend=value('Z'), source = cds2)

p3.legend.location = "top_left"

HoverP3 = [('A','@A'),('B','@B'),('C','@C'),('P','@P'),('Z','@Z'),('Week Ending','@DATESTRING')]
p3.add_tools(HoverTool(tooltips=HoverP3))

#Adding Dropdown widget for use with line chart
lineSelect=Select(title="Select to filter by Borough",
                 options=['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND'],
                 value='MANHATTAN')

lineSelect.on_change('value', updateLine)
CSelect.on_change('value', updateLine)

#show(Column(lineSelect,p3))
#show(Column(p, lineSelect, p3))
#output_file('inspections-by-year.html')
curdoc().add_root(Column(CSelect, p, lineSelect, p3))