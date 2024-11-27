# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 14:49:09 2024

@author: marta.victoria.perez
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec 

data=pd.read_csv('resources/clean_data.csv',
                 index_col=0)

data.index = pd.to_datetime(data.index, utc=True) 

start_date = '2024-11-01 00:00:00'
end_date = '2024-11-15 00:00:00'
tz='UTC' 
time_index_day = pd.date_range(start=start_date, 
                                 end=end_date, 
                                 freq='D',  
                                 tz=tz)

for day in time_index_day:
    time_index = pd.date_range(start=day, 
                           periods=24*12*1, 
                           freq='5min',
                           tz=tz)
    
    # #power generation inverter
    # plt.figure(figsize=(8, 6))
    # gs1 = gridspec.GridSpec(1, 1)
    # ax0 = plt.subplot(gs1[0,0])
    # for inverter in [1,2]:
    #     ax0.plot(data['Inverter {} Total input power (kW)'.format(inverter)][time_index], 
    #            #color='dodgerblue',
    #            label='Inverter {} Total input power (kW)'.format(inverter))
    
    # # ax0.set_ylim([0,40])
    # # ax0.set_ylabel('DC Power (kW)')
    # plt.setp(ax0.get_xticklabels(), ha="right", rotation=45)
    # ax0.grid('--')
    # ax0.legend()
    # plt.savefig('Figures/daily_profiles/power_generation_{}_{}_{}.jpg'.format(day.year, str(day.month).zfill(2), str(day.day).zfill(2)), 
    #             dpi=100, bbox_inches='tight')
    
    #power generation per string
    plt.figure(figsize=(8, 6))
    gs1 = gridspec.GridSpec(1, 1)
    ax0 = plt.subplot(gs1[0,0])
    #inverter=1
    ls = {1:'-',
         2:'-'}
    
    n_modules_inverter_1 = {1:20,
                            2:20,
                            3:9,
                            4:9,
                            5:20,
                            6:20,
                            7:9,
                            8:9,}
    
    n_modules_inverter_2 = {1:6,
                            2:6,
                            3:19,
                            4:19, #no genera corriente
                            5:13,
                            6:13,
                            7:13,
                            8:13,}  #no genera corriente 
    mark = {1:'o',
            2:'+',
            3:'*',
            4:'^',
            5:'o',
            6:'+',
            7:'*',
            8:'^',}
    p_module_inverter_1 = 430 # Longi 
    p_module_inverter_2 = 550 # Maxeon
    v_module_inverter_1 = 29.97  #Longi @NOCT
    v_module_inverter_2 = 43.08  #Maxeon @NOCT
    for inverter in [2]:
        n_modules = n_modules_inverter_1 if inverter==1 else n_modules_inverter_2
        p_module = p_module_inverter_1 if inverter==1 else p_module_inverter_2
        v_module = v_module_inverter_1 if inverter==1 else v_module_inverter_2
        for pv_string in [1,2,3,4,5,6,7,8]:
            ax0.plot(
                     (
                          #data['Inverter {} PV{} input current(A)'.format(inverter,pv_string)][time_index]),
                          1/(v_module)*data['Inverter {} PV{} input voltage(V)'.format(inverter,pv_string)][time_index]), 
                          label='Inverter-{} PV string-{}'.format(inverter,pv_string),
                          linestyle=ls[inverter],
                          marker=mark[pv_string],
                          alpha=0.7)
    
    #ax0.set_ylim([0,10])
    ax0.set_xlim(time_index[0], time_index[-1])
    #ax0.set_ylabel('relative DC Power (kW)')
    ax0.set_ylabel('number of PV modules')
    plt.setp(ax0.get_xticklabels(), ha="right", rotation=45)
    ax0.grid('--')
    ax0.legend(loc=(1.01,0.1))
    plt.savefig('Figures/daily_profiles/voltage_inv2_{}_{}_{}.jpg'.format(day.year, str(day.month).zfill(2), str(day.day).zfill(2)), 
                dpi=100, bbox_inches='tight')


   