#########################################################################################
#############                                                               #############
#############      Browser visualization Python Script - Uilson Bonfim      #############
#############                                                               #############
#########################################################################################

# %%
# Importing library that will be used in this scipt

import pandas as pd
import matplotlib.pyplot as plt, mpld3

# %%
# Import dataset file from CSV

country_serie = pd.read_csv('./dataset/WDICountry-Series.csv')
country = pd.read_csv('./dataset/WDICountry.csv')
data = pd.read_csv('./dataset/WDIData.csv')
series_time = pd.read_csv('./dataset/WDISeries-Time.csv')
series = pd.read_csv('./dataset/WDISeries.csv')
# %%
# Formatting 'data' dataset in order do merge to 'series' dataset

new_data = data.drop(
    ['Indicator Name', 'Unnamed: 65'], axis = 1
    ).melt(id_vars = ['Country Name', 'Country Code', 'Indicator Code']
    ).rename(columns = {
            'Country Code' : 'country_code',
            'Country Name' : 'country_name',
            'Indicator Code' : 'indicator_code',
            'variable' : 'year',
            'value' : 'data'}
    )

# %%
# Selecting variables related to Land Use in order to generate charts from it
# Formatting 'series' dataset in order do merge to 'data' dataset

features_selected = series.loc[
        [0, 22, 3, 4, 17, 237, 238, 243, 244, 601]].drop(
        columns = series.columns[5:], axis = 0
         ).rename(columns = {
                'Series Code' : 'indicator_code',
                'Topic' : 'topic',
                'Indicator Name' : 'indicator_name',
                'Short definition' : 'short_definition',
                'Long definition' : 'long_definition'}
)
# %%
# Merging 'data' and 'series' dataset

result = (
    features_selected
    .merge(
        new_data,
        on = 'indicator_code',
        how = 'left'
    )
)
# %%
# In order to present in a simply way to display charts on Brower a specific view was selected:
# Selecting top 10 countries with highest Agriculture, forestry, and fishing, value added per worker in 2019 (most recent year containg info)

countries_selected = result[(result.year == '2019') & (result.indicator_code == 'NV.AGR.EMPL.KD')].sort_values(by = 'data', ascending = True)[:10]

indicator_name = pd.DataFrame(countries_selected.indicator_name).iloc[1].values

# %%
# Creating a chart from the select data

fig, ax = plt.subplots(figsize = (20, 10))

bars = ax.barh(
        countries_selected.country_name, 
        countries_selected.data
    )
ax.set_title(f'Top 10 Countries with highest {indicator_name}'
    )

ax.set_xlabel(f'{indicator_name}')
ax.set_ylabel('Country')

# %%
# Displaying HTML code to embeed on WebSite

print(mpld3.fig_to_html(fig, template_type="simple"))

# %%
# Exporting HTML Code naming index.html

html_str = mpld3.fig_to_html(fig)
Html_file= open("index.html","w")
Html_file.write(html_str)
Html_file.close()

# %%
# Plotting data in a browser

mpld3.enable_notebook()
mpld3.show()
