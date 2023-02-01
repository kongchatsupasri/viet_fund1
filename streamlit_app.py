#%%
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import glob
import numpy as np
import plotly.express as px
# %% 
st.header('🇻🇳 vietnam fund')
with st.sidebar:
  st.header(':round_pushpin: Dashboard')
  sidebar_radio = st.radio('sidebar_radio',
                          ['📈 NAV', '🌳 treemap', '📍 xxx'],
                          # index = 0,
                          label_visibility = 'collapsed',
                          key = 'disabled')
#%%
if sidebar_radio == '📈 NAV':
    year_option = st.selectbox('select year', [i for i in range(2017, 2024)])
    # note : no FTSE
    # data source; www.investing.com
    index_files = glob.glob('./indices/*.csv')
    indices_dict = {file.split('/')[-1].split(' His')[0]: pd.read_csv('./indices/'+file.split('/')[-1]) for file in index_files}

    nav_df = pd.read_csv('./nav_df.csv')

    nav_df1 = nav_df[pd.to_datetime(nav_df['date'], format = '%Y-%m-%dT%H:%M:%S').dt.year == year_option].reset_index(drop = True)

    index_options = st.multiselect('select index', indices_dict.keys(), ['SET Index', 'VN Index'])
    fund_options = st.multiselect('select fund(s)', nav_df1.short_code.unique().tolist(), nav_df1.short_code.unique().tolist()[0])

    df = nav_df1[nav_df1['short_code'].isin(fund_options)]
    df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%dT%H:%M:%S')

    df = df[df['date'].dt.year == year_option].reset_index(drop = True)

    indices_dict = {file.split('/')[-1].split(' His')[0]: pd.read_csv('./indices/'+file.split('/')[-1]) for file in index_files}
    fig = go.Figure()

    for index in index_options:
        index_df = indices_dict[index]
        index_df['Date'] = pd.to_datetime(index_df['Date'], format = '%m/%d/%Y')
        index_df = index_df.sort_values(by = ['Date'], ascending = True)
        index_df = index_df[index_df.Date.dt.year == year_option].reset_index(drop = True)

        index_df['Price'] = index_df['Price'].str.replace(',', '').astype(float)
        index_df['Index'] = (index_df['Price']/ index_df.loc[0, 'Price']) * 100
        

        fig.add_trace(go.Scatter(x = index_df.Date,
                                y = index_df.Index,
                                mode = 'lines',
                                line = dict(width = 2, dash = 'dot'),
                                name = index))

    for short_code in df.short_code.unique():
        df1 = df[df['short_code'] == short_code].reset_index(drop = True)
        df1['Index'] = (df1['value'] / df1.loc[0, 'value']) * 100
        fig.add_trace(go.Scatter(x = df1.date,
                                y = df1.Index,
                                mode = 'lines',
                                name = df1.loc[0, 'short_code']))
    st.plotly_chart(fig, use_container_width=True)
# %%

elif sidebar_radio == '🌳 treemap':
    nav_df = pd.read_csv('nav_df.csv')
    name_df = pd.read_csv('viet_fund.csv')
    # %%
    #PRINCIPAL VTOPP-X  มูลค่าทรัพย์สินสุทธิ   1,452,292.3 บาท
    year_option = st.selectbox('select year', [i for i in range(2017, 2024)])
    nav_df = nav_df[pd.to_datetime(nav_df.date, format = '%Y-%m-%d').dt.year == year_option]

    df = pd.DataFrame()
    for short_code in nav_df.short_code.unique():
        parent = name_df[name_df['short_code'] == short_code].cat_name_en.values[0] + ' | ' + name_df[name_df['short_code'] == short_code].sub_cat_name_en.values[0]
        nav_df1 = nav_df[nav_df['short_code'] == short_code].reset_index(drop = True)
        ret = (nav_df1.iloc[-1, -2] / nav_df1.iloc[0, -2]) - 1
        size = nav_df1.iloc[-1, -1] / 1000000
        df = pd.concat([df, 
                        pd.DataFrame([[parent, short_code, ret, size]], columns = ['parent', 'id', 'ret', 'size'])],
                        axis = 0)


    selected_color = st.selectbox('select colorscales', 
                                   px.colors.named_colorscales())           
    fig = px.treemap(df, path=[px.Constant("vietnam fund"), 'parent', 'id'], values='size',
                    color='ret', hover_data=['ret', 'size'],
                    color_continuous_scale=selected_color,
                    color_continuous_midpoint=np.average(df['ret'], weights=df['size']))
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, use_container_width=True)
# %%
