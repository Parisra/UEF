# -*- coding: utf-8 -*-

"""
This script retrieves raw data files from the inverters datalogger, 
creates a data file named 'clean_data.csv' and 
stores it in the folder 'resources'.
"""

import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def retrieve_inverter(data_path, clean_dataframe, inverter, start_date, end_date, tz): 

    """
    Retrieve inverters data (collected trough solar fussion)
    """

    #index to read the datafiles, one datafile per month, 
    time_index_month = pd.date_range(start=start_date, 
                                     end=end_date, 
                                     freq='M',  
                                     tz=tz)
    
    for m in time_index_month:
    
        fn='Inverter_{}_{}_{}.xlsx'.format(inverter,m.year, str(m.month).zfill(2))
        print('retrieving ' + fn)
        input_data = pd.read_excel((data_path + fn),
                                   sheet_name="5 minutes", 
                                   index_col=3, 
                                   header=0, 
                                   skiprows=3,
                                   engine='openpyxl').squeeze("columns")
    
        input_data.index = pd.to_datetime(input_data.index).tz_localize(tz=tz)

        clean_data.loc[input_data.index,['Inverter {} Total input power (kW)'.format(inverter)]] = input_data['Total input power(kW)']
        for pv_string in [1,2,3,4,5,6,7,8]:
            clean_data.loc[input_data.index,['Inverter {} PV{} input current(A)'.format(inverter,pv_string)]] = input_data['PV{} input current(A)'.format(pv_string)]
            clean_data.loc[input_data.index,['Inverter {} PV{} input voltage(V)'.format(inverter,pv_string)]] = input_data['PV{} input voltage(V)'.format(pv_string)]



    clean_data.to_csv('resources/clean_data.csv')
    return clean_data
    
# Create empty dataframe to be populated
tz = 'UTC' 
start_date = '2024-09-01 00:00:00'
end_date = '2025-04-23 23:55:00'
time_index = pd.date_range(start=start_date, 
                               end=end_date, 
                               freq='5min',  
                               tz=tz)
clean_data=pd.DataFrame(index=time_index)   

time_index_hour = pd.date_range(start=start_date, 
                                end=end_date, 
                                freq='H',  
                                tz=tz)

#retrieve data from inverters, dateindex in CET/CEST (indicated by DST)
data_path='data/inverter_monthly_datafiles/'
for inverter in [1,2]:
    clean_data = retrieve_inverter(data_path, 
                                   clean_data, 
                                   inverter=inverter,
                                   start_date = '2024-09-03 00:00:00', 
                                   end_date = end_date, 
                                   tz='CET')


# Plot summary of available clean data
clean_data_plot=clean_data.astype(float)
plt.subplots(figsize=(20,15))
ax = sns.heatmap(clean_data_plot.loc[time_index_hour].abs()/clean_data_plot.loc[time_index_hour].abs().max(), 
                 cmap="plasma", mask=clean_data_plot.loc[time_index_hour].isnull())
ticklabels = [time_index_hour[int(tick)].strftime('%Y-%m-%d') for tick in ax.get_yticks()]
ax.set_yticklabels(ticklabels);
plt.savefig('Figures/summary_clean_data.jpg', dpi=300, bbox_inches='tight')

