#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jdavis
"""
import os

import pandas as pd
import geopandas as gpd

from slugify import slugify


datafile = os.path.expanduser('/Users/jdavis/Downloads/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_10576830/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_10576830.csv')
shapefile = os.path.expanduser('/Users/jdavis/Downloads/ne_10m_admin_0_countries_lakes (1)')

colors = 9
cmap = 'Reds'
figsize = (16, 10)
year = '2014'
cols = ['Country Name', 'Country Code', year]
title = 'GDP (in 2019 USD) in {}'.format(year)

imgfile = 'img/{}.png'.format(slugify(title))


gdf = gpd.read_file(shapefile)[['ADM0_A3', 'geometry']].to_crs('+proj=robin') 
gdf.sample(5)

df = pd.read_csv(datafile, skiprows=4, usecols=cols, engine='python') 
df.sample(5)

merged = gdf.merge(df, left_on='ADM0_A3', right_on='Country Code') 
merged.describe()

ax = merged.dropna().plot(column=year, cmap=cmap, figsize=figsize, scheme='equal_interval', k=colors, legend=True)

merged[merged.isna().any(axis=1)].plot(ax=ax, color='#fafafa', hatch='///')

ax.set_title(title, fontdict={'fontsize': 16}, loc='center') 

ax.set_axis_off() 
ax.set_xlim([-1.5e7, 1.7e7]) 
ax.get_legend().set_bbox_to_anchor((.12, .4)) 
ax.get_figure()
