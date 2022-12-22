from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests
import plotly.express as px


def create_premade_layout(layout, data1, type = ''):

    data = data1

    if layout == '2d-layout-1':

        ## get symbols 
        symbols = [x['ASSET'] for x in data]
        all_symbols = []
        for i in symbols:
            if i not in all_symbols:
                all_symbols.append(i)

        ## drop text box 
        symbols = st.multiselect("", all_symbols, all_symbols[:9])
        st.text("")

        ## sort data 
        vol_data = {}
        vol_data_sum = {}
        date_data = []
        vol = []
        asset = ''
        for x in data:
            if x['ASSET'] in symbols:
                if not x['ASSET'] == asset:
                    if asset == '':
                        asset = x['ASSET']
                    else:
                        vol_data_sum[asset] = sum(vol)
                        vol_data[asset] = vol
                        asset = x['ASSET']
                        
                    vol = []
                    vol.append(x['SWAP_VOLUME'])
                    date_data = []
                    date_data.append(x['DAY'])
                else:
                    date_data.append(x['DAY'])
                    vol.append(x['SWAP_VOLUME'])

        vol_data[asset] = vol           
        symbols.sort()

        ## create data frames
        chart = pd.DataFrame(
            vol_data,
            index=date_data
        )

        chart2 = pd.DataFrame(
            [sum(vol_data[x])/12 for x in vol_data],
            index=[x for x in vol_data]
        )

        ## place data frame 
        if type == 'line':
            st.line_chart(chart)
        elif type == 'bar':
            st.bar_chart(chart)
        elif type == 'area':
            st.area_chart(chart)
        else:
            st.area_chart(chart)
            
        st.bar_chart(chart2)
        
    elif layout == 'pie-layout-1':
        ### data needs to made like {BIG_CATEGORY, SMALL_CATEGORY, VALUE}
        symbols = [x['BIG_CATEGORY'] for x in data]
        big_category = []
        for i in symbols:
            if i not in big_category:
                big_category.append(i)
                
        symbols3 = st.selectbox("", big_category)

        df = [x for x in data if x['BIG_CATEGORY'] == symbols3]
        if len(df) > 10:
            df = sorted(df, key=lambda x: x['VALUE'], reverse=True)
            df = df[0:10]
        
        fig = px.pie(df, values='VALUE', names='SMALL_CATEGORY')
        st.plotly_chart(fig, use_container_width=True)






def sort_flipside_api(link, bridge, type, chain):
    #sort TVL_data 
    if type == 'TVL':

        data = requests.get(link).json()
        data_list = []
        for x in data:
            ##data if 
            if "TVL_USD" in x:
                amount = x['TVL_USD']
            elif "TVL" in x:
                amount = x['TVL']
            elif "BALANCE" in x:
                amount = x['BALANCE']
            elif "BALANCE_USD" in x:    
                amount = x['BALANCE_USD']    
               
            ## token if 
            if "TOKEN" in x:
                token = x['TOKEN']
            elif "SYMBOL" in x:
                token = x['SYMBOL']
                
            ## time if 
            if "WEEK" in x:
                day1 = x['WEEK']
            else:
                day1 = x['DAY']
              

            #print(x)
            clean_dict = {'DAY':day1, 'TOKEN':token, 'BRIDGE':bridge, 'CHAIN':chain, 'VOLUME':amount}
            data_list.append(clean_dict)

        return data_list

    if type == 'VOLUME':

        data = requests.get(link).json()
        data_list = []
        for x in data:
            
                ##data if 
                if 'OUT_VOLUME' in x:
                    amount = x['OUT_VOLUME']
                if 'AMT_OUT' in x:
                    amount = x['AMT_OUT']
                if 'VOLUME' in x:
                    amount = x['VOLUME']
                if 'VOL_USD_OUT' in x:
                    amount = x['VOL_USD_OUT']

                clean_dict = {'DAY':x['DAY'], 'BRIDGE':bridge, 'CHAIN':chain, 'VOLUME':amount}
                data_list.append(clean_dict)

        return data_list

    if type == 'USERS':

        data = requests.get(link).json()
        data_list = []
        for x in data:
            
                ##data if 
                if 'USERS' in x:
                    amount = x['USERS']
                if 'USER' in x:
                    amount = x['USER']
                if 'TOTAL_UNIQUE_USERS' in x:
                    amount = x['TOTAL_UNIQUE_USERS']
                #if 'VOLUME' in x:
                #    amount = x['VOLUME']
                #if 'VOL_USD_OUT' in x:
                #    amount = x['VOL_USD_OUT']
                clean_dict = {'DAY':x['DAY'], 'BRIDGE':bridge, 'CHAIN':chain, 'VOLUME':amount}
                data_list.append(clean_dict)

        return data_list


## sort all data here
volume_api_list = [ 
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/fdf997c5-7919-457d-9a1d-1e00d9893417/data/latest', 'Bridge':'Stargate', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/83dc8c1c-c201-4db8-ae5f-f09a018b622b/data/latest', 'Bridge':'Stargate', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/be86d39e-03cd-4e64-ac15-fb73a1d465a9/data/latest', 'Bridge':'Stargate', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/921cb1e3-ac92-44b1-abd6-7fa3a28a0103/data/latest', 'Bridge':'Stargate', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/94e61d0e-94fe-4106-b0de-dbd6aed26870/data/latest', 'Bridge':'Stargate', 'Chain':'Arbitrum'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/fdf997c5-7919-457d-9a1d-1e00d9893417/data/latest', 'Bridge':'Hop', 'Chain':'Ethereum'},
    
   
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/14a003fa-2d2c-4230-9097-1ed9093b12a0/data/latest', 'Bridge':'Hyphen', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/0e4e52c4-2446-41a3-a1a9-1903ea40e886/data/latest', 'Bridge':'Hyphen', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/d1db5ed3-9354-49d2-aedf-181427250e61/data/latest', 'Bridge':'Hyphen', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/9e8066c8-1021-4dc8-80d6-97573b725910/data/latest', 'Bridge':'Hyphen', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/1bf70037-576f-424d-8c5e-22728d7ff6d3/data/latest', 'Bridge':'Hyphen', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/6a1c0cd6-ace1-4b8b-a585-9d1083df9c2f/data/latest', 'Bridge':'Hyphen', 'Chain':'BSC'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/40a97f66-196e-4b1c-becf-1d26457cf224/data/latest', 'Bridge':'Synapse', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/3313ad2e-95a0-418b-94b8-81b992627b3b/data/latest', 'Bridge':'Synapse', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/a3e782ce-6f67-4d44-9555-b94110ec2de3/data/latest', 'Bridge':'Synapse', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/7928274b-039c-443c-ab31-32e8b099449e/data/latest', 'Bridge':'Synapse', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/05a3d21c-bbd1-4bda-97ee-8607d760884b/data/latest', 'Bridge':'Synapse', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/310cbe64-415f-4403-aee6-5d14bc9571e2/data/latest', 'Bridge':'Synapse', 'Chain':'BSC'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/8a46a0f0-1d40-454a-a92b-1408aecba712/data/latest', 'Bridge':'Across', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/93904208-4440-4af8-a5fe-ffbc2c352525/data/latest', 'Bridge':'Across', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/28872bda-ab05-4f4d-9377-6ef8c6d562d6/data/latest', 'Bridge':'Across', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/6f685167-7a7e-479d-b263-691a2c6744ae/data/latest', 'Bridge':'Across', 'Chain':'Arbitrum'}
]

full_volume_list = []
full_volume_list2 = []
for api in volume_api_list:
    api_data_clean = sort_flipside_api(api['link'], api['Bridge'], 'TVL', api['Chain'])
    for x in api_data_clean:
        full_volume_list.append(x)




restructure_group_dict = {}
final_data_list1 = []
final_data_list2 = []
for x in full_volume_list:
    if x['VOLUME'] == None:
        x['VOLUME'] = 0
    if not x['DAY'] in restructure_group_dict:
        restructure_group_dict[x['DAY']] = {x['BRIDGE']:x['VOLUME']}
    else:
        if not x['BRIDGE'] in restructure_group_dict[x['DAY']]:
            restructure_group_dict[x['DAY']][x['BRIDGE']] = x['VOLUME']
        else:
            restructure_group_dict[x['DAY']][x['BRIDGE']] = restructure_group_dict[x['DAY']][x['BRIDGE']] + x['VOLUME']
            
#clean dict 
if len(restructure_group_dict) > 12: 
    pairs = list(restructure_group_dict.items())
    sorted_pairs = sorted(pairs, key=lambda x: x[0])
    repeat = len(restructure_group_dict) - 12
    for x in range(repeat):
        sorted_pairs.pop(0)
restructure_group_dict = dict(sorted_pairs)

for x in restructure_group_dict.keys():
    for y in restructure_group_dict[x].keys():
        final_dict = {'DAY':x, 'ASSET':y, 'SWAP_VOLUME': restructure_group_dict[x][y]}
        final_dict2 = {'BIG_CATEGORY':x, 'SMALL_CATEGORY':y, 'VALUE': restructure_group_dict[x][y]}
        final_data_list1.append(final_dict)
        final_data_list2.append(final_dict2)

final_data_list1 = sorted(final_data_list1, key=lambda  x:(x['ASSET'], x['DAY']), reverse=True) 
## make diffrent graph 
restructure_group_dict2 = {}
final_data_list3 = []
for x in full_volume_list:
    if x['VOLUME'] == None:
        x['VOLUME'] = 0
    if not x['BRIDGE'] in restructure_group_dict2:
        restructure_group_dict2[x['BRIDGE']] = {x['CHAIN']:x['VOLUME']}
    else:
        if not x['CHAIN'] in restructure_group_dict2[x['BRIDGE']]:
            restructure_group_dict2[x['BRIDGE']][x['CHAIN']] = x['VOLUME']
        else:
            restructure_group_dict2[x['BRIDGE']][x['CHAIN']] = restructure_group_dict2[x['BRIDGE']][x['CHAIN']] + x['VOLUME']

for x in restructure_group_dict2.keys():
    for y in restructure_group_dict2[x].keys():
        final_dict = {'DAY':x, 'ASSET':y, 'SWAP_VOLUME': restructure_group_dict2[x][y]}
        final_dict3 = {'BIG_CATEGORY':x, 'SMALL_CATEGORY':y, 'VALUE': restructure_group_dict2[x][y]}
        
        final_data_list3.append(final_dict3)


#create_premade_layout('2d-layout-1', final_data_list1)
#create_premade_layout('pie-layout-1', final_data_list3)
#create_premade_layout('pie-layout-1', final_data_list2)


"""
# Cross Chain Bridge TVL Metrics 
Welcome to our on-chain analysis dashboard! In this dashboard, you can view the weekly TVL of the cross-chain bridges Hyphen, Hop, Stargate, Across, and Synaps. Additionally, you can see the breakdown of each bridge's weekly TVL by the chain its on."""

create_premade_layout('2d-layout-1', final_data_list1)
"""
### Description  
The graphs above shows the weekly and overall average TVL of cross chain bridges Hyphen, Hop, Stargate, Across, and Synaps in the past 90 days.
"""

create_premade_layout('pie-layout-1', final_data_list3)
"""
### Description  
The graph above shows the weekly bridge TVL broken down by cross chain bridges Hyphen, Hop, Stargate, Across, and Synaps
"""

create_premade_layout('pie-layout-1', final_data_list2)
"""
### Description  
The graph above shows the TVL of each bridge broken down by the chain. 
"""
