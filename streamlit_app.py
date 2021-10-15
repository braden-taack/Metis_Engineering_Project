'''
Make sure to install streamlit with `conda install -c conda-forge streamlit`.

Run `streamlit hello` to get started!

Streamlit is *V* cool, and it's only going to get cooler (as of February 2021):

https://discuss.streamlit.io/t/override-default-color-palette/9088/2

To run this app, run `streamlit run streamlit_app.py` from inside this directory
'''

#import necessary libraries 
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle as pkl
import datetime
import requests
import pymongo

#set page configuration settings
#use this for cloud icon 'https://cdn-icons-png.flaticon.com/512/616/616682.png'
st.set_page_config(layout="wide", page_title = 'Air Quality Dashboard', 
    page_icon ='https://emoji.slack-edge.com/T01MF50RVGV/party-blob/16b9ca5fe1f173c7.gif')
st.config.set_option('theme.base','light') #picture is light so need dark text for readability

#add background image manually
page_bg_img = '''
<style>
section {
    background-image: url("https://images.unsplash.com/photo-1582499571609-78fa6b420cba?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=2071&q=80");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)




#print headers and project description
st.write(
'''
# Air Quality Dashboard
The problem of global emissions and worsening air quality are growing issues as the demand for energy and other resources rise every year. It is a complicated matter and even more difficult without clear, interpretable data. My goal is to leverage satellite air quality data into a user-friendly, interactive dashboard. 

This dashboard covers 4 common pollutants: [methane (CH4)](https://www.epa.gov/gmi/importance-methane), [carbon monoxide (CO)](https://www.epa.gov/co-pollution), [ground-level ozone (O3)](https://www.epa.gov/ground-level-ozone-pollution), and [nitrogen dioxide (NO2)](https://www.epa.gov/no2-pollution). For more detailed information on the compounds and their effects as pollutants, please follow the links to their respective [EPA articles](https://www.epa.gov/)!

The data has been sourced from the [Emissions API](https://emissions-api.org/). The group's initiative is to help people access air quality data from the European Space Agency's Sentinel-5P satellite. 

The background image has been sourced from [Marcin Jozwiak's](https://unsplash.com/@marcinjozwiak) photo library on Unsplash.com.
___
''')

#import pickle data 
with open("Data/data.pkl",'rb') as f:
    df = pkl.load(f)
df = df.sort_values(by=['compound','country','time']) #not all time data is sorted correctly, sort for plotting

with open("Data/country_dict.pkl",'rb') as f:
    country_dict = pkl.load(f)
region_dict = {'Europe':1,'North_America':0}

with open("Data/location_df.pkl",'rb') as f:
    location_df = pkl.load(f)





#plot bar chart for various top 10 countries for pollution levels
st.write(
'''
### Top 10 Average Country Pollution Levels for CH4, CO, O3, and NO2 
Please select desired statistic, pollutant, and date range. Press apply button after changes are made.
'''
)
row0_1, row0_2, row0_3 ,row0_4 = st.columns(4)

#user selected statistic
with row0_1:
    stat = st.radio(
        "Choose Statistic",
        ('avg', 'max', 'min'))

#user selected pollutant
with row0_2:
    cmpd = st.radio(
        "Choose Pollutant",
        ('methane', 'carbonmonoxide', 'ozone','nitrogendioxide'))

#user selected date range, gray out dates that are not in df
with row0_3:
    try:
        begin_date, end_date = st.date_input(label='Select a date range',value=(datetime.date(2021,9,1),datetime.date(2021,10,1)),
                      min_value=datetime.date(2019,5,1), max_value=datetime.date(2021,10,1))
    except ValueError:
        begin_date, end_date = datetime.date(2021,9,1),datetime.date(2021,10,1)

#to avoid ValueErrors, have user hit apply for each change
with row0_4:
    st.empty()
    go = st.button('Apply Changes')
    if end_date - begin_date <  datetime.timedelta(days=2):
        st.write("The function is calculating an average and requires a minimum of 2 days. Please select at least 2 days.")
        go = False

#calculate top 10 data averages and update plot
if go:
    mask = ((df['compound']==cmpd) & (df['time'] > begin_date) & (df['time'] < end_date))
    mean_df = df[mask].groupby(by=['compound','country'],as_index= False).mean().sort_values(by=[stat], ascending = False).head(10)
    fig_bar = px.bar(x = 'country', y = stat, title = f"Average {cmpd} Value ({begin_date} to {end_date})", labels = {stat:f"{cmpd} (mol/m3)"},
           color = 'country', data_frame = mean_df)
    go = False
    st.plotly_chart(fig_bar,use_container_width=True)
    




#plot line charts for each compound given a region and country input from the user
st.write(
'''
---
### Historical Line Charts for CH4, CO, O3, and NO2 by Country
Select desired region and country to output plots for the pollutants. Please note that some countries may not have data available from the API. 
'''
)
row1_1, row1_2, row1_3= st.columns(3)

with row1_2:
    region_0 = st.selectbox('Please select a region',('Europe','North_America'))
    country_0 = st.selectbox('Please select a country',(country_dict[region_dict[region_0]].keys()))

row2_1,row2_2= st.columns(2)

with row2_1:
    cmpd_0 = 'methane'
    mask_0 = ((df['compound']==cmpd_0) & (df['country']==country_dict[region_dict[region_0]][country_0]))
    fig_0 = px.line(x = 'time', y = 'avg', title = f"Daily Average {cmpd_0} Value", labels = {'time':'Date','avg':f"{cmpd_0} (mol/m3)"},
           data_frame = df[mask_0])
    st.plotly_chart(fig_0)

with row2_2:
    cmpd_1 = 'carbonmonoxide'
    mask_1 = ((df['compound']==cmpd_1) & (df['country']==country_dict[region_dict[region_0]][country_0]))
    fig_1 = px.line(x = 'time', y = 'avg', title = f"Daily Average {cmpd_1} Value", labels = {'time':'Date','avg':f"{cmpd_1} (mol/m3)"},
           color = 'country', data_frame = df[mask_1])
    st.plotly_chart(fig_1)

row3_1,row3_2= st.columns(2)

with row3_1:
    cmpd_2 = 'ozone'
    mask_2 = ((df['compound']==cmpd_2) & (df['country']==country_dict[region_dict[region_0]][country_0]))
    fig_2 = px.line(x = 'time', y = 'avg', title = f"Daily Average {cmpd_2} Value", labels = {'time':'Date','avg':f"{cmpd_2} (mol/m3)"},
           data_frame = df[mask_2])
    st.plotly_chart(fig_2)

with row3_2:
    cmpd_3 = 'nitrogendioxide'
    mask_3 = ((df['compound']==cmpd_3) & (df['country']==country_dict[region_dict[region_0]][country_0]))
    fig_3 = px.line(x = 'time', y = 'avg', title = f"Daily Average {cmpd_3} Value", labels = {'time':'Date','avg':f"{cmpd_3} (mol/m3)"},
           color = 'country', data_frame = df[mask_3])
    st.plotly_chart(fig_3)




#user input longitude and latitude, map with results from API
st.write(
'''
---
### Choose Lon & Lat and Return API Data
Choose your Latitude and Longitude to pull data from the API and plot it. 
'''
)
row4_1,row4_2, row4_3 = st.columns((1,1,2))

#find dates for today and a week ago
today = datetime.date.today()
last_week = today - datetime.timedelta(days = 7)

with row4_1:
    text = st.text_input('Input longitude and latitude as: lon,lat', value = '-73.935242,40.730610')
    lon, lat = text.split(',')
    lon, lat = float(lon), float(lat)
with row4_2:
    cmpd_4 = st.selectbox('Please select a pollutant',('methane','carbonmonoxide','ozone','nitrogendioxide'))
with row4_3:
    st.write('''Note that by selecting new pollutants or coordinates, you are actually adding to a shared database.
        Add your favorite locations for others to view too!  
        As of now, this data is only being collected 
        for the past week.''')

#connect to mongodb 
client = pymongo.MongoClient("mongodb://app:ZhZrJ6p4Wzs5t39@emissions-cluster-shard-00-00.pbc8n.mongodb.net:27017,emissions-cluster-shard-00-01.pbc8n.mongodb.net:27017,emissions-cluster-shard-00-02.pbc8n.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-kp9bdx-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.get_database('Emissions-Data')

#function grabs location based data from API, adds to mongodb, querries mongoDB, returns df
def get_loc_data(db,col,compound,lon,lat,begin_date,end_date):
    response = requests.get('https://api.v2.emissions-api.org/api/v2/'+compound+'/statistics.json?' +
                         'point='+str(lon)+'%2C'+str(lat)+'&interval=day&begin='+begin_date+'&end='+end_date+'&offset=0')
    res = response.json()
    res_list =[]
    #loop for multiple results
    for i in res:
        loc_dict = {'lat':lat,'lon':lon,'compound':compound,'time':i['time']['interval_start'],'avg':i['value']['average'],'max':i['value']['min'],
                'count':i['value']['count'],'min':i['value']['min'],'std':i['value']['standard deviation']}
        res_list.append(loc_dict)

    #add to mongodb
    if len(res_list) >= 1:
        input_i = db[col].insert_many(res_list)
    
    #query mongodb and return dataframe
    #pipeline to extract important info into pandas 
    pipeline = [{'$project':{'_id':0,'lon':1,'lat':1,'compound':1,'time':1, 'avg':1,'max':1,'min':1,'std':1,'count':1}}]
    return pd.DataFrame(list(db[col].aggregate(pipeline)))

#call function and get data
location_df = get_loc_data(db,'Data',cmpd_4,lon,lat,str(last_week),str(today))

row5_1,row5_2= st.columns(2)
with row5_1:
    st.map(location_df) #convet to df and plot, had issues with df
with row5_2:
    st.dataframe(location_df.style.set_properties(**{'background-color': 'white','border-color': 'white'}),)


#optionally show the dataframe used for the project
st.write(
'''
---
### View and Download Data
Select the checkbox to show a preview of the DataFrame. Click the button to download the entire DataFrame as a csv.
'''
)
show_df = st.checkbox('Show first 10 rows of Source Data', value=False)
rowlast_0, rowlast_space, rowlast_1 = st.columns((4,0.2,1))
if show_df:
    with rowlast_0:
        st.dataframe(df.head(10).style.set_properties(**{'background-color': 'white','border-color': 'white'}))
    
    #allow users to download data as csv
    with rowlast_1: 
        @st.cache
        def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='emissions_data.csv',
            mime='text/csv',
        )
