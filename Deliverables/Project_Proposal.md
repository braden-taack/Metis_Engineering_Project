___
Braden Taack
###  Emissions Engineering Project Proposal
#### October 6th, 2021
___
  

#### Question/need:
* What is the framing question of your analysis, or the purpose of the model/system you plan to build?   
  
  Global emissions are a constantly growing issue as climate change continues to intensify. Emissions are a key contributor to climate change and as we move forward it will be as important as ever to track them. The goal of this project is to leverage the [Emissions API](https://emissions-api.org/) data source into an interactive dashboard to allow users to view different basic statistics on country emission data. 

* Who benefits from exploring this question or building this model/system?  
  
  Anyone interested in focusing in on the global emissions issue could use this dashboard to analyze different country's emissions data. 

#### Data Description:
* What dataset(s) do you plan to use, and how will you obtain the data?  
  
  I plan to pull in data using the [Emissions API](https://emissions-api.org/). It is a free, open-source API that will allow me to gather daily emission data by country for the following compounds: CO, NO2, O3, and CH4. The first data dates back to Dec 31st, 2018, so I will attempt to create my initial database based on that data for at least 10 countries. I am hoping to continue to gather data on a weekly basis to continue to grow the project.  
  
* What is an individual sample/unit of analysis in this project? What characteristics/features do you expect to work with?  
  
  An individual sample will consist of a daily summary for a single compound for a country. The unit of measurement for each of the compounds will be in mol/m2. The features associated with the sample will be: date, country, average, max, min, and standard deviation. The reason for these aggregates is that the API collects satellite data and summarizes 10s to 1000s of data points into regions. 
  
* If modeling, what will you predict as your target? 

  Provided enough time for completion, other country or city data could be included such as population, GDP, etc into a basic linear model. The goal of this model would be to offer interpretable features and predictive power on future emissions from growing nations. Modeling will likely be considered under future work for this project.    
  
#### Tools:
* How do you intend to meet the tools requirement of the project?  
  
  I plan to create the dataset by leveraging the Emissions API linked above. To meet the data requirement, I plan to scrape enough countries to meet the 100,000 datapoint mark. For easy json conversion, I plan to start by ingesting the data into a mongo database. Data cleaning will either be done in mongo or pandas dataframes, depending if a size bottleneck is present. Data visualization will be done with plotly. A final interactive dashboard made with Dash using the plotly graphs will be created as well.  

#### MVP Goal:
* What would a [minimum viable product (MVP)](./mvp.md) look like for this project?  
  
  The goal for the MVP will have completed running through the API to create the initial emissions database. Data cleanup and some basic feature engineering will be performed. Lastly, basic plots such as emissions for a country for the previous month will be created and viewable on a working dashboard. 
  
#### Alternate Project Idea:
  
My alternative project idea will be working with Wikipedia page visit information obtained via the [WikiMedia Rest API](https://wikitech.wikimedia.o/wiki/Analytics/AQS/Pageviews) The goal of this project will be to ingest large amounts of Wikipedia page view data and perform interesting exploratory data analysis. The most interesting results will be posted to an interactive dashboard.  
