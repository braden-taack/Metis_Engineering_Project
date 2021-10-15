Braden Taack
### Air Quality Dashboard Engineering Project
#### October 15, 2021
---

#### Abstract
  
The goal of this project is to create an efficent data pipeline resulting in a user-friendly, interactive dashboard. The air quality data contains average pollutant concentrations by day sourced from the [Emissions API](https://emissions-api.org/). The data is initially stored in a mongo database but translated into a pandas dataframe for plotting with Plotly. The final product consists of an interactive dashboard built with Streamlit and deployed with Heroku. There are 4 main portions to the page that display basic EDA based graphics: top 10 concentrations by country, historical plots for all 4 pollutants, map and location inputs, and a space to download the data. Follow the link to view the [Air Quality Dashboard](https://metis-emissions-project.herokuapp.com/)!


#### Design

The problem of global emissions and worsening air quality are growing issues as the demand for energy and other resources rise every year. It is a complicated matter and even more difficult without clear, interpretable data. My goal is to leverage satellite air quality data into a user-friendly, interactive dashboard. 

This dashboard covers 4 common pollutants: [methane (CH4)](https://www.epa.gov/gmi/importance-methane), [carbon monoxide (CO)](https://www.epa.gov/co-pollution), [ground-level ozone (O3)](https://www.epa.gov/ground-level-ozone-pollution), and [nitrogen dioxide (NO2)](https://www.epa.gov/no2-pollution). For more detailed information on the compounds and their effects as pollutants, please follow the links to their respective [EPA articles](https://www.epa.gov/)!

#### Data
  
The data has been sourced from the [Emissions API](https://emissions-api.org/). The group's initiative is to help people access air quality data from the European Space Agency's Sentinel-5P satellite. Initially, data was collected from the API for all countries in Europe and North America for all 4 pollutants, and the data was stored into a local mongoDB. This initial data set contained 153,878 records from 2019-05-01 to 2021-10-01 with the following features: daily average, daily max, daily min, daily standard deviation, day, compound, and country. The data was restricted to this date range because this was the largest range available from the API at the time.
  
To get the dashboard working, the data was converted into a pandas dataframe and saved as a pickle object, which could be loaded into the webpage on the page request. Later, this would make more sense to include into a SQL database, either locally or on a cloud platform. 
  
A second database was created to handle the user requests while inputing latitude and longitude data for the mapping container on the dashboard. This is a cloud based mongoDB. When the user inputs new coordinates, data is called in from the API and stored into this cloud database. So, anyone will be able to view a map of all of the places queried by others. 

#### Algorithms
  
*Data Collection*  
    
All of the data for this project was collected from the [Emissions API](https://emissions-api.org/). This very cool service analyzes the satellite data for you and returns very easily interpretable values. The API required [Alpha-3 codes](https://www.iban.com/country-codes) when using country as an input. So, dictionaries for European countries, North American countries, and their respective codes was developed to be iterated through for different requests. 

To collect all of the initial data, a nested for loop structure was created to account for all combinations between the 4 pollutants and all of the countries (only 1 country and 1 pollutant could be called at once). 

A similar function was developed to collect the latitude/longitude based data for the map on the Streamlit application. However, a short pipeline was included into this function as it was intended to be repeatedly called. After requesting the API, the function cleans the messy, nested json data into a list of dictionaries. This list is then passed into the cloud mongoDB. Finally, the database is queried and the result is passed into a dataframe for use in the application. 

*Data Cleanup* 
  
Data Cleanup was a relatively simple process for this dataset. The main issue came from the structure of the json response from the API. There were several layers of nesting and undesired parameters. Seen in the example below, time.max, time.min, and grouping the data under 'values':{} was not necessary for this project. 

```json  
[
  {
    "time": {
      "interval_start": "2019-02-10T00:00:00Z",
      "max": "2019-02-10T20:33:51.270000Z",
      "min": "2019-02-10T17:10:06.712000Z"
    },
    "value": {
      "average": 1842.27966792409,
      "count": 328,
      "max": 1937.666259765625,
      "min": 1781.021240234375,
      "standard deviation": 21.21835560472388
    }
  }
]
```
After adding in additional query data, and the transforming the data via a pipeline and a mongo aggregation, the resulting format looked as such:
```{python}  
{'country': 'BLZ',
 'compound': 'methane',
 'time': '2019-07-02T00:00:00Z',
 'avg': 1848.2527262369792,
 'max': 1856.6776123046875,
 'min': 1834.5887451171875,
 'std': 11.940083799133346}
```
The last portion of data cleaning dealt with transforming the string under time to a datetime.date object and removing rows where avg == Null. 
  
*Streamlit Application*
1. Set Page Config Options
    - Add custom background image
    - Set theme to be light so text would show up better
    - Change page header and icon (for fun)
2. Import Local Data
    - Import country DataFrame and sort so dates are in order
    - Import country dictionaries 
3. Update Bar Plot
    - The Plotly bar plot data function uses a date range selection. The page would try and update once one of the dates was selected and then would error out because it would try to proceed with only 1 out of 2 date variables filled. To avoid this, I added a button to have the user manually tell the page to incorporate the new data that was selected. 
    - Because the API would not include the end date in the pull, and because the function required 2+ days to calculate the mean, at least 2 days were required to be selected. Additional error checking was added in to make sure appropriate days were being selected. 
    - The date selection tool was also limited to the max and min dates of the dataset. 
    - Additional selective options were also added for the kind of pollutant and statistic of choice (avg, max, or min). 
4. Plot Historical Trends
    - With so many countries involved (61), 2 selectboxes were made: region and country. The user could select a region, and then the list of countries would automatically update to choose a country from the given region. 
    - The 4 Plotly plots for CH4, CO, O3, and NO2 were then updated with the selected country. 
5. Map Scatter Plot Updates
    - Connect to Atlas MongoDB
    - get_loc_data
        1. Request API
        2. Loop through individual response. Convert into easy format as described in data cleaning
        3. Check if data exists, if so add to MongoDB
        4. Query MongoDB
        5. Save query to local pandas DataFrame
    - Plot with streamlit.map. Display updated DataFrame
6. Show and Download Data
    - Optionally show dataset
    - Download button with download added to cache for better performance
  
#### Tools

- [Emissions API v2](https://api.v2.emissions-api.org/ui/#/default/emissionsapi.web.get_statistics) for data source using Requests library
- pymongo for local country data storage 
- Atlas: MongoDB for cloud-based latitude/longitude data storage
- Pandas for data ingestion and basic exploration
- Numpy and Pandas for data manipulation
- datetime for cleaning time data
- Plotly for data visualization
- Streamlit for web application development
- Heroku for app deployment

#### Conclusions  
  
This was a very rewarding and fun project. I learned a lot about data engineering and look to learn more. As for my dashboard, I hope to explore it myself in search of valuable air pollution data. I am sure there is much more to discover from this data other than exploratory data analysis visualizations.  
  
I expect there to be some valuable nuggets of insight further in the dataset. In the future, I would like to look at adding a modeling element to the project. A time series model for a certain location could be useful for predictive features and comparisons to other locations. Secondly, I would like to set up the project to pull in data from all available countries and regions. Ideally, all of this data would be regularly updated on a weekly basis (the API adds new data every few days) and saved into a cloud database. 

