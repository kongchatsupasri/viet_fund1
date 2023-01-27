#%%
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
# %%
nav_df = pd.read_csv('./nav_df.csv')
# %%
fund_options = st.multiselect('select fund(s)', nav_df.short_code.unique().tolist(), 'K-VIETNAM')
year_option = st.selectbox('select year', pd.to_datetime(nav_df['date']).dt.year.unique().tolist())

df = nav_df[nav_df['short_code'].isin(fund_options)]
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%dT%H:%M:%S')
# %%
df = df[df['date'].dt.year == year_option].reset_index(drop = True)
# %%
fig = go.Figure()
for short_code in df.short_code.unique():

    df1 = df[df['short_code'] == short_code].reset_index(drop = True)

    fig.add_trace(go.Scatter(x = df1.date,
                            y = df1.value,
                            mode = 'lines',
                            name = df1.loc[0, 'short_code']))
st.plotly_chart(fig, use_container_width=True)
# %%
