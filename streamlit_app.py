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
                          ['NAV', 'treemap', 'spiderweb'],
                          # index = 0,
                          label_visibility = 'collapsed',
                          key = 'disabled')
#%%
#https://finance.yahoo.com/quote/JWN/chart?p=JWN#eyJpbnRlcnZhbCI6ImRheSIsInBlcmlvZGljaXR5IjoxLCJ0aW1lVW5pdCI6bnVsbCwiY2FuZGxlV2lkdGgiOjgsImZsaXBwZWQiOmZhbHNlLCJ2b2x1bWVVbmRlcmxheSI6dHJ1ZSwiYWRqIjp0cnVlLCJjcm9zc2hhaXIiOnRydWUsImNoYXJ0VHlwZSI6ImxpbmUiLCJleHRlbmRlZCI6ZmFsc2UsIm1hcmtldFNlc3Npb25zIjp7fSwiYWdncmVnYXRpb25UeXBlIjoib2hsYyIsImNoYXJ0U2NhbGUiOiJwZXJjZW50Iiwic3R1ZGllcyI6eyLigIx2b2wgdW5kcuKAjCI6eyJ0eXBlIjoidm9sIHVuZHIiLCJpbnB1dHMiOnsiaWQiOiLigIx2b2wgdW5kcuKAjCIsImRpc3BsYXkiOiLigIx2b2wgdW5kcuKAjCJ9LCJvdXRwdXRzIjp7IlVwIFZvbHVtZSI6IiMwMGIwNjEiLCJEb3duIFZvbHVtZSI6IiNmZjMzM2EifSwicGFuZWwiOiJjaGFydCIsInBhcmFtZXRlcnMiOnsid2lkdGhGYWN0b3IiOjAuNDUsImNoYXJ0TmFtZSI6ImNoYXJ0In19fSwicGFuZWxzIjp7ImNoYXJ0Ijp7InBlcmNlbnQiOjEsImRpc3BsYXkiOiJKV04iLCJjaGFydE5hbWUiOiJjaGFydCIsImluZGV4IjowLCJ5QXhpcyI6eyJuYW1lIjoiY2hhcnQiLCJwb3NpdGlvbiI6bnVsbH0sInlheGlzTEhTIjpbXSwieWF4aXNSSFMiOlsiY2hhcnQiLCLigIx2b2wgdW5kcuKAjCJdfX0sInNldFNwYW4iOnt9LCJsaW5lV2lkdGgiOjIsInN0cmlwZWRCYWNrZ3JvdW5kIjp0cnVlLCJldmVudHMiOnRydWUsImNvbG9yIjoiIzAwODFmMiIsInN0cmlwZWRCYWNrZ3JvdWQiOnRydWUsImV2ZW50TWFwIjp7ImNvcnBvcmF0ZSI6eyJkaXZzIjp0cnVlLCJzcGxpdHMiOnRydWV9LCJzaWdEZXYiOnt9fSwic3ltYm9scyI6W3sic3ltYm9sIjoiSldOIiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IkpXTiIsInF1b3RlVHlwZSI6IkVRVUlUWSIsImV4Y2hhbmdlVGltZVpvbmUiOiJBbWVyaWNhL05ld19Zb3JrIn0sInBlcmlvZGljaXR5IjoxLCJpbnRlcnZhbCI6ImRheSIsInRpbWVVbml0IjpudWxsLCJzZXRTcGFuIjp7fX0seyJzeW1ib2wiOiJBQVBMIiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IkFBUEwifSwicGVyaW9kaWNpdHkiOjEsImludGVydmFsIjoiZGF5IiwidGltZVVuaXQiOm51bGwsInNldFNwYW4iOnt9LCJpZCI6IkFBUEwiLCJwYXJhbWV0ZXJzIjp7ImNvbG9yIjoiIzcyZDNmZiIsIndpZHRoIjoyLCJpc0NvbXBhcmlzb24iOnRydWUsInNoYXJlWUF4aXMiOnRydWUsImNoYXJ0TmFtZSI6ImNoYXJ0Iiwic3ltYm9sT2JqZWN0Ijp7InN5bWJvbCI6IkFBUEwifSwicGFuZWwiOiJjaGFydCIsImZpbGxHYXBzIjpmYWxzZSwiYWN0aW9uIjoiYWRkLXNlcmllcyIsInN5bWJvbCI6IkFBUEwiLCJnYXBEaXNwbGF5U3R5bGUiOiJ0cmFuc3BhcmVudCIsIm5hbWUiOiJBQVBMIiwib3ZlckNoYXJ0Ijp0cnVlLCJ1c2VDaGFydExlZ2VuZCI6dHJ1ZSwiaGVpZ2h0UGVyY2VudGFnZSI6MC43LCJvcGFjaXR5IjoxLCJoaWdobGlnaHRhYmxlIjp0cnVlLCJ0eXBlIjoibGluZSIsInN0eWxlIjoic3R4X2xpbmVfY2hhcnQifX1dfQ--
#https://stackoverflow.com/questions/41599166/python-plotly-legend-positioning-and-formatting
if sidebar_radio == 'NAV':
    year_option = st.selectbox('select year', [i for i in range(2017, 2024)[::-1]])
    # note : no FTSE, MAI
    # data source; www.investing.com
    index_files = glob.glob('./indices/*.csv')
    indices_dict = {file.split('/')[-1].split(' His')[0]: pd.read_csv('./indices/'+file.split('/')[-1]) for file in index_files}

    nav_df = pd.read_csv('./nav_df.csv')

    nav_df1 = nav_df[pd.to_datetime(nav_df['date'], format = '%Y-%m-%dT%H:%M:%S').dt.year == year_option].reset_index(drop = True)

    performance_df = pd.DataFrame()
    for short_code in nav_df1.short_code.unique():
        df1 = nav_df1[nav_df1['short_code'] == short_code].sort_values(by = ['date'], ascending = True).reset_index(drop = True)
        nav_df1['pct_change'] = nav_df1['value'].pct_change()
        ret = (nav_df1['value'][nav_df1.shape[0] - 1] / nav_df1['value'][0]) - 1
        stdev = nav_df1['pct_change'].std()
        sharpe = ret / stdev
        performance_df = pd.concat([performance_df, 
                                    pd.DataFrame([[short_code, ret, stdev, sharpe]], columns = ['short_code', 'mean', 'stdev', 'sharpe'])],
                                    axis = 0).reset_index(drop = True)
    st.dataframe(performance_df.sort_values(by = 'mean'))

    index_options = st.multiselect('select index', 
                                    indices_dict.keys(), 
                                    ['SET Index', 'VN Index'])

    fund_options = st.multiselect('select fund(s)', 
                                    nav_df1.short_code.unique().tolist(), 
                                    nav_df1.short_code.unique().tolist()[0])

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
        # st.write(index['Price'].dtypes)
        if index_df['Price'].dtype == 'float64':
            pass
        else:
            index_df['Price'] = index_df['Price'].map(lambda x: (''.join(x.split(',')))).astype(float)
        index_df['Index'] = (index_df['Price']/ index_df.loc[0, 'Price']) - 1

        fig.add_trace(go.Scatter(x = index_df.Date,
                                y = index_df.Index,
                                mode = 'lines',
                                line = dict(width = 3, dash = 'dot'),
                                name = index,
                                hovertemplate = index + ': %{y:.2%}<extra></extra>'))

    for short_code in df.short_code.unique():
        df1 = df[df['short_code'] == short_code].reset_index(drop = True)
        df1['Index'] = (df1['value'] / df1.loc[0, 'value']) -1
        fig.add_trace(go.Scatter(x = df1.date,
                                y = df1.Index,
                                mode = 'lines',
                                line = dict(width = 1),
                                name = df1.loc[0, 'short_code'],
                                hovertemplate = short_code + ': %{y:.2%}<extra></extra>'))
    fig.layout.yaxis.tickformat = ',.0%'
    fig.update_layout(legend=dict(
                            yanchor="auto",
                            y=0.99,
                            xanchor="left",
                            x=0.01
                        ))

    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = True,  linewidth=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(index_df, use_container_width = True)
    
# %%
# color: darkmint
elif sidebar_radio == 'treemap':

    nav_df = pd.read_csv('nav_df.csv')
    name_df = pd.read_csv('viet_fund.csv')
    # %%
    #PRINCIPAL VTOPP-X  มูลค่าทรัพย์สินสุทธิ   1,452,292.3 บาท
    year_option = st.selectbox('select year', [i for i in range(2017, 2024)[::-1]])
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
